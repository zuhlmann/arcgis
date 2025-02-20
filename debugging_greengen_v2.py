import importlib
import spyder_arcgis_oop as agolZ
importlib.reload(sys.modules['spyder_arcgis_oop'])
import pandas as pd

# Resourceing after move
# FLA road improvement greengen
# 20241017

subproject='greengen_cultural'
fp_pathlist = r"C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\df_utility_csvs\path_list_updated.csv"
fp_pathlist_aprx = r"C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\df_utility_csvs\path_list_aprx.xlsx"
prj_file=r'CA_sp_II_nad83_ft_esri102642.prj'

# Initiaate
pro_obj = agolZ.proProject()
pro_obj.proProject_init(fp_pathlist_aprx)
pro_obj.dbase_init(prj_file, subproject, fp_pathlist)

df_lyR_map_str=f"df_{subproject}_map_lyR"
df_lyR_aprx_str=f"df_{subproject}_aprx_lyR"
df_lyR_all_str=f"df_{subproject}_all_lyR"
df_map_matrix = f"df_{subproject}_map_matrix"
fp_lyR_inv_map = pro_obj.pl_aprx.loc[subproject, 'fp_lyR_map']
fp_lyR_inv_maestro = pro_obj.pl_aprx.loc[subproject, 'fp_lyR_aprx']
fp_lyR_inv_all = pro_obj.pl_aprx.loc[subproject, 'fp_lyR_aprx']
fp_map_matrix = self.pl_aprx.loc[subproject, 'fp_map_matrix']

fp_aprx=pro_obj.pl_aprx.loc[subproject,'fp_aprx']
fp_df_maestro = pro_obj.pl_aprx.loc[subproject,'fp_df_maestro']
fp_lyR_inv_maestro = pro_obj.pl_aprx.loc[subproject,'fp_lyR_aprx']
fp_map_matrix = pro_obj.pl_aprx.loc[subproject,'fp_map_matrix']

# -------CREATE INVENTORIES / FLAG-------

# # A2) If need to Create
# # Create in Pro Utilities
# df_layers = pro_obj.aprx_map_inv(fp_aprx)
# cf = ['ITEM','IS_RASTER','IS_BROKEN']
# df_aggregated = pro_obj.aggregate_rows(df_layers,'DATA_LOCATION_MCMILLEN', 'MAP_NAME', carry_fields=cf)
# df_aggregated.to_csv(fp_lyR_inv)

# # A3) After creating lyR_inv
# df_lyR_str = f"df_{subproject}_lyR_maestro"
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

# # Initiate
# df_lyR_str=f"df_{subproject}_aprx_lyR"
# pro_obj.add_df(fp_lyR_inv_maestro, df_lyR_str, 'DATA_LOCATION_MCMILLEN')

# # B0) OUTER join - lyR to df_maestro
csv_temp=r"C:\Users\UhlmannZachary\Documents\fuck.csv"
# df_maestro=pd.read_csv(fp_df_maestro, index_col='DATA_LOCATION_MCMILLEN')
# df_lyR_maestro=pd.read_csv(fp_lyR_inv_maestro, index_col='DATA_LOCATION_MCMILLEN')
# df_lyR_maestro_subset=df_lyR_maestro[df_lyR_maestro.ACTION_JOIN=='join']
# df_merged = df_maestro.merge(df_lyR_maestro_subset[['ACTION','ITEM']], left_index=True, right_index=True, how='outer')
# df_merged.to_csv(fp_df_maestro)

# # B1_0 Transfer action from lyR_maestro to maestro
# # (separate maestro for PSP_2024)
# import copy
# csv_temp = r'C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\sharepoint\templates\SCL_data_package_devel\temp.csv'
# tc = 'DATA_LOCATION_MCMILLEN'
# df1 = getattr(pro_obj, 'df_lyR_maestro')
# df2 = getattr(pro_obj, 'df')
# action = ['FIX_PSP_2024_2']
# mc_dict={'ACTION':'ACTION','ABSTRACT':'ABSTRACT','MOVE_LOCATION':'MOVE_LOCATION',}
# df2 = pro_obj.df_to_df_transfer_v2(df1, df2, 'ACTION',action, tc, tc, mc_dict, True)
# df2.to_csv(fp_df_maestro)

# # B1_0_copy/move APPX) TAKE_ACTION
# # Probably best performed in Pro to confirm everything was moved
# pro_obj.selection_idx('df', target_action='copy_PSP_2024_2')
# pro_obj.take_action('df','copy_replace', dry_run = True, save_df = True)
# pro_obj.df.loc[pro_obj.indices, 'CREDITS']= 'standard'

# # B1) Transfer Action from df to df_LYr_maestro
# df1 = getattr(pro_obj, 'df')
# df2 = getattr(pro_obj, 'df_lyR_maestro')
# mc_dict={'ACTION':'ACTION','DATA_LOCATION_MCMILLEN':'DATA_LOCATION_MCM_RESOURCE'}
# tc1 = 'DATA_LOCATION_MCM_STAGING'
# tc2 = 'DATA_LOCATION_MCMILLEN'
# action=['copy']
# df2 = pro_obj.df_to_df_transfer_v2(df1, df2, 'ACTION', action, tc1, tc2, mc_dict, False)
# df2.to_csv(fp_lyR_inv_maestro)

# # # # B1) Transfer Action from df_lyr_maestro to df_LYr
# df1 = getattr(pro_obj, 'df_lyR_maestro')
# df2 = getattr(pro_obj, 'df_lyR_inv')
# mc_dict={'ACTION':'ACTION','DATA_LOCATION_MCM_RESOURCE':'DATA_LOCATION_MCM_RESOURCE'}
# tc1 = 'DATA_LOCATION_MCMILLEN'
# tc2 = 'DATA_LOCATION_MCMILLEN'
# action=['copy']
# df2 = pro_obj.df_to_df_transfer_v2(df1, df2, 'ACTION', action, tc1, tc2, mc_dict, False)
# df2.to_csv(fp_lyR_inv)

#----------RESOURCING TRANSFERS------------
df_lyR_str=f"df_{subproject}_aprx_lyR"
df_base_str = df_lyR_str.replace('df_', '')
prop_str_indices = '{}_indices'.format(df_base_str)
pro_obj.add_df(fp_lyR_inv_maestro, df_lyR_str, 'DATA_LOCATION_MCMILLEN')
ta = 'copy'

# # # Add ReSource info
# pro_obj.selection_idx(df_lyR_str, target_action=ta)
# pro_obj.format_lyR_inv_datasource_standard(subproject, lyR_maestro=True)

# Z) Create map matrix - just do once
pro_obj.expand_rows(subproject, fp_map_matrix)

# D) Resource Time
# load maps
pro_obj.add_aprx(subproject,lyR_maestro=True)
pro_obj.selection_idx(df_lyR_str, target_action=ta)
pro_obj.add_maps(subproject)
pro_obj.re_source_lyR_maestro(subproject,prop_str_indices)
# SAVE
df_lyR_inv_all = getattr(pro_obj, df_lyR_all_str)
df_lyR_inv_map = getattr(pro_obj, df_lyR_map_str)
df_lyR_inv_aprx = getattr(pro_obj, df_lyR_aprx_str)
df_map_matrix = getattr(pro_obj, df_map_matrix)
df_lyR_inv_all.to_csv(fp_lyR_inv_all)
df_lyR_inv_map.to_csv(fp_lyR_inv_map)
df_lyR_inv_aprx.to_csv(fp_lyR_inv_all)
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

