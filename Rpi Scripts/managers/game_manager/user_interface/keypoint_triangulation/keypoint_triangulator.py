import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import matplotlib.pyplot as plt
import numpy as np

#from mediapipe.tasks.python.vision.drawing_utils import draw_landmarks

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
        # Media pipe hands setup
        base_options = python.BaseOptions(model_asset_path='resources/hands_model/hand_landmarker.task')
        options = vision.HandLandmarkerOptions(base_options=base_options,
                                               min_hand_detection_confidence=0.05,
                                               min_hand_presence_confidence=0.05,
                                               min_tracking_confidence=0.05,
                                               num_hands=1)
        self.__detector = vision.HandLandmarker.create_from_options(options=options)

    def tearDown(self):
        self.__aCamObj.tearDown()
        self.__bCamObj.tearDown()
        self.__detector.close()

    def run(self):
        # First capture the images from both cameras
        aCamImage, bCamImage = self.__captureImages()
        # Undistort the images and get the new camera matricies
        aCamImageUndistorted, aNewCamMatrix = self.__undistortImage(aCamImage, self.__aCamMatrix, self.__aDistCoeffs)
        bCamImageUndistorted, bNewCamMatrix = self.__undistortImage(bCamImage, self.__bCamMatrix, self.__bDistCoeffs)
        # Extract all the hand keypoints from both images
        aCamDetectionResult, bCamDetectionResult = self.__keypointExtraction(aCamImageUndistorted, bCamImageUndistorted)
        # The hand must be present in both images otherwise if it is not return None to indicate that triangulation
        # cannot take place
        if aCamDetectionResult is None or bCamDetectionResult is None:
            
            if aCamDetectionResult is not None:
                self.__drawKeypoints(aCamDetectionResult, aCamImageUndistorted)

            if bCamDetectionResult is not None:
                self.__drawKeypoints(bCamDetectionResult, bCamImageUndistorted)
            combinedImage = np.hstack((bCamImageUndistorted, aCamImageUndistorted))
            cv2.imshow('capture', combinedImage)
            return None
        # For debugging purposes we are drawin the location of all the keypoints
        self.__drawKeypoints(aCamDetectionResult, aCamImageUndistorted)
        self.__drawKeypoints(bCamDetectionResult, bCamImageUndistorted)
        # Horizontal stack the images
        combinedImage = np.hstack((bCamImageUndistorted, aCamImageUndistorted))
        # Show the combined images
        cv2.imshow('capture', combinedImage)
        # Get the realworld location of all the landmarks
        landMarkRealWorldLocation = self.__triangulePoints(
            aCamDetectionResult=aCamDetectionResult,
            bCamDetectionResult=bCamDetectionResult,
            aNewCamMatrix=aNewCamMatrix,
            bNewCamMatrix=bNewCamMatrix,
            offset=self.__offset)

        return landMarkRealWorldLocation

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

    def __keypointExtraction(self, aCamImage, bCamImage):
        # Convert all the images to the required RGB
        aCamImageRgb = cv2.cvtColor(aCamImage, cv2.COLOR_BGR2RGB)
        bCamImageRgb = cv2.cvtColor(bCamImage, cv2.COLOR_BGR2RGB)
        # Get the Mp images of both cameras
        aCamMpImage = mp.Image(image_format=mp.ImageFormat.SRGB, data=aCamImageRgb)
        bCamMpImage = mp.Image(image_format=mp.ImageFormat.SRGB, data=bCamImageRgb)
        # Perform the pose detection
        aCamDetectionResult = self.__detector.detect(aCamMpImage)
        bCamDetectionResult = self.__detector.detect(bCamMpImage)
        # If the length of the resulting detection is 0 in either it means the detection was unsuccessful
        if len(aCamDetectionResult.hand_landmarks) == 0 or len(bCamDetectionResult.hand_landmarks) == 0:
            return None, None
        # Put the x and y coordinates in pixels
        aCamDetectionResult = self.__normalizedCordinatesToPixel(results=aCamDetectionResult,
                                                                 xDim=aCamImage.shape[1],
                                                                 yDim=aCamImage.shape[0])

        bCamDetectionResult = self.__normalizedCordinatesToPixel(results=bCamDetectionResult,
                                                                   xDim=bCamImage.shape[1],
                                                                   yDim=bCamImage.shape[0])

        return aCamDetectionResult, bCamDetectionResult
    
    def __normalizedCordinatesToPixel(self, results, xDim, yDim):
        landmarkList = results.hand_landmarks[0]
        for landmark in landmarkList:
            landmark.x = landmark.x * xDim
            landmark.y = landmark.y * yDim
        return results

    def __triangulePoints(self, aCamDetectionResult, bCamDetectionResult , aNewCamMatrix, bNewCamMatrix, offset):
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
        #print(offset)
        #print(f"fxa:{fxa}, fya:{fya}, oxa:{oxa}, oya:{oya}")
        #print(f"fxb:{fxb}, fyb:{fyb}, oxb:{oxb}, oyb:{oyb}")
        
        
        # This list will store all the realworld locations of all the landmarks
        landMarkRealWorldLocation = []
        # zip the landmark lists and loop through each individual landmark
        for i, (aCamLandmark, bCamLandmark) in enumerate(zip(aCamDetectionResult.hand_landmarks[0], bCamDetectionResult.hand_landmarks[0])):
            # Get the location of the landmark for camera a
            ua = aCamLandmark.x
            va = aCamLandmark.y
            # Get the location of the landmark for camera b
            ub = bCamLandmark.x
            vb = bCamLandmark.y
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
            estimatedMinimumDistancePoint = (aLocMin + bLocMin) / 2
            # Storing the result in created list
            landMarkRealWorldLocation.append(estimatedMinimumDistancePoint)
            if i == 8:
                pass
                #print(f"ua:{ua}, va:{va}")
                #print(f"ub:{ub}, vb:{vb}")
                #print(f"Va:{aDir},Vb:{bDir}")
                #print(f"P:{P},S:{S},R:{R},T:{T},U:{U}")
                #print(estimatedMinimumDistancePoint)
        # Returning the real world location of the landmarks
        return landMarkRealWorldLocation

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
    landmarkLocations = testTri.run()
    if landmarkLocations is not None:
        print(landmarkLocations[8])
        print("###################################################")


testTri.tearDown()


