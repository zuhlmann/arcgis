from osgeo import gdal
from osgeo import osr

src_dset = r'D:\box_offline\small_projects\eklutna_d\lidar_geomorph\2015_dem_clipped.tif'
tgt_dset = r'D:\box_offline\small_projects\eklutna_d\lidar_geomorph\2015_dem_warped_gdal.tif'

src = osr.SpatialReference()
src.SetFromUserInput('ESRI:102634')
tgt = osr.SpatialReference()s
tgt.SetFromUserInput('EPSG:6335')

extents = [368000,396200,6799000,6818000]
options = gdal.WarpOptions(xRes=0.5, yRes = 0.5, resampleAlg = gdal.GRA_Cubic, targetAlignedPixels=True, \
                srcSRS = src, dstSRS = tgt,)

gdal.Warp(tgt_dset, src_dset, options = options)




