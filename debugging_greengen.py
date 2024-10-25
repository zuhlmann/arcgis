import importlib
import spyder_arcgis_oop as agolZ
importlib.reload(sys.modules['spyder_arcgis_oop'])
import pandas as pd

# Resourceing after move
# FLA road improvement greengen
# 20241017
subproject='aquatics_4peaks'
fp_pathlist = r"C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\df_utility_csvs\path_list_updated.csv"
# pl = pd.read_csv(fp_pathlist, index_col='subproject')
# prj_file = pl.loc[subproject, 'prj_file']
fp_pathlist_aprx = r"C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\df_utility_csvs\path_list_aprx.xlsx"
pl_aprx=pd.read_excel(fp_pathlist_aprx, index_col='subproject')
fp_aprx=pl_aprx.loc[subproject,'fp_aprx']
fp_lyR_inv = pl_aprx.loc[subproject,'fp_lyR_inv']
fp_map_matrix = pl_aprx.loc[subproject,'fp_map_matrix']


# Initiaate
pro_obj = agolZ.proProject()
# pro_obj.dbase_init(prj_file,subproject,fp_pathlist, use_item_desc=False)

# A2) If need to Create
# Create in Pro Utilities
df_layers = pro_obj.aprx_map_inv(fp_aprx)
df_aggregated = pro_obj.aggregate_rows(df_layers,'DATA_LOCATION_MCMILLEN', 'MAP_NAME', carry_fields=True)
df_aggregated.to_csv(fp_lyR_inv)

# # A3) After creating lyR_inv
# # Can set to False if no inv yet, then set to True
# pro_obj.add_aprx(fp_aprx, fp_lyR_inv,True, 'DATA_LOCATION_MCMILLEN')
# pro_obj.get_base_aprx_content(aprx_str)
#
# # Create Broken Filepath Inv
# # A) Inventory broken layers
# pro_obj.aprx_broken_source_inv(aprx_str, fp_lyR_inv)

# # A2) Create fixed path column
# # Manually add 'target' and 'replace' vals for DATA_LOCATION.replace('target','replace')
# # to iterate and create DATA_LOCATION_RESOURCE
# pro_obj.selection_idx('df_FLA_road_improvement_lyR', target_action='fix')
# pro_obj.aprx_broken_source_inv2(fp_lyR_inv,'aprx_FLA_road_improvement')

# # B) Transfer Action from df to df_aprx
# merge_cols = ['DATA_LOCATION_MCMILLEN','ACTION']
# pro_obj.df_to_df_transfer_v2('df', 'df_greengen_ferc_lyR', r'ACTION',r'ACTION',r'copy',
#                      'DATA_LOCATION_MCM_ORIGINAL', 'DATA_LOCATION_MCMILLEN', merge_cols,
#                      merge_cols_dict={'DATA_LOCATION_MCMILLEN':'DATA_LOCATION_MCM_RESOURCE'})
# # Save
# pro_obj.df_greengen_ferc_lyR_matched.to_csv(csv_lyR_inv)

# # # Add ReSource info
# # # pro_obj.add_df(fp_lyR_inv, 'df_greengen_ferc_lyR', 'random')
# pro_obj.selection_idx('df_FLA_road_improvement_lyR', target_action='fix')
# pro_obj.format_lyR_inv_datasource_standard('aprx_FLA_road_improvement')

# # # # Z) Create map matrix - just do once
csv_map_matrix = r'C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Maps\FLA\data_inv\map_matrix.csv'
# pro_obj.expand_rows(aprx_str, csv_map_matrix)

# # D) Resource Time
# # load maps
# import pandas as pd
# pro_obj.selection_idx('df_FLA_road_improvement_lyR', target_action='fix')
# # pro_obj.get_base_aprx_content(aprx_str)
# df_map_matrix = pd.read_csv(csv_map_matrix, index_col='DATA_LOCATION_MCMILLEN')
# pro_obj.re_source_lyR_maestro(aprx_str, df_map_matrix)

# # E) ONE-OFF Multiple APRX
# # Created Input CSV in dir_use_inv inventory, to list all aprx used in PAD/PSP and agglomerate
# csv_aprx=r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\map_documents\map_documents_aprx_inventory.csv"
# csv_aprx_lyR=r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\sharepoint\templates\SCL_data_package_devel\SFT_lyR_deliverable_inv.csv"
# # pro_obj.aprx_map_inv2(csv_aprx, csv_aprx_lyR)
#
# # E2) Concatenate Aggregate
# csv_aprx_lyR_devel=r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\sharepoint\templates\SCL_data_package_devel\SFT_lyR_deliverable__devel_inv.csv"
# # A. Agglomerate with aprx and map_name
# # pro_obj.concatenate_aggregate(csv_aprx_lyR, csv_aprx_lyR_devel, 'APRX', 'DATA_LOCATION_MCMILLEN', 'MAP_NAME')
# df1=pd.read_csv(csv_aprx_lyR)
# # B. Aggregate Map_Name from Data_Location;  could have potentially skipped step 2.
# df2 = pro_obj.aggregate_rows(df1, 'DATA_LOCATION_MCMILLEN','APRX')
# csv_aprx_lyR2=r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\sharepoint\templates\SCL_data_package_devel\SFT_lyR_deliverable_inv2.csv"
# df2.to_csv(csv_aprx_lyR2)
