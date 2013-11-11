import numpy as np
import numpy.ma as ma
from scipy import ndimage
import time
try:
    import arcpy

    arcpy.CheckOutExtension("Spatial")
except:
    pass

#Function for generic filter
def variable_filter(in_arr, buf_size):
    process_data = np.reshape(in_arr, (buf_size * 2 + 1, buf_size * 2 + 1, 2))
    radius = process_data[buf_size, buf_size, 1] #get centrepoint of array
    try:
        #build a mask for our array
        z = get_circle(buf_size, radius)

        return ma.array(process_data[:, :, 0], mask=z).max()
        
    except Exception, e:
#        print e
        return np.NaN


#Functionto create the circle annulus in numpy
def get_circle(buf_size, radius):
    z = np.zeros((buf_size * 2 + 1, buf_size * 2 + 1)).astype('uint8')
    y, x = np.ogrid[1-radius: radius,1-radius: radius]
    index = x**2 + y**2 <= radius**2
    z[buf_size+1-radius:buf_size+radius,
      buf_size+1-radius:buf_size+radius][index] = 1
    return z

in_raster = None
in_mask = None

#Create some random data
try:
    a = arcpy.NumPyArrayToRaster(np.random.random((100, 100)))
    a_mask = arcpy.NumPyArrayToRaster(np.random.randint(0,5, (100, 100)))


#Test generic filter
    in_raster = arcpy.RasterToNumPyArray(a)
    in_mask = arcpy.RasterToNumPyArray(a_mask)
except:
    in_raster = np.random.random((100, 100))
    in_mask = np.random.randint(0, 5, (100, 100))

t0 = time.time()

combined = np.dstack((in_raster, in_mask))

max_buffer_size = np.max(in_mask)
out_arr = ndimage.filters.generic_filter(combined, variable_filter,
                                         (max_buffer_size * 2 + 1,
                                          max_buffer_size * 2 + 1, 2),
                                         mode="constant", cval=0,
                                         extra_arguments=(max_buffer_size,))
try:
    out_rast1 = arcpy.NumPyArrayToRaster(out_arr[:, :, 1])
except:
    pass
t1 = time.time()


#Test picking from maximum filter
try:
    in_raster = arcpy.RasterToNumPyArray(a)
    in_mask = arcpy.RasterToNumPyArray(a_mask)
except:
    in_raster = np.random.random((100, 100))
    in_mask = np.random.randint(0, 5, (100, 100))

max_filters = np.dstack([ndimage.filters.maximum_filter(in_raster,
                                                        footprint=get_circle(i, i),
                                                        mode="constant", cval=0)
    for i in np.unique(in_mask)])

out_arr2 = np.take(max_filters, in_mask)
t2 = time.time()

import matplotlib.pyplot as plt

plt.imshow(out_arr2, origin="lower", cmap="winter")
plt.show()

try:
    #Test arcpy inbuilt functions
    out_stack = [arcpy.sa.FocalStatistics(a, arcpy.sa.NbrCircle(i, "CELL"), "MAXIMUM","DATA") for i in xrange(5)]
    out_rast3 = arcpy.sa.Pick(a_mask, out_stack)
except:
    pass
t3 = time.time()

print t1 - t0, t2 - t1 #, t3 - t2
