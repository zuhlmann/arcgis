import copy
from osgeo import gdal
import numpy as np
# import scipy as sp
# import scipy.ndimage
# import raster_from_array
# import matplotlib.pyplot as plt
#
# # 20220909 For Gaussian Filtering a DEM at Swancove and then resaving as Tif
#
# fp_in = r'D:\box_offline\small_projects\eklutna_d\lidar_geomorph\2015_dem_warped_gdal.tif'
#
# ds1 = gdal.Open(fp_in)
# arr_orig = ds1.ReadAsArray()
# # NOTE!! this will destroy values less than -9998.  Will work on -3.28 e ... and -9999.  Terrible Hack
# arr_orig[arr_orig<-9998] = np.nan
# arr_orig = arr_orig *
#
# arr_in = copy.copy(arr4)
# fp_out = r'C:\Users\uhlmann\Documents\urisa_conference_2022\data_maps\data\raster\USGS_13_n45w117_20220309_clip_guass_sigma2.tif'
# gt = ds1.GetGeoTransform()
# ul = (gt[0], gt[3])
# res = gt[1]
# nd = -9999
# gdal_dtype = gdal.GDT_Float32
# wkid = 4502
# wkid = 4269
# driver = 'GTiff'
# print(ul)
# print(res)
# raster_from_array.numpy_array_to_raster(fp_out,
#                   arr_in,
#                   ul,
#                   res,
#                   nband = 1,
#                   no_data = nd,
#                   gdal_data_type = gdal_dtype,
#                   spatial_reference_system_wkid = wkid,
#                   driver = driver,
#                   raster_with_projection = fp_in)
#
#
# # https://gis.stackexchange.com/questions/164853/reading-modifying-and-writing-a-geotiff-with-gdal-in-python
# # source_prj = r'D:\box_offline\swancove_2022\backbarrier_20220314\rasters\sc_bathwithsurf_barrier_20220331_step3.tif'
# # ds = gdal.Open(source_prj)
# # [rows, cols] = arr4.shape
# # driver = gdal.GetDriverByName("GTiff")
# # outdata = driver.Create(fp_out, cols, rows, 1, gdal.GDT_Float32)
# # outdata.SetGeoTransform(ds.GetGeoTransform())##sets same geotransform as input
# # outdata.SetProjection(ds.GetProjection())##sets same projection as input
# # outdata.GetRasterBand(1).WriteArray(arr4)
# # outdata.GetRasterBand(1).SetNoDataValue(-9999)##if you want these values transparent
# # outdata.FlushCache() ##saves to disk!!
# # outdata = None
# # band=None
# # ds=None
# # print(ds.GetGeoTransform())


def pt_from_raster(raster_src, shp_pt, csv_out):
    csv = r'C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\Cultural_Resources\CUL2_data\GLO_direct\gcs_7N_15E.csv'

    src_ds = gdal.Open(raster_src)
    gt_forward = src_ds.GetGeoTransform()
    gt_reverse = gdal.InvGeoTransform(gt_forward)
    ds = ogr.Open(shp_pt)
    lyr = ds.GetLayer()

    rb = src_ds

    li_values = list()
    x_coords = []
    y_coords = []
    col_num = []
    row_num = []
    id_list = []
    desc_list = []
    TR_list = []
    for feat in lyr:
        geom = feat.GetGeometryRef()
        feat_id = feat.GetField('id')
        desc = feat.GetField('desc')
        mx, my = geom.GetX(), geom.GetY()
        print(feat_id, mx, my)
        gt = gt_reverse
        px = int((mx - gt[0]) / gt[1])
        py = int((my - gt[3]) / gt[5])
        col_num.append(abs(px))
        row_num.append(abs(py))
        x_coords.append(round(mx))
        y_coords.append(round(my))
        id_list.append(feat_id)
        desc_list.append(desc)
        TR_list.append(TR)
        if vals:
            intval = rb.ReadAsArray(px, py, 1, 1)
            # if needing values (i.e. raster values like elevatiohn)
            # https://gis.stackexchange.com/questions/46893/getting-pixel-value-of-gdal-raster-under-ogr-point-without-numpy#comment428498_46898
            # https://gis.stackexchange.com/questions/269603/extract-raster-values-from-point-using-gdal
            li_values.append([feat_id, intval[0]])
        else:
            pass
        col_stack = np.column_stack([id_list, desc_list, col_num, row_num, x_coords, y_coords])
        df = pd.DataFrame(col_stack, columns=['id', 'desc', 'col_num', 'row_num', 'x_coord', 'y_coord'])
    df.to_csv(csv_out)

raster_src=r"C:\Box\MCM Projects\MCWRA\25-001_San Antonio Spillway Design\6.0 Plans and Specs\6.4 Design\6.4.4 Hydraulics\2025 PMF update\Gridded Rainfall\2023\KHNX_N1P_20230110_175100.nc"
shp_pt=r"C:\Box\MCM Projects\MCWRA\25-001_San Antonio Spillway Design\6.0 Plans and Specs\6.4 Design\6.4.4 Hydraulics\2025 PMF update\IDW_Precip\base_data\san_antonio_rain_gages.shp"
csv_out=r'C:\Users\ZacharyUhlmann\Documents\staging\sanantonio_pt_raster'

pt_from_raster(raster_src, shp_pt, csv_out)

