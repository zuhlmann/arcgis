from osgeo import gdal
from osgeo import osr
import os
import copy

src_dset = r'E:\box_offline\projects\graip\USGS_1M_DEM_2019_mosaic_ft.tif'
# src_dset = r'E:\box_offline\small_projects\eklutna_d\2022_lidar\EklutnaRiver_BE_DEM_UTM6.tif'
dir_out = r'E:\box_offline\projects\graip\clips\buffered'

src = osr.SpatialReference()
src.SetFromUserInput('EPSG:6418')
tgt = osr.SpatialReference()
tgt.SetFromUserInput('EPSG:6418')

# REsampling options
# CUBIC gdal.GRA_cubic
# NEAREST gdal.GRA_NearestNeighber
# BILINEAR gdal.GRA_Bilinear

fp_cutline = r'E:\box_offline\projects\graip\sheets_alignments_CASP2_buff200ft_square.shp'
fp_cutline = r"E:\box_offline\projects\graip\sheets\full_sheets\mokelumne_roads_cad_buff100.shp"
shp_name = os.path.split(fp_cutline)[-1][:-4]
fld = 'FID'
sc_num = [2]

ot = 'GTiff'
# ot = 'JPEG'
ext = {'GTiff':'tif','JPEG':'jpg'}
ext = ext[ot]

ct = 1
for n in sc_num:
    tgt_val = copy.copy(n)
    sql_clause = "SELECT * FROM {} WHERE {} = '{}'".format(shp_name, fld, tgt_val)
    sql_clause = "SELECT * FROM {} WHERE {} = {}".format(shp_name, fld, tgt_val)
    options = gdal.WarpOptions(resampleAlg=gdal.GRA_NearestNeighbour, format=ot,\
                               cutlineDSName=fp_cutline, cutlineLayer = shp_name, \
                               cropToCutline=True, cutlineSQL= sql_clause)

    # vf = tgt_val.replace('kml','sheet')
    vf = 'FID_{}'.format(n)
    vf = 'RD_8N40'

    # DEM tgt dset
    fname = r'USGS_UpperSouthAmerican_Eldorado_2019_nn_{}_CA_SP2_ft.tif'.format(vf)
    tgt_dset = os.path.join(dir_out, fname)
    print(n)
    gdal.Warp(tgt_dset, src_dset, options = options)








