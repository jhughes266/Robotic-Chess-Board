import cv2
import numpy as np

def getCameraCordinate(event, x, y, flags, params):

    if event == cv2.EVENT_LBUTTONDOWN:
        Wx = float(input("Enter world X: "))
        Wy = float(input("Enter world Y: "))
        Wz = float(input("Enter world Z: "))
        W = np.array([[Wx], [Wy], [Wz], [1]])
        homogenous = P@W
        print(f"Cx: {homogenous[0] / homogenous[2]}, Cy: {homogenous[1] / homogenous[2]}")
        cv2.imshow('Resized Image',image)
        print(f"x={x}, y={y}")
        cv2.circle(image, (x, y), 2, (0, 0, 255), -1)
        cv2.imshow('Resized Image', image)




# Load the image
image = cv2.imread('resources/calibration_cube_test_3.jpg')
# Load the projection matrix
P = np.loadtxt('resources/projection_matrix.txt')
# Scale the image down
scaleFactor = 10
newHeight = int(image.shape[0] / scaleFactor)
newWidth = int(image.shape[1] / scaleFactor)
print(f"New Height: {newHeight}\nNew Width: {newWidth}")
image = cv2.resize(image, (newWidth, newHeight))
# Show the image
cv2.imshow('Resized Image',image)
# Attach the mouse callback
cv2.setMouseCallback('Resized Image',getCameraCordinate)
cv2.waitKey(0)
cv2.destroyAllWindows()
