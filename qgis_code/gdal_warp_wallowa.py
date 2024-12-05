from osgeo import osr,gdal
import os
import subprocess
import copy
# import pandas as pd

# 20240531
# Multiple files: ~ 10 same everything; 4 diff proj; 2 diff projection and spatial res
# tiffs Initially converted from arcgrid wihch were downloaded from usgs:
# C:\Box\MCMGIS\Project_Based\Wallowa_Dam\Map\wallowa_dam

base_dir = r'C:\Users\UhlmannZachary\Documents\staging\CONVERTED_zu'
out_dir = r'C:\Users\UhlmannZachary\Documents\staging\CONVERTED_zu\projected'

df = pd.read_csv(r"C:\Box\MCMGIS\Project_Based\Wallowa_Dam\Map\wallowa_dam\input_grid_files2.csv")
df_subset = df.iloc[6:]
for idx, row in df_subset.iterrows():
    # Translate WITH reprojection - for the smaller tiles
    srs_in = row['SRS_Code']
    src = osr.SpatialReference()
    src.SetFromUserInput('EPSG:{}'.format(int(srs_in)))

    tgt = osr.SpatialReference()
    f = open(r'C:\Users\UhlmannZachary\Documents\staging\NAD_1983_2011_Oregon_Statewide_Lambert_Feet_Intl.prj', 'r')
    out_proj = f.read()
    tgt.SetFromUserInput(out_proj)

    options = gdal.WarpOptions(resampleAlg=gdal.GRA_Cubic, xRes = 3, yRes=3, \
                               srcSRS=src, dstSRS=tgt, dstNodata=-9999)
    src_dset = os.path.join(base_dir, row['fname_out'])
    tgt_dset = os.path.join(out_dir, r'{}_OR_lambert.tif'.format(os.path.splitext(row['fname_out'])[0]))
    gdal.Warp(tgt_dset, src_dset, options=options)
    print(tgt_dset)

    # Translate withOUT reprojection (just new noData)
    options = gdal.WarpOptions(resampleAlg=gdal.GRA_Cubic, xRes=3, yRes=3, \
                               dstNodata=-9999)
    src_dset = os.path.join(base_dir, row['fname_out'])
    tgt_dset = os.path.join(out_dir, r'{}_noData.tif'.format(os.path.splitext(row['fname_out'])[0]))
    gdal.Warp(tgt_dset, src_dset, options=options)
#     print(tgt_dset)


# # GDAL_calc to convert Z to feet
# # MOTE!! Error - regarding somehing with string parsing in subprocesses call.  resorted to manual
# # DID NOT WORK - but fixable
# gdal_path = r'C:\Users\UhlmannZachary\anaconda3\envs\gdal_env\Scripts'
# gdal_calc_path = os.path.join(gdal_path, 'gdal_calc.py')
#
# # Arguements.
# base_dir = r'C:\Users\UhlmannZachary\Documents\staging\CONVERTED_zu\projected'
# file_list = r'C:\Users\UhlmannZachary\Documents\staging\CONVERTED_zu\projected\2008_2009_data2.txt'
#
# with open(file_list, 'r') as files:
#     for line in files:
#         fname_in = copy.copy(line)
#         file_in = os.path.join(base_dir, fname_in)
#         fname_out = r'{}_feet.tif'.format(os.path.splitext(file_in)[0])
#         file_out = os.path.join(base_dir, fname_out)
#         calc_expr = '"A*3.28084"'
#         nodata = '-9999'
#         typeof = '"Float32"'
#
#         # Generate string of process.
#         gdal_calc_str = 'python {0} -A {1} --outfile={2} --calc={3} --NoDataValue={4} --type={5}'
#         gdal_calc_process = gdal_calc_str.format(gdal_calc_path, fname_in,
#             file_out, calc_expr, nodata, typeof)
#
#         # Call process.
#         print(gdal_calc_process)
#         subprocess.run(gdal_calc_process, shell=True)
