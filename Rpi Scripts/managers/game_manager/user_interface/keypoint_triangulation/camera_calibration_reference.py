import cv2
import glob
import numpy as np
"""
KEEPING THIS FOR REFENCE FOR LATER AS IT MAY BE USEFUL TO REFER BACK TO
"""
def calibrateCamera(cameraName,chessBoardSize, chessBoardSquareSideLength, calibrationPatternsDirectory, patternFileExtension = '.jpg'):
    images = glob.glob(calibrationPatternsDirectory + '*' + patternFileExtension)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp = np.zeros((chessBoardSize[0]*chessBoardSize[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessBoardSize[0], 0:chessBoardSize[1]].T.reshape(-1, 2) * chessBoardSquareSideLength

    objPoints = []
    imgPoints = []

    for fileName in images:
        print(fileName)
        image = cv2.imread(fileName)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, chessBoardSize, None)

        if ret == True:
            objPoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            imgPoints.append(corners)

            cv2.drawChessboardCorners(image, chessBoardSize, corners2, ret)
            cv2.imshow('img', image)
            cv2.waitKey(0)

    cv2.destroyAllWindows()

    ret, cameraMatrix, dist, rvecs, tvecs = cv2.calibrateCamera(objPoints, imgPoints, gray.shape[::-1], None, None)

    print(cameraMatrix)
    print("___________________________________")
    print(rvecs)
    print("___________________________________")
    print(tvecs)
    print("___________________________________")


    newImage = cv2.imread('resources/test.jpg')
    h, w = newImage.shape[:2]
    newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w, h), 1, (w, h))
    print(newCameraMatrix)
    print(roi)
    dst = cv2.undistort(newImage, cameraMatrix, dist, None, newCameraMatrix)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv2.imshow('dst', dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


calibrateCamera(cameraName='TestCam',chessBoardSize=(7,7), chessBoardSquareSideLength=28.5, calibrationPatternsDirectory='resources/calibration_images/')

