import importlib
import spyder_arcgis_oop as agolZ
importlib.reload(sys.modules['spyder_arcgis_oop'])
import pandas as pd

# ONE OFF: Create joined lyR_inv and flag BROKEN paths
# 20241031
# A) Base Everyghint
fp_pathlist_aprx = r"C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\df_utility_csvs\path_list_aprx.xlsx"

pro_obj = agolZ.proProject()
pro_obj.proProject_init(fp_pathlist_aprx)

# #-----------------MULTI-APRX LYR INVS (1 THRU 3)`````````````````
# # Master lyR_inv for projects with multiple aprx i.e. SFT_lyR_deliverable_inv2_v3_<2,1,0>
# # E) ONE-OFF lyR Inv for MULTIPLE aprx from script
# # Created Input CSV in dir_use_inv inventory, to list all aprx used in PAD/PSP and agglomerate
# fp_pathlist_aprx=r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\map_documents\map_documents_aprx_inventory.csv"
fp_pathlist_aprx=r"C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\DLA\data_inventories\aprx\FLA_aprx_all.csv"
csv_aprx_lyR_2=r"C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\DLA\data_inventories\aprx\FLA_aprx_all_lyr_v1_2.csv"
# pro_obj.aprx_map_inv2(fp_pathlist_aprx, csv_aprx_lyR_2)
#
# # E2) Concatenate Aggregate
# csv_aprx_lyR_1=r"C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\DLA\data_inventories\aprx\FLA_aprx_all_lyr_v1_1.csv"
# cf = ['ITEM','IS_RASTER','IS_BROKEN']
# pro_obj.concatenate_aggregate(csv_aprx_lyR_2, csv_aprx_lyR_1, 'APRX', 'DATA_LOCATION_MCMILLEN', 'MAP_NAME', carry_fields=cf)
# #
# # B. Aggregate Map_Name from Data_Location;  could have potentially skipped step 2.
# df1=pd.read_csv(csv_aprx_lyR_1)
# df2 =pro_obj.aggregate_rows(df1, 'DATA_LOCATION_MCMILLEN','APRX',carry_fields=cf)
# csv_aprx_lyR_0=r"C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\DLA\data_inventories\aprx\FLA_aprx_all_lyr_v1_0.csv"
# df2.to_csv(csv_aprx_lyR_0)

# ---------------------BULK CREATE LYR AND MAP_MATRIX INDICES------

# # ONE OFF: Create joined lyR_inv and flag BROKEN paths

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

#--------------------MISCELLENAOUSS-------------

# # C) lyR inv of all broken layers from aprx_maestro
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

# # MISC Flag cols containing csString vals i.e. PSP_2024
# # df_lyR_str='df_lyR_maestro'
# pro_obj.add_df(fp_lyR_inv_maestro, 'df_lyR_maestro', 'DATA_LOCATION_MCMILLEN')
# df = pro_obj.flag_csString_val('df_lyR_maestro', 'APRX', 'PSP_2024_2', 'PSP_2024_2')
# df.to_csv(fp_lyR_inv_maestro)

df_reSource=pd.read_csv(r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\sharepoint\templates\SCL_data_package_devel\staging\SFT_lyR_reSourcing.csv")
df_lyr0=pd.read