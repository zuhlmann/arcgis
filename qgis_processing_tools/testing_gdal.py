
from osgeo import gdal
from osgeo import osr
import copy


ot = 'GTiff'
vals = [1,2,3]
fp_cutline=r"C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\Imagery\naip_clip_box_cutslopes.shp"
shp_name = os.path.split(fp_cutline)[-1][:-4]
shp_name = 'naip_clip_box_cutslopes'
fp_raster =r"C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\Imagery\Mokelumne_NAIP_merged.tif"
name_field='dissolve'
output_dir = r'C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\Imagery'

from osgeo import osr
src = osr.SpatialReference()
src.SetFromUserInput('EPSG:26910')
tgt = osr.SpatialReference()
tgt.SetFromUserInput('ESRI:26910')
for v in vals:
    sql_clause = "SELECT * FROM {} WHERE {} = '{}'".format(shp_name, name_field, v)
    options = gdal.WarpOptions(resampleAlg=gdal.GRA_NearestNeighbour, format=ot, \
                               cutlineDSName=fp_cutline, cutlineLayer=shp_name,
                               cropToCutline=True, cutlineSQL=sql_clause, \
                               srcSRS='EPSG:26910', dstSRS=R'EPSG:26910')
    print(v)
    src_dset = copy.copy(fp_raster)
    basename = os.path.split(fp_raster)[-1]
    basename = basename.split('.')[0]
    tgt_dset = os.path.join(output_dir, '{}_{}_{}.tif'.format(basename, name_field, v))
    src_dset = r"C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\Imagery\Mokelumne_NAIP_merged.tif"
    gdal.Warp(tgt_dset, src_dset, options=options)