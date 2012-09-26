"""
Example code to conver raster (image) data to numpy arrays
"""
import numpy as np

in_raster = "elevation.tif"

#Read a raster into a Numpy array with ArcGIS 10
import arcpy
a = arcpy.RasterToNumPyArray(in_raster)


#We can use matplotlib.pylot.imread and Image to read any image associated with PIL
#Note here though we're not going to be able to get coordinate information
import matplotlib.pyplot as plt
import Image
a = plt.imread(in_raster, format="TIFF")

#The most common open source alternative to arcpy is GDAL for raster processing (OGR
#for vectors)
#Using GDAL we can access crs information for the raster
from osgeo import gdal
from osgeo import gdalconst
dataset = gdal.Open(in_raster, gdalconst.GA_ReadOnly)
band = dataset.GetRasterBand(1) #Bands start from 1 in GDAL to conform with the
                                #standard convention based on landsat (i.e. band
                                #1 corresponds with landsat band 1)
a = band.ReadAsArray()
