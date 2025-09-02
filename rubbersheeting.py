from math import floor
from osgeo import gdal,ogr
import struct
import numpy as np
import pandas as pd

# Rubbersheeting
# ZU 20230601
# Note 20250828 - copied from:
# C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\Cultural_Resources\CUL2_data\GLO_direct\processing_points_mokelumne.py
# CHECK PARENT DIR OF ABOVE BASE PATH IN MOKELUMNE for README (instructions on gdal calls to georegister)

# STEP1 make corresponding tie points on both images
# a) Create shapefiles of points (one for georeferenced aerial imagery or whatever real locs
# and one for the drawing pulled in as a tiff
# b) Save drawing PDF (if pdf) to tif, then georerence with right click --> save to new image
# c) Save both dataframes (did not show save step) | Then use col row from drawing and easting northing
# from actual coords to forumate gdal callstats
vals = False

# MOKELUMNE
GLO_7N_15E = r"C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\Cultural_Resources\CUL2_data\GLO_direct\CA210070N0150E00001_CAII.tif"
GLO_8N_15E  = r"C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\Cultural_Resources\CUL2_data\GLO_direct\CA210080N0150E00002_clipped_projected.tif"
src_filename = GLO_7N_15E
shp_filename = r"C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\Cultural_Resources\CUL2_data\digitized\GLO_T7_R14_map_ref_pts_NAD83_CAII_ft.shp"
csv=r'C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\Cultural_Resources\CUL2_data\GLO_direct\gcs_7N_15E.csv'

# CHIGNIK
# 20250828
src_filename = r"C:\Box\MCMGIS\Project_Based\ANTHC\chignik\data\vector\field_map\rubbersheet\chignik_site_map_projected_AKSP6.tif"
shp_filename = r"C:\Box\MCMGIS\Project_Based\ANTHC\chignik\data\vector\field_map\chignik_conceptual_plan_georegistering_pts_src_AKSP6.shp"
csv = r"C:\Box\MCMGIS\Project_Based\ANTHC\chignik\data\vector\field_map\rubbersheet\gcs_chignik_site_map_AKSP6.csv"

# src_ds=gdal.Open(src_filename)
# gt_forward=src_ds.GetGeoTransform()
# gt_reverse=gdal.InvGeoTransform(gt_forward)
# ds=ogr.Open(shp_filename)
# lyr=ds.GetLayer()
#
# rb = src_ds
#
# li_values = list()
# x_coords = []
# y_coords = []
# col_num = []
# row_num = []
# id_list=[]
# desc_list=[]
# for feat in lyr:
#    geom = feat.GetGeometryRef()
#    feat_id = feat.GetField('id')
#    desc = feat.GetField('desc')
#    mx, my = geom.GetX(), geom.GetY()
#    print(feat_id, mx, my)
#    gt=gt_reverse
#    px = int((mx - gt[0]) / gt[1])
#    py = int((my - gt[3]) / gt[5])
#    col_num.append(abs(px))
#    row_num.append(abs(py))
#    x_coords.append(round(mx))
#    y_coords.append(round(my))
#    id_list.append(feat_id)
#    desc_list.append(desc)
#    if vals:
#       intval = rb.ReadAsArray(px, py, 1, 1)
#       # if needing values (i.e. raster values like elevatiohn)
#       #https://gis.stackexchange.com/questions/46893/getting-pixel-value-of-gdal-raster-under-ogr-point-without-numpy#comment428498_46898
#       # https://gis.stackexchange.com/questions/269603/extract-raster-values-from-point-using-gdal
#       li_values.append([feat_id, intval[0]])
#    else:
#       pass
#    col_stack = np.column_stack([id_list,desc_list,col_num,row_num,x_coords,y_coords])
#    df = pd.DataFrame(col_stack, columns = ['id','desc_list','col_num','row_num','x_coord','y_coord'])
# df.to_csv(csv)

# Step 2 Call in gdal
# a) Creating the gdal_translate substring
df2= pd.read_csv(csv)
sub = df2[['col_num','row_num','easting','northing']]
substr = []
for idx in df2.index:
   t1=[]
   t1.append(int(df2.loc[idx, 'col_num']))
   t1.append(int(df2.loc[idx, 'row_num']))
   t1.append(df2.loc[idx, 'easting'])
   t1.append(df2.loc[idx, 'northing'])
   t1 = [str(r) for r in t1]
   substr.append(' '.join(t1))
full_str = ' -gcp '.join(substr)
print(full_str)

# FORMAT AND CALL IN CLI - note two consecutive calls
# b) gdal_translate -gcp 507 482 6246215 2268541 -gcp 1594 289 6246103 2268561 -gcp 3000 674 6245981 2268666 test_projected.tif test_projected_gcp_3pts.tif
# c) gdalwarp -order 1 test_projected_gcp_3pts.tif test_projected_gcp_3pts_warped.tif

    


   