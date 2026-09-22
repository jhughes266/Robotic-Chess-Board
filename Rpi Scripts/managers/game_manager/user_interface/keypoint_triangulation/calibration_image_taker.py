import copy
import cv2
from managers.game_manager.user_interface.keypoint_triangulation.camera import *
import time

def showChessBoardDetection(image):
    # Deepcopy the image so that when drawing on this one it doesnt effect the original
    imageCopy = copy.deepcopy(image)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # Turn the image gray
    gray = cv2.cvtColor(imageCopy, cv2.COLOR_BGR2GRAY)
    # Find chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, chessBoardSize, None)
    # If found draw corners on the baord
    if ret == True:
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        cv2.drawChessboardCorners(imageCopy, chessBoardSize, corners2, ret)
    # Return the copy of the image
    return imageCopy

# Define either 'csi' or 'usb' depending on which camera you want to use to take the images
mode = 'csi'
# Size of the chessboard in the image
chessBoardSize = (7, 6)
# Instantiate the camera devices
if mode == 'usb':
    cam = OpenCvDevice(captureWidth=640, captureHeight=480, deviceIndex = 1)
elif mode == 'csi':
    cam = PiCameraDevice(captureWidth=640, captureHeight=480, deviceIndex = 0)
# Call the setup method on the camera
cam.setUp()
# Store the image save count which is used to name files
imageSaveCount = 0
# Keep going until the user specifies
while True:
    #capture the image with the camera
    image = cam.captureImage()
    if image is None:
        continue
    # Perform the chessboard pattern detection on the image to see if the image works
    displayImage = showChessBoardDetection(image)
    # Show the image with the chessboard pattern
    cv2.imshow('capture', displayImage)
    # Capture the key press
    key = cv2.waitKey(0) & 0xFF
    # Save the image if 'y'
    if key == ord('y'):
        cv2.imwrite(f"resources/calibration_images/{mode}_cam/cal_{imageSaveCount}.jpg", image)
        print("Image Saved")
        imageSaveCount += 1
    # Quit the capturing if 'q'
    elif key == ord('q'):
        break
    elif key == ord('n'):
        print("Image Rejected")
    # Redo if anything else
    #time.sleep(1)
cv2.destroyAllWindows()
# Free camera resources
cam.tearDown()

