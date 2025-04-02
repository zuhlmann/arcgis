import os
import pandas as pd
import sys
sys.path.append('c:/users/uhlmann/code')
sys.path.append('c:/users/uhlmann/code/arcpy_script_tools_uhlmann')
import importlib

# DATA MANAGEMENT PATHS2
fp_pathlist = r'C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\df_utility_csvs\path_list_updated.csv'
pl = pd.read_csv(fp_pathlist, index_col = 'gdb_str')
fp_offline = r'C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\df_utility_csvs\offline_lookup_table.csv'
olt = pd.read_csv(fp_offline, index_col = 'gdb_str')
prj_dir = r'C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\prj_files'

def ol_translate(fp_current, gdb_str, offline):
    offline_base, online_base = olt.loc[gdb_str, 'offline'], olt.loc[gdb_str, 'online']
    fp_current = os.path.normpath(fp_current)
    if offline:
        print('there')
        fp_out = fp_current.replace(online_base, offline_base)
    else:
        print('here')
        fp_out = fp_current.replace(offline_base, online_base)
    return(fp_out)

idx = -1
offline = False

subproject = 'PSP_2024'

# non_klamath
gdb_str_dict = {r'easements': 'easements_RH_gdb',
                'kauai': 'kauai_offline_gdb'}
try:
    gdb_str = gdb_str_dict[subproject]
except KeyError:
    gdb_str = '{}_gdb'.format(subproject)
gdb_pro = ol_translate(pl.loc[gdb_str, 'fp_gdb'], gdb_str, offline)
prj_file = os.path.join(prj_dir, pl[pl.subproject == subproject].prj_file.values[0])

# TOLT
import spyder_arcgis_oop as agolZ
importlib.reload(sys.modules['utilities'])
importlib.reload(sys.modules['spyder_arcgis_oop'])
agol_obj = agolZ.commonUtils()
agol_obj.dbase_init(prj_file,subproject,fp_pathlist, use_item_desc=False)

# # INDICES
# agol_obj.selection_idx('df', indices = [18])
agol_obj.selection_idx('df', target_action= 'rename')
for i, n in zip(agol_obj.indices_iloc, agol_obj.indices):
    print('{}:  {}'.format(i,n))

print('nothing')

agol_obj.take_action('df', 'move', target_col = 'DATA_LOCATION_MCMILLEN',
                     dry_run = False, save_df = True,
                     offline_source=False, offline_target=False)