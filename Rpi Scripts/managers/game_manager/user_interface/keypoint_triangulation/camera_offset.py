import numpy as np
csiDist = np.loadtxt(f"resources/calibration_results/csi_cam/distance_to_same_point.txt")
usbDist = np.loadtxt(f"resources/calibration_results/usb_cam/distance_to_same_point.txt")
print(csiDist)
print(usbDist)
offset = csiDist - usbDist 
print(offset)
np.savetxt('resources/calibration_results/offset.txt', offset)
