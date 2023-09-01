from osgeo import gdal
from osgeo import osr
import os

src_dset = r'E:\box_offline\small_projects\eklutna_d\2022_lidar\Eklutna2022_Topobathy_clip.tif'
dir_out = r'E:\box_offline\small_projects\eklutna_d\lu_clip_dem_20230810\clipped_dems\clipped_800ft_topobathy\test_lu'

src = osr.SpatialReference()
src.SetFromUserInput('EPSG:6335')
tgt = osr.SpatialReference()
tgt.SetFromUserInput('ESRI:102634')

# REsampling options
# CUBIC gdal.GRA_cubic
# NEAREST gdal.GRA_NearestNeighber
# BILINEAR gdal.GRA_Bilinear

fp_cutline = r'E:\box_offline\small_projects\eklutna_d\lu_clip_dem_20230810\clipped_dems\clipped_800ft\eklutna_river_crossing_800ft_bx_crossing7_2.shp'
shp_name = os.path.split(fp_cutline)[-1][:-4]
fld = 'Name'
sc_num = [1,2,3,4,5,6,7,8]

# for aerial imagery
sc_num =[1,2,3,4,5,6,7,8]
tiles = [9,8,8,7,6,6,5,5]
eklut_indices_dict =dict(zip(sc_num,tiles))
aerial_base_str = r'E:\box_offline\small_projects\eklutna_d\2022_lidar\2022_Eklutna_0'

ct = 0
for n in sc_num:
    tgt_val = 'SC {}'.format(n)
    sql_clause = "SELECT * FROM {} WHERE {} = '{}'".format(shp_name, fld, tgt_val)
    print(sql_clause)
    options = gdal.WarpOptions(resampleAlg=gdal.GRA_NearestNeighbour, format='GTiff', \
                               cutlineDSName=fp_cutline, cutlineLayer = shp_name, cropToCutline=True, cutlineSQL= sql_clause, \
                               srcSRS=src, dstSRS=tgt)
    vf = tgt_val.replace(' ','_')

    # # DEM tgt dset
    # fname = r'eklutna2022_topobathy_stream_nn_{}.tif'.format(vf)
    # tgt_dset = os.path.join(dir_out, fname)

    # Aerial tgt dset
    tile_num = eklut_indices_dict[n]
    src_dset = '{}{}.tif'.format(aerial_base_str, tile_num)
    tgt_dset = os.path.join(dir_out, '2022_Eklutna_Aerial_nn_{}.tif'.format(vf))
    print(src_dset)
    print(tgt_dset)
    gdal.Warp(tgt_dset, src_dset, options = options)
    ct+=1






