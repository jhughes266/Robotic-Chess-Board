import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import matplotlib.pyplot as plt
import numpy as np
import copy

from managers.game_manager.user_interface.keypoint_triangulation.camera import *

class KeypointTriangulator:
    def __init__(self, aCamObj, bCamObj, aCamIntrinsicDir, bCamIntrinsicDir):
        # store the camera objects as private attributes
        self.__aCamObj = aCamObj
        self.__bCamObj = bCamObj
        # store the camera matrices in private attributes
        self.__aCamMatrix = np.loadtxt(aCamIntrinsicDir + '/camera_matrix.txt')
        self.__bCamMatrix = np.loadtxt(bCamIntrinsicDir + '/camera_matrix.txt')
        # store the distortion coefficients in private attributes
        self.__aDistCoeffs = np.loadtxt(aCamIntrinsicDir + '/dist.txt')
        self.__bDistCoeffs = np.loadtxt(bCamIntrinsicDir + '/dist.txt')
        # offset with a as the origin
        self.__offset = np.loadtxt('resources/calibration_results/offset.txt')

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
        # Get the realworld location of all the landmarks
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
        
        dispImageA = copy.deepcopy(aCamImage)
        dispImageB = copy.deepcopy(bCamImage)
    
        aCamImage = aCamImage.astype(np.int32)
        bCamImage = bCamImage.astype(np.int32)
        
        aGreenAmount = 2 * aCamImage[:,:,1]- aCamImage[:,:,0] - aCamImage[:,:,2]
        aGreenAmount = (np.where(aGreenAmount < 0, 0, aGreenAmount))
        aGreenAmount = (np.where(aGreenAmount > 255, 255, aGreenAmount))
        
        bGreenAmount = 2 * bCamImage[:,:,1]- bCamImage[:,:,0] - bCamImage[:,:,2]
        bGreenAmount = (np.where(bGreenAmount < 0, 0, bGreenAmount))
        bGreenAmount = (np.where(bGreenAmount > 255, 255, bGreenAmount))
        
        
        aGreenAmount = aGreenAmount.astype(np.uint8)
        bGreenAmount = bGreenAmount.astype(np.uint8)
        
        aThreshold = 110
        bThreshold = 45
        
        aGreenAmount = (np.where(aGreenAmount < aThreshold, 0, aGreenAmount))
        bGreenAmount = (np.where(bGreenAmount < bThreshold, 0, bGreenAmount))
        aGreenAmount = (np.where(aGreenAmount > aThreshold, 255, aGreenAmount))
        bGreenAmount = (np.where(bGreenAmount > bThreshold, 255, bGreenAmount))
        
        vaArray, uaArray = np.where(aGreenAmount > aThreshold)
        vbArray, ubArray = np.where(bGreenAmount > bThreshold)
        if len(vaArray) == 0 or len(uaArray) == 0 or len(vbArray) == 0 or len(ubArray) == 0:
            combinedImage = np.hstack((dispImageB, dispImageA))
            cv2.imshow('test',combinedImage)
            return None, None, None, None    
        va = int(np.average(vaArray))
        ua = int(np.average(uaArray))
        vb = int(np.average(vbArray))
        ub = int(np.average(ubArray))
        
        cv2.circle(dispImageA, (ua, va), radius=3, color=(0,0,255), thickness=-1)
        cv2.circle(dispImageB, (ub, vb), radius=3, color=(0,0,255), thickness=-1)
        
        combinedImage = np.hstack((dispImageB, dispImageA))
        cv2.imshow('test',combinedImage)


        return ua, va, ub, vb

    def __triangulePoints(self, ua, va, ub, vb, aNewCamMatrix, bNewCamMatrix, offset):
        # IMPORTANT: The -1's ensure that the tracking result produces the desired cordinate system. That
        # is x:left from aCam Optical Centre y:up from aCam Optical Centre and z:forward from aCam optical Centre
        print(f"ua:{ua},va:{va},ub:{ub},vb:{vb},")
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
        realWorldLocation = (aLocMin + bLocMin) / 2
        # Returning the real world location of the landmarks
        return realWorldLocation

    def __drawKeypoints(self, results, image):
        hand_landmarks_list = results.hand_landmarks
        #print(results.handedness)
        if len(hand_landmarks_list) > 0:
            for hand in hand_landmarks_list:
                for landmark in hand:
                    cv2.circle(image, (int(landmark.x), int(landmark.y)), 2, (0, 0, 255), -1)




aCam = OpenCvDevice(captureWidth=640, captureHeight=480, deviceIndex=0)
bCam = PiCameraDevice(captureWidth=640, captureHeight=480, deviceIndex = 0)

#testCam2 = OpenCvDevice(captureWidth=640, captureHeight=480, deviceIndex=0)
testTri = KeypointTriangulator(aCamObj=aCam, bCamObj=bCam,aCamIntrinsicDir='resources/calibration_results/usb_cam', bCamIntrinsicDir='resources/calibration_results/csi_cam')
testTri.setUp()

while True:
    ### For debugging ####
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    stylusRealWorldLocation = testTri.run()
    if stylusRealWorldLocation is not None:
        print(stylusRealWorldLocation)
        print("###################################################")


testTri.tearDown()


