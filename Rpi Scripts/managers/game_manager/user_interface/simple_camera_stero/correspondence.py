import cv2
import numpy as np

def getCameraCordinate(event, x, y, flags, params):
    global counter

    if event == cv2.EVENT_LBUTTONDOWN:
        correspondenceArray[counter, 3] = x
        correspondenceArray[counter, 4] = y
        if counter != correspondenceArray.shape[0] - 1:
            print(
                f"Please click on the global point \nWx:{correspondenceArray[counter + 1, 0]}\nWy:{correspondenceArray[counter + 1, 1]}\nWz:{correspondenceArray[counter + 1, 2]}")
            counter += 1
        else:
            print("ALL POINTS DONE PRESS ANY KEY TO EXIT")
        cv2.circle(image, (x, y), 2, (0, 0, 255), -1)
        cv2.imshow('Resized Image', image)



# Load the image
image = cv2.imread('resources/calibration_cube_test_1.jpg')
# Scale the image down
scaleFactor = 4
newHeight = int(image.shape[0] / scaleFactor)
newWidth = int(image.shape[1] / scaleFactor)
print(f"New Height: {newHeight}\nNew Width: {newWidth}")
image = cv2.resize(image, (newWidth, newHeight))
# set up the matrix that will store the correspondence
# Counter that keeps track of which real world point we are finding the correspondence for
counter = 0
# each point will be structured like [Wx,Wy,Wz,Cx,Cy] (W is world coordinates and C is camera coordinates)
correspondenceArray = np.full((0, 5), np.nan)
increment = 10
#1st face
Wx = 0
for Wz in range(5,31,increment):
    for Wy in range(5,31,increment):
        correspondence = np.array([Wx, Wy, Wz, np.nan, np.nan])
        correspondenceArray = np.vstack((correspondenceArray, correspondence))
#2nd face
Wz = 35
for Wx in range(5,31,increment):
    for Wy in range(5,31,increment):
        correspondence = np.array([Wx, Wy, Wz, np.nan, np.nan])
        correspondenceArray = np.vstack((correspondenceArray, correspondence))
#3rd face
Wy = 0
for Wz in range(5,31,increment):
    for Wx in range(5,31,increment):
        correspondence = np.array([Wx, Wy, Wz, np.nan, np.nan])
        correspondenceArray = np.vstack((correspondenceArray, correspondence))
# Reset the counter as it is used in the callback function
print(correspondenceArray.dtype)
counter = 0
# Show the image
cv2.imshow('Resized Image',image)
#Prompt clicking on the first point
print(f"Please click on the global point \nWx:{correspondenceArray[counter, 0]}\nWy:{correspondenceArray[counter, 1]}\nWz:{correspondenceArray[counter, 2]}")
# Attach the mouse callback
cv2.setMouseCallback('Resized Image',getCameraCordinate)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(correspondenceArray)
np.savetxt('resources/correspondence.txt', correspondenceArray)
