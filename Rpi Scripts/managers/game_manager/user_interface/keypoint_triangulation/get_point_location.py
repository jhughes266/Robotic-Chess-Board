import cv2
import numpy as np
import math
from managers.game_manager.user_interface.keypoint_triangulation.camera import *


def calculateDistanceToPoint(p1, p2, camera_matrix):
    # The actual distance between the selected points in mm
    realDistBetweenPoints = 10
    # Extracting the u and v coordinates from the selected points
    u1 = p1[0]
    v1 = p1[1]
    u2 = p2[0]
    v2 = p2[1]
    # Getting the focal lengths and optical and distance to where the optical axis pierces the plane
    fx = camera_matrix[0][0]
    ox = camera_matrix[0][2]
    fy = camera_matrix[1][1]
    oy = camera_matrix[1][2]
    # Calculate the tangent of the angle between the two points and the optical centre as if
    # the two points were directly above the optical centre.
    tanThetaY1 = abs(v1 - oy) / fy
    tanThetaY2 = abs(v2 - oy) / fy
    # Use the real distance between points and the calculated tangents to get the distance to the points
    zDist = realDistBetweenPoints / (tanThetaY2 - tanThetaY1)
    # Calculate the ratio of between the x coordinate and the focal length. This is the same as the x/z ratio
    # in the real world.
    xzRatio = abs(u1 - ox) / fx
    # Use the previous ratio to get the distance
    xDist = xzRatio * zDist
    # Use pythagoras theorem and the calculated tangent to get the yDist
    yDist = ((xDist**2 + zDist**2)**0.5) * tanThetaY1
    print(f"xDist: {xDist}, yDist: {yDist}, zDist: {zDist}")
    result = np.array([xDist, yDist, zDist])
    np.savetxt('resources/calibration_results/' + mode + '_cam/distance_to_same_point.txt', result)


def getCameraCordinate(event, x, y, flags, params):
    # Triggers when the left button has been clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        # Append a tupple with the x y location of the click
        points.append((x,y))
        # Draw a circle at the click location
        cv2.circle(undistoredImage, (x, y), 1, (0, 0, 255), -1)
        cv2.imshow('Undistorted Image', undistoredImage)
        # Once two clicks have taken place perform the distance calculation
        if len(points) == 2:
            calculateDistanceToPoint(p1=points[0], p2=points[1], camera_matrix=newCameraMatrix)



# Define either 'csi' or 'usb' depending on which camera you want to use to take the images
mode = 'csi'
image = None
# Instantiate the camera devices
if mode == 'usb':
    cam = OpenCvDevice(captureWidth=640, captureHeight=480, deviceIndex = 0)
elif mode == 'csi':
    cam = PiCameraDevice(captureWidth=640, captureHeight=480, deviceIndex = 0)
# Call the setup method on the camera
cam.setUp()
# Keep going until the user specifies
while True:
    #capture the image with the camera
    image = cam.captureImage()
    if image is None:
        continue
    # Show the image with the chessboard pattern
    cv2.imshow('capture', image)
    # Capture the key press
    key = cv2.waitKey(0) & 0xFF
    # Save the image if 'y'
    if key == ord('y'):
        break
    elif key == ord('n'):
        print("Image Rejected")
    # Redo if anything else
    #time.sleep(1)
cv2.destroyAllWindows()
# Free camera resources
cam.tearDown()
# Load the camera matrix and the distortion coefficient
cameraMatrix = np.loadtxt(f"resources/calibration_results/{mode}_cam/camera_matrix.txt")
print(f"The camera matrix is:\n {cameraMatrix}")
print(f"The distorted image has dims of: {image.shape}")
#Load the dist Coeffs
distCoeff = np.loadtxt(f"resources/calibration_results/{mode}_cam/dist.txt")
#Undistort the image
h, w = image.shape[:2]
newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, distCoeff, (w, h), 0, (w, h))
print(f"The new camera matrix is:\n {newCameraMatrix}")
dst = cv2.undistort(image, cameraMatrix, distCoeff, None, newCameraMatrix)
x, y, w, h = roi
undistoredImage = dst[y:y + h, x:x + w]
print(f"The undistorted image has dims of: {undistoredImage.shape}")
# put a circle where the optical axis pierces the sensor
cv2.circle(undistoredImage,
           (int(newCameraMatrix[0][2]), int(newCameraMatrix[1][2])),
           4, (255, 0, 255), -1)
# put a rectangle to indicate the quadrant where you can click
cv2.rectangle(undistoredImage,
              (int(newCameraMatrix[0][2]),0), (undistoredImage.shape[1], int(newCameraMatrix[1][2])),
              (0, 0, 255), 1)
# Show the image
cv2.imshow('Undistorted Image',undistoredImage)
# Store the selected points
print("Please select points that have the same horizontal coordinate. Select the bottom point first and the top point second. Make sure that the points are above and to the right of the optical centre (INSIDE THE RED SQUARE)! The program measures the distance components to the BOTTOM POINT")
points = []
# Attach the mouse callback
cv2.setMouseCallback('Undistorted Image',getCameraCordinate)
cv2.waitKey(0)
cv2.destroyAllWindows()