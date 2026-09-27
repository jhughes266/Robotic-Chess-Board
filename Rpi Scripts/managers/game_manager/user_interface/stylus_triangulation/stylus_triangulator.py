import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import copy
import math
from scipy import signal
from managers.game_manager.user_interface.stylus_triangulation.camera import *

class StylusTriangulator:
    def __init__(self, aCamObj, bCamObj, resourcesPath, aCamType, bCamType):
        # store the camera objects as private attributes
        self.__aCamObj = aCamObj
        self.__bCamObj = bCamObj
        # store the camera matrices in private attributes
        self.__aCamMatrix = np.loadtxt(resourcesPath + f"/calibration_results/{aCamType}_cam/camera_matrix.txt")
        self.__bCamMatrix = np.loadtxt(resourcesPath + f"/calibration_results/{bCamType}_cam/camera_matrix.txt")
        # store the distortion coefficients in private attributes
        self.__aDistCoeffs = np.loadtxt(resourcesPath + f"/calibration_results/{aCamType}_cam/dist.txt")
        self.__bDistCoeffs = np.loadtxt(resourcesPath + f"/calibration_results/{bCamType}_cam//dist.txt")
        # offset with a as the origin
        self.__offset = np.loadtxt(resourcesPath + '/calibration_results/offset.txt')
        
        self.__vaMovingAverage = []
        self.__uaMovingAverage = []
        self.__vbMovingAverage = []
        self.__ubMovingAverage = []

    def setUp(self):
        # Camera object setup
        self.__aCamObj.setUp()
        self.__bCamObj.setUp()
    
    def tearDown(self):
        self.__aCamObj.tearDown()
        self.__bCamObj.tearDown()

    def run(self):
        # First capture the images from both cameras
        aCamImage, bCamImage = self.__captureImages()
        # Undistort the images and get the new camera matricies
        aCamImageUndistorted, aNewCamMatrix = self.__undistortImage(aCamImage, self.__aCamMatrix, self.__aDistCoeffs)
        bCamImageUndistorted, bNewCamMatrix = self.__undistortImage(bCamImage, self.__bCamMatrix, self.__bDistCoeffs)
        # Extract all the hand keypoints from both images
        ua, va, ub, vb = self.__stylusExtraction(aCamImageUndistorted, bCamImageUndistorted)
        stylusRealWorldLocation = None
        # Get the realworld location of the stylus (can just check if ua is None because in an invalid result all coordinates
        # will be None)
        if ua is not None:
            stylusRealWorldLocation = self.__triangulePoints(
                ua=ua,
                va=va,
                ub=ub,
                vb=vb,
                aNewCamMatrix=aNewCamMatrix,
                bNewCamMatrix=bNewCamMatrix,
                offset=self.__offset)

        return stylusRealWorldLocation

    def __captureImages(self):
        #Capture images from both cameras
        aCamImage = self.__aCamObj.captureImage()
        bCamImage = self.__bCamObj.captureImage()
        return aCamImage, bCamImage

    def __undistortImage(self, image, camMatrix, distCoeffs):
        # Get the height and the width of the image
        h, w = image.shape[:2]
        # Get the new camera matrix and roi
        newCamMatrix, roi = cv2.getOptimalNewCameraMatrix(camMatrix, distCoeffs, (w, h), 0, (w, h))
        # Undistort the image
        undistorted = cv2.undistort(image, camMatrix, distCoeffs, None, newCamMatrix)
        x, y, w, h = roi
        # Perform cropping on the undistored image to make sure that we only get good pixels
        croppedUndistorted = undistorted[y:y + h, x:x + w]
        return croppedUndistorted, newCamMatrix

    def __stylusExtraction(self, aCamImage, bCamImage):
        #Copy the image for display
        dispImageA = copy.deepcopy(aCamImage)
        dispImageB = copy.deepcopy(bCamImage)
        # Convert the images to signed 16 bit integer as we need to be able to have negative numbers for processing
        aCamImage = aCamImage.astype(np.int16)
        bCamImage = bCamImage.astype(np.int16)
        # Calculate the ammount of green in each image by doubling the green channel and then subtracting the blue
        # and red channels. The doubling is done because we are subtracting 2 channels from the green.
        aGreenAmount = 2 * aCamImage[:,:,1]- aCamImage[:,:,0] - aCamImage[:,:,2]
        aGreenAmount = (np.where(aGreenAmount < 0, 0, aGreenAmount))
        aGreenAmount = (np.where(aGreenAmount > 255, 255, aGreenAmount))
        
        bGreenAmount = 2 * bCamImage[:,:,1]- bCamImage[:,:,0] - bCamImage[:,:,2]
        bGreenAmount = (np.where(bGreenAmount < 0, 0, bGreenAmount))
        bGreenAmount = (np.where(bGreenAmount > 255, 255, bGreenAmount))
        # Different thresholds for each of the cameras
        aGreenAmountThreshold = 110
        bGreenAmountThreshold = 45
        # Anything bellow the threshold is discraded.
        aGreenAmount = (np.where(aGreenAmount < aGreenAmountThreshold, 0, aGreenAmount))
        bGreenAmount = (np.where(bGreenAmount < bGreenAmountThreshold, 0, bGreenAmount))
        
        aGreenAmount = (np.where(aGreenAmount > aGreenAmountThreshold, 255, aGreenAmount))
        bGreenAmount = (np.where(bGreenAmount > bGreenAmountThreshold, 255, bGreenAmount))
        #Convert arrays back to unsigned 8 bit integers
        aGreenAmount = aGreenAmount.astype(np.uint8)
        bGreenAmount = bGreenAmount.astype(np.uint8)
        # Get the locations of pixels that are above the threshold
        vaArray, uaArray = np.where(aGreenAmount == 255)
        vbArray, ubArray = np.where(bGreenAmount == 255)
        # Number of active pixels to be determined a detection
        aActivePixelThreshold = 30
        bActivePixelThreshold = 5
        # If there is nothing above the threshold then the stylus is not in the image
        if len(vaArray) < aActivePixelThreshold or len(vbArray) < bActivePixelThreshold:
            combinedImage = np.hstack((dispImageB, dispImageA))
            self.__vaMovingAverage = []
            self.__uaMovingAverage = []
            self.__vbMovingAverage = []
            self.__ubMovingAverage = []
            #combinedImage = np.hstack((bGreenAmount, aGreenAmount))
            cv2.imshow('test',combinedImage)
            return None, None, None, None
        # Get the median of all the returned pixel locations (median helps get rid of outliers)
        va = int(np.median(vaArray))
        ua = int(np.median(uaArray))
        vb = int(np.median(vbArray))
        ub = int(np.median(ubArray))
        
        if len(self.__vaMovingAverage) < 5:
            self.__vaMovingAverage.append(va)
            self.__uaMovingAverage.append(ua)
            self.__vbMovingAverage.append(vb)
            self.__ubMovingAverage.append(ub)
            
            va = sum(self.__vaMovingAverage)/len(self.__vaMovingAverage)
            ua = sum(self.__uaMovingAverage)/len(self.__uaMovingAverage)
            vb = sum(self.__vbMovingAverage)/len(self.__vbMovingAverage)
            ub = sum(self.__ubMovingAverage)/len(self.__ubMovingAverage)
        else:
            self.__vaMovingAverage.pop(0)
            self.__uaMovingAverage.pop(0)
            self.__vbMovingAverage.pop(0)
            self.__ubMovingAverage.pop(0)
            
            self.__vaMovingAverage.append(va)
            self.__uaMovingAverage.append(ua)
            self.__vbMovingAverage.append(vb)
            self.__ubMovingAverage.append(ub)
            
            va = sum(self.__vaMovingAverage)/len(self.__vaMovingAverage)
            ua = sum(self.__uaMovingAverage)/len(self.__uaMovingAverage)
            vb = sum(self.__vbMovingAverage)/len(self.__vbMovingAverage)
            ub = sum(self.__ubMovingAverage)/len(self.__ubMovingAverage)
        
        va = int(va)
        ua = int(ua)
        vb = int(vb)
        ub = int(ub)
        cv2.circle(dispImageA, (ua, va), radius=3, color=(0,0,255), thickness=-1)
        cv2.circle(dispImageB, (ub, vb), radius=3, color=(0,0,255), thickness=-1)
        
        combinedImage = np.hstack((dispImageB, dispImageA))
        #combinedImage = np.hstack((bGreenAmount, aGreenAmount))
        cv2.imshow('test',combinedImage)

        return ua, va, ub, vb
    
    def __triangulePoints(self, ua, va, ub, vb, aNewCamMatrix, bNewCamMatrix, offset):
        # IMPORTANT: The -1's ensure that the tracking result produces the desired cordinate system. That
        # is x:left from aCam Optical Centre y:up from aCam Optical Centre and z:forward from aCam optical Centre
        # This is the offset for camera b
        xOffset = offset[0]
        yOffset = offset[1]
        zOffset = offset[2] * -1
        # Extract the intrinsic properties for both cameras from each of the camera matrices
        fxa = aNewCamMatrix[0][0] * -1
        fya = aNewCamMatrix[1][1] * -1
        oxa = aNewCamMatrix[0][2]
        oya = aNewCamMatrix[1][2]

        fxb = bNewCamMatrix[0][0] * -1
        fyb = bNewCamMatrix[1][1] * -1
        oxb = bNewCamMatrix[0][2]
        oyb = bNewCamMatrix[1][2]
        # calculate the components of the a direction vector
        ia = (ua - oxa) / (fxa)
        ja = (va - oya) / (fya)
        ka = 1
        # calculate the components of the b direction vector
        ib = (ub - oxb) / (fxb)
        jb = (vb - oyb) / (fyb)
        kb = 1
        # Constructing the direction vectors
        aDir = np.array([ia, ja, ka])
        bDir = np.array([ib, jb, kb])
        # Construct the position vector for b (this is the offset) we assume that a starts at (0,0,0)
        bPos = np.array([xOffset, yOffset, zOffset])
        # Calculating the different quantities for the triangulation equations
        P = np.sum(aDir * aDir)
        S = np.sum(aDir * bDir)
        R = np.sum(aDir * bPos)
        T = np.sum(bDir * bDir)
        U = np.sum(bDir * bPos)
        # Using the calculated simultaneous equations to get the parameters
        denominator = P*T - S**2
        ta = (R*T - S*U)/denominator
        tb = (S*R - P*U)/denominator
        # Using the parameters to construct the line equations and get the locations of the minimum distance between lines
        aLocMin = ta * aDir
        bLocMin = tb * bDir + bPos
        # Getting the average of the two to get the best estimate of the location of the minimum distance
        realWorldLocation = aLocMin#(aLocMin + bLocMin) / 2
        # Returning the real world location of the landmarks
        return realWorldLocation


