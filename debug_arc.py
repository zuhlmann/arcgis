import os
import sys
sys.path.append('c:/users/uhlmann/code')
sys.path.append('c:/users/uhlmann/code/arcpy_script_tools_uhlmann')
import utilities
import copy
import pandas as pd
import importlib
importlib.reload(sys.modules['utilities'])

# subproject = 'SFT_common_maps2'
# fp_pathlist = r'C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\df_utility_csvs\path_list_updated.csv'
# pl = pd.read_csv(fp_pathlist, index_col = 'gdb_str')
# prj_dir = r'C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\prj_files'
# prj_file = os.path.join(prj_dir, pl[pl.subproject == subproject].prj_file.values[0])
#
# # TOLT
# import spyder_arcgis_oop as agolZ
# importlib.reload(sys.modules['spyder_arcgis_oop'])
# agol_obj = agolZ.commonUtils()
# agol_obj.dbase_init(prj_file,subproject,fp_pathlist, use_item_desc=False)
#
# # # INDICES
# agol_obj.selection_idx('df', indices = [-1])
# agol_obj.selection_idx('df', target_action= 'copy')
#
# # Ba TAKE ACTION
# agol_obj.take_action('df', 'copy_replace', target_col = 'DATA_LOCATION_MCMILLEN',
#                      dry_run = False, save_df = True,
#                      offline_source=False, offline_target=False)

# # b) SHARE
# fp_csv_tracking = r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\data_sent\data_shared_inventory.csv"
# base_dir = r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\data_sent\study_areas_PSP"
#
# notes = r'Updates Cultural SA which includes USFS land within SFT Watershed.'+\
#         r' ' +\
#         r''
# tags = 'SFT'
# rc = 'Lynn Comppas'
# rn = ''
# project = 'tolt'
# d = {'notes':notes, 'tags':tags,'recipient_company':rc,
#     'recipient_name':rn, 'project':project}
#
# # NEED TO FIX ZIPPING!  Did that manually for predrawdown ground dist. ZU 20230224
# # a) shapefiles
# agol_obj.data_sent_tracking(fp_csv_tracking, base_dir, 'convert_zip', d)
#
# # # b) gdb
# # fp_gdb = os.path.join(base_dir, 'gdb','cultural_SA.gdb')
# # agol_obj.data_sent_tracking(fp_csv_tracking, fp_gdb, 'copy_to_gdb', d)

# C) MISCLENEOUS

# join 20241224
xslx_in=r"C:\Box\MCM Projects\Seattle City Light\23-024_South Fork Tolt Relicensing\11.0 Supplemental Files\Figures\PSP\study_area_descriptions.xlsx"
csv_out=r'C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\data_sent\study_areas_PSP\gdb\SFT_Study_Areas_20241224.csv'
df=pd.read_excel(xslx_in)
df_data=pd.read_csv(r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\data_sent\study_areas_PSP\gdb\SFT_StudyAreas_20241220_inv.csv")
df_join=df.merge(df_data[['row','ITEM']],left_on='JOIN_ROW',right_on='row')
# df_join.to_csv(csv_out)

ser=pd.Series(df_join.columns)
ser.to_csv(r'C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\data_sent\study_areas_PSP\gdb\columns.csv')
