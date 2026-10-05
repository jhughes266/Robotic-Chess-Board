import numpy as np
"""
Calculates the offset between the two cameras given the distance to the same point in the same realworld scene. We assume
that both sensor planes are parrellel to one and other. We save the results of this offset calculating in an offset text
file. For for information on how the distance two these same two points was calculated refer to the 'get_point_location.py'
file.
"""
csiDist = np.loadtxt(f"resources/calibration_results/csi_cam/distance_to_same_point.txt")
usbDist = np.loadtxt(f"resources/calibration_results/usb_cam/distance_to_same_point.txt")
print(csiDist)
print(usbDist)
offset = csiDist - usbDist
print(offset)
np.savetxt('resources/calibration_results/offset.txt', offset)
