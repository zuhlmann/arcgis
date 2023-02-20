import copy
from osgeo import gdal
import numpy as np
import scipy as sp
import scipy.ndimage
import raster_from_array
import matplotlib.pyplot as plt

# 20220909 For Gaussian Filtering a DEM at Swancove and then resaving as Tif

fp_in = r'D:\box_offline\small_projects\eklutna_d\lidar_geomorph\2015_dem_warped_gdal.tif'

ds1 = gdal.Open(fp_in)
arr_orig = ds1.ReadAsArray()
# NOTE!! this will destroy values less than -9998.  Will work on -3.28 e ... and -9999.  Terrible Hack
arr_orig[arr_orig<-9998] = np.nan
arr_orig = arr_orig *

arr_in = copy.copy(arr4)
fp_out = r'C:\Users\uhlmann\Documents\urisa_conference_2022\data_maps\data\raster\USGS_13_n45w117_20220309_clip_guass_sigma2.tif'
gt = ds1.GetGeoTransform()
ul = (gt[0], gt[3])
res = gt[1]
nd = -9999
gdal_dtype = gdal.GDT_Float32
wkid = 4502
wkid = 4269
driver = 'GTiff'
print(ul)
print(res)
raster_from_array.numpy_array_to_raster(fp_out,
                          arr_in,
                          ul,
                          res,
                          nband = 1,
                          no_data = nd,
                          gdal_data_type = gdal_dtype,
                          spatial_reference_system_wkid = wkid,
                          driver = driver,
                          raster_with_projection = fp_in)


# https://gis.stackexchange.com/questions/164853/reading-modifying-and-writing-a-geotiff-with-gdal-in-python
# source_prj = r'D:\box_offline\swancove_2022\backbarrier_20220314\rasters\sc_bathwithsurf_barrier_20220331_step3.tif'
# ds = gdal.Open(source_prj)
# [rows, cols] = arr4.shape
# driver = gdal.GetDriverByName("GTiff")
# outdata = driver.Create(fp_out, cols, rows, 1, gdal.GDT_Float32)
# outdata.SetGeoTransform(ds.GetGeoTransform())##sets same geotransform as input
# outdata.SetProjection(ds.GetProjection())##sets same projection as input
# outdata.GetRasterBand(1).WriteArray(arr4)
# outdata.GetRasterBand(1).SetNoDataValue(-9999)##if you want these values transparent
# outdata.FlushCache() ##saves to disk!!
# outdata = None
# band=None
# ds=None
# print(ds.GetGeoTransform())
