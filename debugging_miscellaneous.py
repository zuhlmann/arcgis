#  DETERMINE mxd version
# https://gis.stackexchange.com/questions/62090/using-arcpy-to-determine-arcmap-document-version
import os
import glob
import sys
sys.path.append('c:/Users/uhlmann/code')
import utilities

# ESRI  ---> set python exe (ctl Alt S; settings, find in list)
# # 1_esri) GET ARC VERSION for mxd
# 20241022
# import mxd_utiltiies
# folder = r'C:\Users\UhlmannZachary\Documents\staging\testing'
# mxdFiles = glob.glob(os.path.join(folder, '*.mxd'))
# for mxdFile in mxdFiles:
#     fileName = os.path.basename(mxdFile)
#     version = mxd_utiltiies.getMXDVersion(mxdFile)
#     print(version, fileName)

# # 2_esri) INVENTORY MXD
# # 20241022
# base_dir=r'C:\Box\MCMGIS\Project_Based\Nuyakuk_Hydro\Maps\ISR_Maps'
# utilities.mxd_inventory_csv(base_dir, 'ISR_mxd_layer_inv.csv')

# Inventory Dir
# INVENTORY DIRECTORY
# 20240722
# from cowlitz_dbase notebook
sys.path.append('c:/users/uhlmann/code')
import importlib
import utilities_oop
importlib.reload(sys.modules['utilities'])
importlib.reload(sys.modules['utilities_oop'])
import pandas as pd
import copy

tc = 'DATA_LOCATION_MCMILLEN'
parent_dir = r"C:\Box\MCM Projects\Klamath River Renewal Corp\4.0 Data Collection\Crescent City Harbor Data\Unzipped Files"
csv_lyt_inv = r"C:\Box\MCM Projects\Klamath River Renewal Corp\4.0 Data Collection\Crescent City Harbor Data\Unzipped Files\unzipped_files_inventory.csv"
subdir_inv_obj = utilities_oop.utilities(parent_dir, tc)

# # a) no filetype filter
# subdir_inv_obj.subdir_inventory(new_inventory = csv_lyt_inv)

# # b) filetype fileter
# ft_filt = ['.gdb','.cpg','.dbf','.idx','.shx','.xml','.shp','.ipynb']
# exclude_sd = ['archive','backups','aprx_inventories']
# subdir_inv_obj.subdir_inventory(ft_filt, exclude_sd, new_inventory = csv_lyt_inv)

# # b2) filter filetype
# projects = ['geosyntec_pad_H20_p2', 'recreation_PAD_p2','SFT_common_maps','terrrestrial_PAD']
# subdir = r'C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\sharepoint\templates\SCL_data_package_devel\map_documents\{}\{}'
# project_dir = [r'Index', r'GpMessages']
# exclude_sd = [os.path.normpath(subdir.format(pn, prd)) for pn in projects for prd in project_dir]
# exclude_sd.append(r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\sharepoint\templates\SCL_data_package_devel\map_documents\backups")
# subdir_inv_obj.subdir_inventory(ft_filt, exclude_sd, new_inventory = csv_lyt_inv)

# # Klamath Buoys ADD search_str
# buoy_str = [f"buoy_{v}" for v in list(range(14))]
# buoy_str2 = [f"buoy{v}" for v in list(range(14))]
# buoy_str.extend(buoy_str2)
# df = pd.read_csv(csv_lyt_inv)
# df['BUOY'] = df['BUOY'].astype(str)
# for idx in df.index:
#     for buoy in buoy_str:
#         if buoy in df.loc[idx, 'ITEM']:
#             t = copy.copy(buoy)
#             t = t.replace('buoy_','').replace('buoy','')
#             df.at[idx, 'BUOY'] = t
# df.to_csv(csv_lyt_inv)

# Klamath Buoys cont..
# 20241022 Aggregate Rows
df = pd.read_csv(csv_lyt_inv)
csv_folders = r'C:\Box\MCM Projects\Klamath River Renewal Corp\4.0 Data Collection\Crescent City Harbor Data\Unzipped Files\unzipped_folders_buoyID.csv'
subdir_inv_obj.aggregate_rows(csv_lyt_inv, csv_folders, 'FINAL_SUBDIR', 'BUOY', data_type='integer')