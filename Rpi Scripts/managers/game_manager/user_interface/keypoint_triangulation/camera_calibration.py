import cv2
import glob
import numpy as np

def calibrateCamera(cameraName,
                    chessBoardSize,
                    chessBoardSquareSideLength,
                    calibrationPatternsDirectory,
                    testUndistortPath,
                    patternFileExtension = '.jpg'):
    # Get all the images
    images = glob.glob(calibrationPatternsDirectory + '*' + patternFileExtension)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # A numpy array representing where all the points are on the chessboard plane
    objp = np.zeros((chessBoardSize[0]*chessBoardSize[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessBoardSize[0], 0:chessBoardSize[1]].T.reshape(-1, 2) * chessBoardSquareSideLength
    # Lists to store the object points and image points
    objPoints = []
    imgPoints = []
    # Loop through all the available files
    for fileName in images:
        # Read the image
        image = cv2.imread(fileName)
        # Convert the image to gray
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Get chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, chessBoardSize, None)
        # If the detection is successful
        if ret == True:
            # Append object points
            objPoints.append(objp)
            # Increase corner accuracy
            corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            # Append corners to the image point list
            imgPoints.append(corners)
            # Draw the image detected pattern on the board
            cv2.drawChessboardCorners(image, chessBoardSize, corners2, ret)
            cv2.imshow('img', image)
            cv2.waitKey(100)
    # Destroy all windows
    cv2.destroyAllWindows()
    # Perform camera calibration
    ret, cameraMatrix, dist, rvecs, tvecs = cv2.calibrateCamera(objPoints, imgPoints, gray.shape[::-1], None, None)
    # Save the camera matrix and the distortion coefficients
    np.savetxt('resources/calibration_results/' + cameraName + '/camera_matrix.txt', cameraMatrix)
    np.savetxt('resources/calibration_results/' + cameraName + '/dist.txt', dist)
    # Test the camera matrix and distortion on an image taken by the camera
    newImage = cv2.imread(testUndistortPath)
    h, w = newImage.shape[:2]
    newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w, h), 0, (w, h))
    dst = cv2.undistort(newImage, cameraMatrix, dist, None, newCameraMatrix)
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]
    cv2.imshow('dst', dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # Get the reprojection error
    
    meanError = 0
    for i in range(len(objPoints)):
        imgpoints2, _ = cv2.projectPoints(objPoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
        imgpoints2 = imgpoints2.reshape(-1,2)
        error = cv2.norm(imgPoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        meanError += error
    print(f"The total error is: {meanError/len(objPoints)}")
    
calibrateCamera(cameraName='csi_cam',
                chessBoardSize=(7,6),
                chessBoardSquareSideLength=28.5,
                testUndistortPath='resources/csiTest.jpg',
                calibrationPatternsDirectory='resources/calibration_images/csi_cam/')


calibrateCamera(cameraName='usb_cam',
                chessBoardSize=(7,6),
                chessBoardSquareSideLength=28.5,
                testUndistortPath='resources/usbTest.jpg',
                calibrationPatternsDirectory='resources/calibration_images/usb_cam/')

