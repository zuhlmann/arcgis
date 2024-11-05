import importlib
import spyder_arcgis_oop as agolZ
importlib.reload(sys.modules['spyder_arcgis_oop'])
import pandas as pd

# Resourceing after move
# FLA road improvement greengen
# 20241017

subproject='PSP_2024'
fp_pathlist = r"C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\df_utility_csvs\path_list_updated.csv"
fp_pathlist_aprx = r"C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\df_utility_csvs\path_list_aprx.xlsx"
fp_all_SFT_aprx=r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\map_documents\map_documents_aprx_inventory.csv"
prj_file=r'NAD_1983_HARN_StatePlane_Washington_North_FIPS_4601_Feet.prj'

# Initiaate
pro_obj = agolZ.proProject()
pro_obj.proProject_init(fp_pathlist_aprx)
pro_obj.dbase_init(prj_file, subproject, fp_pathlist)

prj_file = pro_obj.prj_file
fp_aprx=pro_obj.pl_aprx.loc[subproject,'fp_aprx']
fp_lyR_inv = pro_obj.pl_aprx.loc[subproject,'fp_lyR_inv']
fp_lyR_inv_maestro = pro_obj.pl_aprx.loc[subproject,'fp_lyR_maestro']
fp_tolt_maestro = r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\gdb_inventories\tolt_devel_maestro.csv"
fp_map_matrix = pro_obj.pl_aprx.loc[subproject,'fp_map_matrix']

# -------CREATE INVENTORIES / FLAG-------

# # A2) If need to Create
# # Create in Pro Utilities
# df_layers = pro_obj.aprx_map_inv(fp_aprx)
# df_aggregated = pro_obj.aggregate_rows(df_layers,'DATA_LOCATION_MCMILLEN', 'MAP_NAME', carry_fields=['IS_RASTER','IS_BROKEN'])
# df_aggregated.to_csv(fp_lyR_inv)

# # A3) After creating lyR_inv
# use_maestro=True
# if use_maestro:
#     df_lyR_str = f"df_{subproject}_lyR_maestro"
# pro_obj.add_aprx(subproject, lyR_maestro=use_maestro)

# # Create Broken Filepath Inv
# # A) Inventory broken layers
#  REMOVED THIS METHOD --> USE APRX_INV
# pro_obj.aprx_broken_source_inv(aprx_str, fp_lyR_inv)

# # A2) Create fixed path column
# # Manually add 'target' and 'replace' vals for DATA_LOCATION.replace('target','replace')
# # to iterate and create DATA_LOCATION_RESOURCE
# pro_obj.selection_idx('df_PAD_aerials_lyR', target_action='fix')
# pro_obj.aprx_broken_source_inv2(subproject, lyR_maestro=True)

# --------DF TO DF TRANSFERS------

# # B0) OUTER join - lyR to df_maestro
# csv_maestro=r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\gdb_inventories\tolt_devel_maestro.csv"
# df_maestro=pd.read_csv(csv_maestro, index_col='DATA_LOCATION_MCMILLEN')
# df_lyR_maestro=pd.read_csv(fp_lyR_inv_maestro, index_col='DATA_LOCATION_MCMILLEN')
# df_lyR_maestro_subset=df_lyR_maestro[df_lyR_maestro.ACTION=='copy_PSP_2024']
# df_merged = df_maestro.merge(df_lyR_maestro_subset[['ACTION','ITEM']], left_index=True, right_index=True, how='outer')
# df_merged.to_csv(csv_temp)

# # # B1) Transfer Action from df to df_aprx
# pro_obj.add_df(fp_lyR_inv, 'df_lyR_inv', 'DATA_LOCATION_MCMILLEN')
# pro_obj.add_df(fp_lyR_inv_maestro, 'df_lyR_maestro', 'DATA_LOCATION_MCMILLEN')
csv_temp = r'C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\sharepoint\templates\SCL_data_package_devel\temp.csv'
# df1 = pd.read_csv(fp_tolt_maestro)
# df2 = pro_obj.df_lyR_maestro
# mc_dict={'ACTION':'ACTION','DATA_LOCATION_MCM_ORIGINAL':'DATA_LOCATION_MCM_RESOURCE'}
# tc = 'DATA_LOCATION_MCMILLEN'
# df1 = pro_obj.df_to_df_transfer_v2(df1, df2, 'ACTION','copy_PSP_2024', tc, tc, mc_dict)
# df1.to_csv(csv_temp)

# B2 ONE OFF: Transfer action from Tolt Maestro to PSP_2024_maestro
# (separate maestro for PSP_2024)
import copy
tc = 'DATA_LOCATION_MCMILLEN'
df1 = pd.read_csv(fp_tolt_maestro, index_col=tc)
df2 = copy.copy(pro_obj.df)
action = ['copy_PSP_2024_1','copy_PSP_2024_2','skip_PSP_2024']
mc_dict={'ACTION':'ACTION','DATA_LOCATION_MCM_ORIGINAL':'DATA_LOCATION_MCM_RESOURCE'}
df1 = pro_obj.df_to_df_transfer_v2(df1, df2, 'ACTION',action, tc, tc, mc_dict, True)
df1.to_csv(csv_temp)

#----------RESOURCING TRANSFERS------------

# # # Add ReSource info
# # # pro_obj.add_df(fp_lyR_inv, 'df_greengen_ferc_lyR', 'random')
# pro_obj.selection_idx('df_PAD_aerials_lyR', target_action='fix')
# pro_obj.format_lyR_inv_datasource_standard(subproject, lyR_maestro=True)

# # Z) Create map matrix - just do once
# pro_obj.expand_rows(subproject, fp_map_matrix)

# # D) Resource Time
# # load maps
# import pandas as pd
# # pro_obj.get_base_aprx_content(aprx_str)
# pro_obj.selection_idx(df_lyR_str, target_action='fix2')
# pro_obj.add_maps(subproject)
# pro_obj.re_source_lyR_maestro(subproject, lyR_maestro=True)
# # SAVE
# df_lyR_inv = getattr(pro_obj, f"df_{subproject}_lyR")
# df_map_matrix = getattr(pro_obj, f"df_map_matrix_{subproject}")
# df_lyR_inv.to_csv(fp_lyR_inv)
# df_map_matrix.to_csv(fp_map_matrix)




# # ONE OFF: Create joined lyR_inv and flag BROKEN paths
# # 20241031
# # A) Base Everyghint
# fp_all_SFT_aprx=r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\map_documents\map_documents_aprx_inventory.csv"
# pro_obj = agolZ.proProject()
# pro_obj.proProject_init(fp_pathlist_aprx)
#
# df = pd.read_csv(fp_all_SFT_aprx, index_col='APRX')
# sp_list = df[df.FLAG].index

# # B) Create individual inventories and map matrices
# for subproject in sp_list:
#     print('CREATING INV FOR {}'.format(subproject))
#     # prj_file = pro_obj.pl.loc[subproject, 'prj_file']
#     fp_aprx=pro_obj.pl_aprx.loc[subproject,'fp_aprx']
#     fp_lyR_inv = pro_obj.pl_aprx.loc[subproject,'fp_lyR_inv']
#     fp_map_matrix = pro_obj.pl_aprx.loc[subproject,'fp_map_matrix']
#
#     # A2) If need to Create
#     # Create in Pro Utilities
#     df_layers = pro_obj.aprx_map_inv(fp_aprx)
#     df_aggregated = pro_obj.aggregate_rows(df_layers,'DATA_LOCATION_MCMILLEN', 'MAP_NAME', carry_fields=['IS_RASTER','IS_BROKEN'])
#     df_aggregated.to_csv(fp_lyR_inv)
#
#     # # # Z) Create map matrix - just do once
#     pro_obj.expand_rows(subproject, fp_map_matrix)

# # C) Join all lyR inventories
# import copy
# for subproject in sp_list:
#     fp_lyR_inv = pro_obj.pl_aprx.loc[subproject, 'fp_lyR_inv']
#     df_temp = pd.read_csv(fp_lyR_inv)
#     df_temp=df_temp[df_temp.IS_BROKEN]
#     df_temp['APRX']=[subproject]*len(df_temp)
#     # will be zero if no broken layers
#     if len(df_temp)>0:
#         if not 'df_joined' in locals():
#             df_joined = copy.copy(df_temp)
#         else:
#             print(subproject)
#             df_joined = pd.concat([df_joined[['DATA_LOCATION_MCMILLEN','APRX']], df_temp[['DATA_LOCATION_MCMILLEN','APRX']]])
# df_joined = pro_obj.aggregate_rows(df_joined, 'DATA_LOCATION_MCMILLEN','APRX')
# df_joined.to_csv(r'C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\sharepoint\templates\SCL_data_package_devel\broken_layers.csv')


