"""
Quick example which demonstrates using Scipy to calculate a median filter across a
numpy array.
"""
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
import matplotlib.cm as cm

in_raster = "./data/elevation.tif"

a = None
try:
    a = arcpy.RasterToNumPyArray(in_raster)
except:
    a = np.mean(plt.imread(in_raster, format="TIFF"), axis=2)

print a.shape
med_filtered = ndimage.filters.median_filter(a, size=9)

plt.subplot(211)
plt.imshow(a, cmap=cm.winter, origin="lower")
plt.title("Original")
plt.subplot(212)
plt.imshow(med_filtered, cmap=cm.winter, origin="lower")
plt.title("Filtered")
plt.show()
