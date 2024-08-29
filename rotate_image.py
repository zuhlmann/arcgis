from PIL import Image, ImageOps
import pandas as pd
import os


# # A) Rotating Images for Photologs
# # 202408
# # CHECK
# # C:\Users\UhlmannZachary\Documents\staging\kokish_test
# # C:\Box\MCM Projects\Evolugen-Brookfield\2024 DSIs\5.0 Kokish DSI\6.0 GIS, Photos, and Notes\2024_field_maps
#
# csv = r"C:\Users\UhlmannZachary\Documents\staging\kokish_test\kokish_inspection_20240612_point_photo_log_COPY.csv"
# df = pd.read_csv(csv)
#
# fp_rotated=[]
# for index, row in df.iterrows():
#     if row['rotated']:
#         fp_photo = row['fp_photo']
#         subdir, fname_photo = os.path.split(row['fp_photo'])
#         fp_out = os.path.join(subdir, '{}_rotated.jpg'.format(fname_photo[:-4]))
#         fp_rotated.append(fp_out)
#         # Tinkered in python to get aspect ratio of original kokish photo (640, 360) using snippet found here
#         # https://stackoverflow.com/questions/59476757/python-3-x-pil-image-saving-and-rotating
#         # imfo = img._getexif()  or simply print the img after loading to get original size
#         img = Image.open(fp_photo)
#         img_270 = img.rotate(270, expand=True)
#         # Size determined from above tinkering to retain 640 heighth and aspect ratio to match orig (640,360) to get 1138
#         size = (1138,640)
#         # Padded from this: https://pillow.readthedocs.io/en/stable/reference/ImageOps.html#PIL.ImageOps.pad
#         ImageOps.pad(img_270,size,color='#FFFFFF').save(fp_out)
#     else:
#         # don't rotate --> save original
#         fp_rotated.append(row['fp_photo'])
# df['fp_photo_rotated']=fp_rotated
# df.to_csv(csv)

# B) Rotating geotiff ELA
# 20240828
# NOTE!! See georefernce_ela for function version and usage
import sys
sys.path.append('c:/users/uhlmann/code')
from osgeo import gdal

fp_tif = r"C:\Box\MCM Projects\Mainspring Conservation Trust\24-092 Ela Dam Removal PDB\4.0 Data Collection\Aerials\1VDUT00090009_georeferenced.tif"

import raster_from_array
import numpy as np

ds1 = gdal.Open(fp_tif)
arr_orig = ds1.ReadAsArray()
arr_new = np.rot90(np.rot90(np.rot90(arr_orig)))
gt = ds1.GetGeoTransform()
ul = (gt[0], gt[3])
res = [gt[1], gt[5]]
nd = 0
gdal_dtype = gdal.GDT_Float32
wkid = 4326
driver='GTiff'
fp_out = r"C:\Box\MCM Projects\Mainspring Conservation Trust\24-092 Ela Dam Removal PDB\4.0 Data Collection\Aerials\1VDUT00090009_georeferenced_rotated90.tif"
raster_from_array.numpy_array_to_raster(fp_out,
                          arr_new,
                          ul,
                          res,
                          nband = 1,
                          no_data = nd,
                          gdal_data_type = gdal_dtype,
                          spatial_reference_system_wkid = wkid,
                          driver = driver)