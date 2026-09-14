import glob
import numpy as np
import os
def distanceBetweenPinholes(referenceCamera, offsetCamera, patternFileExtension=".jpg"):
    tvecFileNames = os.listdir('resources/calibration_results/' + referenceCamera + '/tvecs')
    numberOfTvecs = len(tvecFileNames)
    averageXYZdistance = np.zeros(3)
    for tvecFileName in tvecFileNames:
        # Extract the tvecs of the corresponding images
        refrenceTvec = np.loadtxt('resources/calibration_results/' + referenceCamera + '/tvecs/' + tvecFileName)
        if not os.path.exists('resources/calibration_results/' + offsetCamera + '/tvecs/' + tvecFileName):
            continue
        offsetTvec = np.loadtxt('resources/calibration_results/' + offsetCamera + '/tvecs/' + tvecFileName)

        averageXYZdistance += offsetTvec - refrenceTvec

    averageXYZdistance = averageXYZdistance / numberOfTvecs
    print(averageXYZdistance)

distanceBetweenPinholes('csi_cam', 'usb_cam')