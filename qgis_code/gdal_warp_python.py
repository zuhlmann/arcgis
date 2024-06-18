from osgeo import gdal
from osgeo import osr
import os
import pandas as pd

# src_dset = r'E:\box_offline\small_projects\eklutna_d\2022_lidar\Eklutna2022_Topobathy_clip.tif'
# # src_dset = r'E:\box_offline\small_projects\eklutna_d\2022_lidar\EklutnaRiver_BE_DEM_UTM6.tif'
# dir_out = r'E:\box_offline\small_projects\eklutna_d\lu_clip_dem_20230810\clipped_aerials\jpg'
#
src = osr.SpatialReference()
src.SetFromUserInput('EPSG:6335')
tgt = osr.SpatialReference()
tgt.SetFromUserInput('ESRI:102634')
#
# # REsampling options
# # CUBIC gdal.GRA_cubic
# # NEAREST gdal.GRA_NearestNeighber
# # BILINEAR gdal.GRA_Bilinear
#
# fp_cutline = r'E:\box_offline\small_projects\eklutna_d\lu_clip_dem_20230810\clipped_dems\clipped_800ft\eklutna_river_crossing_800ft_bx_crossing7_2.shp'
# shp_name = os.path.split(fp_cutline)[-1][:-4]
# fld = 'Name'
# sc_num = [1,2,3,4,5,6,8,99]
#
# # for topo
# sc_num =[99]
#
# # for aerial
# sc_num =[1,2,3,4,5,6,99,99,8]
# tiles = [9,8,8,7,6,6,6,5,5]
# sc_num = [8]
# tiles=[5]
# eklut_indices_dict =dict(zip(sc_num,tiles))
# aerial_base_str = r'E:\box_offline\small_projects\eklutna_d\2022_lidar\2022_Eklutna_0'
# # ot = 'GTiff'
# ot = 'JPEG'
# ext = {'GTiff':'tif','JPEG':'jpg'}
# ext = ext[ot]

# ct = 0
# for n in sc_num:
#     tgt_val = 'SC {}'.format(n)
#     sql_clause = "SELECT * FROM {} WHERE {} = '{}'".format(shp_name, fld, tgt_val)
#     options = gdal.WarpOptions(resampleAlg=gdal.GRA_NearestNeighbour, format=ot,\
#                                cutlineDSName=fp_cutline, cutlineLayer = shp_name, cropToCutline=True, cutlineSQL= sql_clause, \
#                                srcSRS=src, dstSRS=tgt, )
#
#     options_translate = gdal.TranslateOptions(format=ot, bandList=[1, 2, 3], \
#                                               creationOptions=["WORLDFILE=YES"])
#
#     vf = tgt_val.replace(' ','_')
#
#     # # DEM tgt dset
#     # fname = r'eklutna2022_topobathy_stream_nn_{}.tif'.format(vf)
#     # # fname = r'eklutna2020_BE_nn_{}.tif'.format(vf)
#     # tgt_dset = os.path.join(dir_out, fname)
#
#     # Aerial tgt dset
#     tile_num = eklut_indices_dict[n]
#     src_dset = '{}{}.tif'.format(aerial_base_str, tile_num)
#     tgt_dset = os.path.join(dir_out, '2022_Eklutna_Aerial_nn_{}_tile{}.{}'.format(vf,n,ext))
#     print(src_dset)
#     print(tgt_dset)
#
#     # gdal.Warp(tgt_dset, src_dset, options = options)
#     gdal.Translate(tgt_dset, src_dset, options = options_translate)
#     ct+=1

# ot = 'GTiff'
ot = 'JPEG'
ext = {'GTiff':'tif','JPEG':'jpg'}
# ext = ext[ot]
# substr =['1','2','3','4','5','5_tile7','6','8','99','99_tile5']
# substr =['1','2','3','4','5','5_tile7','6','8','99','99_tile5']
# # TRANSLATE
# aerial_base_str = r"E:\box_offline\small_projects\eklutna_d\lu_clip_dem_20230810\clipped_aerials\2022_Eklutna_Aerial_nn_SC_"
# for sb in substr:
#     options_translate = gdal.TranslateOptions(format=ot, bandList=[1, 2, 3], \
#                                               creationOptions=["WORLDFILE=YES"])
#
#     vf = tgt_val.replace(' ', '_')
#
#     # Aerial tgt dset
#     tile_num = eklut_indices_dict[n]
#     src_dset = '{}{}.tif'.format(aerial_base_str, sb)
#     tgt_dset = os.path.join(dir_out, '2022_Eklutna_Aerial_nn_SC_{}.{}'.format(sb, ext))
#     print(src_dset)
#     print(tgt_dset)
#
#     # gdal.Warp(tgt_dset, src_dset, options = options)
#     gdal.Translate(tgt_dset, src_dset, options=options_translate)
#     ct += 1

dir_out = r'C:\Box\MCMGIS\GIS_Data\tutorials\qgis_processing_tools\gdal_utils_mosaics\tiles'
ext='tif'
df=pd.read_csv(r"C:\Box\MCM USERS\3.0 - Employees\zuhlmann\qgis_utils\staging2\tutorial_data_reproject.csv")
df=df.iloc[:-1]
df['FNAME']=[os.path.split(fp)[-1][:-4] for fp in df.LOCATION]
for idx,row in df.iterrows():
    options_warp = gdal.WarpOptions(resampleAlg=gdal.GRA_Average,xRes=15,yRes=15,format='GTiff')
    src_dset = row['LOCATION']
    tgt_dset = os.path.join(dir_out, '{}_15ft.{}'.format(row['FNAME'], ext))
    print(src_dset)
    print(tgt_dset)

    gdal.Warp(tgt_dset, src_dset, options=options_warp)







