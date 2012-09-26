import numpy
from scipy.ndimage import generic_filter

import matplotlib.pyplot as plt
from numpy import ma


def calc_slope(in_filter, x_cellsize, y_cellsize):
    #slope calculation here - note need to reshape in array to be 3*3
    if 0.0 in in_filter:
        return -9999
    else:
        [a, b, c, d, e, f, g, h, i] = in_filter
    
        dz_dx = ((c + 2*f + i) - (a + 2 * d + g)) / (8 * x_cellsize)
        dz_dy = ((g + 2*h + i) - (a + 2 * b + c)) / (8 * y_cellsize)
        slope = numpy.sqrt(dz_dx ** 2 + dz_dy**2)
    
        return numpy.degrees(slope)


def get_array(f):
    try:
        import arcpy
        r = arcpy.Raster(f)
        return RasterToNumPyArray(r), r.meanCellWidth, r.meanCellHeight
    except:
        from osgeo import gdal
        from osgeo import gdalconst
        dataset = gdal.Open(f)
        band = dataset.GetRasterBand(1)
        #Now we read the data as a numpy array
        rast_data = band.ReadAsArray()
        rast_data = rast_data.astype(numpy.float)
        return rast_data, band.XSize, band.YSize
    

def main():
    #Get the raster from the disk
    rast_data, x_cellsize, y_cellsize = get_array("./data/elevation.tif")

    slope = generic_filter(rast_data, calc_slope, size=3, extra_arguments=(x_cellsize, y_cellsize))

    plt.imshow(ma.masked_equal(slope, -9999), cmap=plt.winter(), origin="lower")
    plt.show()

if __name__ == "__main__":
    main()
