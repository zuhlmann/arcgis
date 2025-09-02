import os
import pandas as pd
import sys
import arcpy
import copy
sys.path.append('c:/users/uhlmann/code')
sys.path.append('c:/users/uhlmann/code/arcpy_script_tools_uhlmann')
import importlib

# DATA MANAGEMENT PATHS2
fp_pathlist = r'C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\df_utility_csvs\path_list_updated.csv'
pl = pd.read_csv(fp_pathlist, index_col = 'gdb_str')
fp_offline = r'C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\df_utility_csvs\offline_lookup_table.csv'
olt = pd.read_csv(fp_offline, index_col = 'gdb_str')
prj_dir = r'C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\prj_files'

subproject = 'PSP_2024_2'

gdb_str = '{}_gdb'.format(subproject)
gdb_pro = pl.loc[gdb_str, 'fp_gdb']
prj_file = os.path.join(prj_dir, pl[pl.subproject == subproject].prj_file.values[0])

# TOLT
import spyder_arcgis_oop as agolZ
importlib.reload(sys.modules['utilities'])
importlib.reload(sys.modules['spyder_arcgis_oop'])
agol_obj = agolZ.commonUtils()
agol_obj.dbase_init(prj_file,subproject,fp_pathlist, use_item_desc=False)

# # INDICES
# agol_obj.selection_idx('df', indices = [18])
agol_obj.selection_idx('df', target_action= 'delete_psp2_test')

print('nothing')

agol_obj.take_action('df', 'delete', target_col = 'DATA_LOCATION_MCMILLEN',
                     dry_run = True, save_df = False,
                     offline_source=False, offline_target=False)

