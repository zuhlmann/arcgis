import importlib
import spyder_arcgis_oop as agolZ
importlib.reload(sys.modules['spyder_arcgis_oop'])
import pandas as pd

# Resourceing after move
# FLA road improvement greengen
# 20241017

subproject='PSP_2024_2'
fp_pathlist = r"C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\df_utility_csvs\path_list_updated.csv"
fp_pathlist_aprx = r"C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\df_utility_csvs\path_list_aprx.xlsx"
fp_all_SFT_aprx=r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\map_documents\map_documents_aprx_inventory.csv"
prj_file=r'NAD_1983_HARN_StatePlane_Washington_North_FIPS_4601_Feet.prj'

# Initiaate
pro_obj = agolZ.proProject()
pro_obj.proProject_init(fp_pathlist_aprx)
pro_obj.dbase_init(prj_file, subproject, fp_pathlist)

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

# Initiate
pro_obj.add_df(fp_lyR_inv, 'df_lyR_inv', 'DATA_LOCATION_MCMILLEN')
pro_obj.add_df(fp_lyR_inv_maestro, 'df_lyR_maestro', 'DATA_LOCATION_MCMILLEN')

# # B0) OUTER join - lyR to df_maestro
# csv_maestro=r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\gdb_inventories\tolt_devel_maestro.csv"
# df_maestro=pd.read_csv(csv_maestro, index_col='DATA_LOCATION_MCMILLEN')
# df_lyR_maestro=pd.read_csv(fp_lyR_inv_maestro, index_col='DATA_LOCATION_MCMILLEN')
# df_lyR_maestro_subset=df_lyR_maestro[df_lyR_maestro.ACTION=='copy_PSP_2024']
# df_merged = df_maestro.merge(df_lyR_maestro_subset[['ACTION','ITEM']], left_index=True, right_index=True, how='outer')
# df_merged.to_csv(csv_temp)

# # B1_0 Transfer action from lyR_maestro to maestro
# # (separate maestro for PSP_2024)
# import copy
# tc = 'DATA_LOCATION_MCMILLEN'
# df1 = getattr(pro_obj, 'df_lyR_maestro')
# df2 = getattr(pro_obj, 'df')
# action = ['MOVE_PSP']
# mc_dict={'ACTION':'ACTION','ABSTRACT':'ABSTRACT','MOVE_LOCATION':'MOVE_LOCATION',}
# df2 = pro_obj.df_to_df_transfer_v2(df1, df2, 'ACTION',action, tc, tc, mc_dict, False)
# df2.to_csv(csv_temp)

# # B1_0_copy/move APPX) TAKE_ACTION
# # Probably best performed in Pro to confirm everything was moved
# pro_obj.selection_idx('df', target_action='copy_PSP_2024_2')
# pro_obj.take_action('df','copy_replace', dry_run = True, save_df = True)
# pro_obj.df.loc[pro_obj.indices, 'CREDITS']= 'standard'

# # # # B1) Transfer Action from df to df_LYr_maestro
# csv_temp = r'C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\sharepoint\templates\SCL_data_package_devel\temp.csv'
# df1 = getattr(pro_obj, 'df')
# df2 = getattr(pro_obj, 'df_lyR_maestro')
# mc_dict={'ACTION':'ACTION','DATA_LOCATION_MCMILLEN':'DATA_LOCATION_MCM_RESOURCE'}
# tc1 = 'DATA_LOCATION_MCM_STAGING'
# tc2 = 'DATA_LOCATION_MCMILLEN'
# action=['MOVE_PSP']
# df2 = pro_obj.df_to_df_transfer_v2(df1, df2, 'ACTION', action, tc1, tc2, mc_dict, False)
# df2.to_csv(fp_lyR_inv_maestro)

# # # # B1) Transfer Action from df to df_LYr_maestro
# df1 = getattr(pro_obj, 'df_lyR_maestro')
# df2 = getattr(pro_obj, 'df_lyR_inv')
# mc_dict={'ACTION':'ACTION','DATA_LOCATION_MCM_RESOURCE':'DATA_LOCATION_MCM_RESOURCE'}
# tc1 = 'DATA_LOCATION_MCMILLEN'
# tc2 = 'DATA_LOCATION_MCMILLEN'
# action=['MOVE_PSP']
# df2 = pro_obj.df_to_df_transfer_v2(df1, df2, 'ACTION', action, tc1, tc2, mc_dict, False)
# df2.to_csv(fp_lyR_inv)

#----------RESOURCING TRANSFERS------------
df_lyR_str='df_{}_lyR'.format(subproject)
pro_obj.add_df(fp_lyR_inv, df_lyR_str, 'DATA_LOCATION_MCMILLEN')
ta = 'MOVE_PSP'

# # # Add ReSource info
# pro_obj.selection_idx(df_lyR_str, target_action='MOVE_PSP')
# pro_obj.format_lyR_inv_datasource_standard(subproject)

# # Z) Create map matrix - just do once
# pro_obj.expand_rows(subproject, fp_map_matrix)

# D) Resource Time
# load maps
pro_obj.add_aprx(subproject)
pro_obj.selection_idx(df_lyR_str, target_action=ta)
pro_obj.add_maps(subproject)
pro_obj.re_source_lyR_maestro(subproject)
# SAVE
df_lyR_inv = getattr(pro_obj, f"df_{subproject}_lyR")
df_map_matrix = getattr(pro_obj, f"df_map_matrix_{subproject}")
df_lyR_inv.to_csv(fp_lyR_inv)
df_map_matrix.to_csv(fp_map_matrix)

# # D_a) Update CSS from maestro
# # After Re-Sourcing, remove aprx name from csSring
# aprx='PSP_2024'
# df_lyR_inv = getattr(pro_obj, df_lyR_str)
# index_csString=df_lyR_inv[df_lyR_inv.RESOURCE_COMPLETE=='yes'].index
# df=pd.read_csv(fp_lyR_inv_maestro, index_col='DATA_LOCATION_MCMILLEN')
# for idx in index_csString:
#     csString_orig = df.loc[idx, 'APRX_TO_FIX']
#     csString_updated = pro_obj.parse_csString_utils(csString_orig, remove_item=aprx)
#     df.at[idx, 'APRX_TO_FIX']=csString_updated
# df.to_csv(fp_lyR_inv_maestro)


# # E_a) write_xml
# df_str = 'df'
# pro_obj.write_xml('df', offline=False)

