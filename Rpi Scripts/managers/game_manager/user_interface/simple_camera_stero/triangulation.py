import matplotlib.pyplot as plt
import numpy as np
def triangulation(uRefCam, vRefCam, uOffsetCam, vOffsetCam, refCameraMatrix, offsetCameraMatrix, xOffset, yOffset, zOffset):
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    ox = 640
    oy = 360
    fx = 3
    fy = 3

    z = np.linspace(0,10,100)
    x = (z * (uRefCam - ox)) / fx
    y = (z * (vRefCam - oy)) / fy
    ax.plot3D(x, y, z, 'red')
    plt.show()


triangulation(uRefCam=330, vRefCam=560, uOffsetCam=560, vOffsetCam=440, refCameraMatrix=None, offsetCameraMatrix=None, xOffset=-100, yOffset=0, zOffset=0)