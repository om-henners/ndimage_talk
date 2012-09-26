"""
An example of processing as an n-dimensional array.
"""
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from glob import glob

lsat = None
try:
    import arcpy
    lsat = np.dstack(arcpy.RasterToNumPyArray(in_raster)
                     for in_raster in glob("./data/lsat7_2002_*.tif"))
except:
    lsat = np.dstack(np.mean(plt.imread(in_raster, format="TIFF"), axis=2)
                     for in_raster in glob("./data/lsat7_2002_*.tif"))

print lsat.shape
median = ndimage.median_filter(lsat, size=9)
print median[:, :, 5].shape

plt.subplot(211)
plt.imshow(lsat[:, :, 5], cmap=plt.winter(), origin="lower")
plt.title("Original")
plt.subplot(212)
plt.imshow(median[:, :, 5], cmap=plt.winter(), origin="lower")
plt.title("Filtered")

plt.show()
