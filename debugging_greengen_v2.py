import importlib
import spyder_arcgis_oop as agolZ

importlib.reload(sys.modules['spyder_arcgis_oop'])
import pandas as pd
import os

subproject='geosyntec_pad_H20'
fp_pathlist = r"C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\df_utility_csvs\path_list_updated.csv"
fp_pathlist_aprx = r"C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\df_utility_csvs\path_list_aprx.xlsx"
prj_file = r'NAD_1983_HARN_StatePlane_Washington_North_FIPS_4601_Feet.prj'

# Initiaate
pro_obj = agolZ.proProject()
pro_obj.proProject_init(fp_pathlist_aprx)
pro_obj.dbase_init(prj_file, subproject, fp_pathlist)

df_lyR_aprx_str=f"df_{subproject}_aprx_lyR"
df_lyR_map_str=f"df_{subproject}_map_lyR"
df_lyR_all_str=f"df_{subproject}_all_lyR"
df_map_matrix_str = f"df_{subproject}_map_matrix"
df_reSource_str = f"df_{subproject}_reSource"
fp_lyR_inv_map = pro_obj.pl_aprx.loc[subproject, 'fp_lyR_map']
fp_lyR_inv_maestro = pro_obj.pl_aprx.loc[subproject, 'fp_lyR_aprx']
fp_lyR_inv_all = pro_obj.pl_aprx.loc[subproject, 'fp_lyR_all']
fp_map_matrix =pro_obj.pl_aprx.loc[subproject, 'fp_map_matrix']
fp_lyR_inv = pro_obj.pl_aprx.loc[subproject, 'fp_lyR_inv']

fp_aprx=pro_obj.pl_aprx.loc[subproject,'fp_aprx']
fp_map_matrix = pro_obj.pl_aprx.loc[subproject,'fp_map_matrix']
fp_maestro = pro_obj.pl_aprx.loc[subproject,'fp_df_maestro']
fp_reSource = pro_obj.pl_aprx.loc[subproject, 'fp_df_reSource']

# # -------CREATE INVENTORIES / FLAG-------

# # A1a) Single APRX from subproject
# df_layers = pro_obj.aprx_map_inv(fp_aprx)
# # Raw, unaggregated NEED for creating _0 _1 _2 invs
# df_layers.to_csv(fp_lyR_inv)
# cf = ['ITEM','IS_RASTER','IS_BROKEN']
# df_aggregated = pro_obj.aggregate_rows(df_layers,'DATA_LOCATION_MCMILLEN', 'MAP_NAME', carry_fields=cf)
# df_aggregated.to_csv(r'{}_aggregated.csv'.format(os.path.splitext(fp_lyR_inv)[0]))
# A2b) Create map matrix - just do once
# pro_obj.expand_rows(subproject, fp_map_matrix)

# # A1b)  Create Single Inventories from DF
# # This will recreate individual inventories- Do ocassionally
# # ALL FLAGGED
# df_pl_aprx=getattr(pro_obj,'pl_aprx')
# df_pl_aprx=df_pl_aprx[df_pl_aprx.FLAG]
# #
# for idx in df_pl_aprx.index:
#     df_layers = pro_obj.aprx_map_inv(df_pl_aprx.loc[idx, 'fp_aprx'])
#     # Raw, unaggregated NEED for creating _0 _1 _2 invs
#     fp_lyR_inv_temp = df_pl_aprx.loc[idx, 'fp_lyR_inv']
#     df_layers.to_csv(fp_lyR_inv_temp)
#     cf = ['ITEM','IS_RASTER','IS_BROKEN']
#     df_aggregated = pro_obj.aggregate_rows(df_layers,'DATA_LOCATION_MCMILLEN', 'MAP_NAME', carry_fields=cf)
#     df_aggregated.to_csv(r'{}_aggregated.csv'.format(os.path.splitext(fp_lyR_inv_temp)[0]))
#
# # Matrix from DF
# for idx in df_pl_aprx.index:
#     fp_map_matrix_temp=df_pl_aprx.loc[idx, 'fp_map_matrix']
#     pro_obj.expand_rows(idx, fp_map_matrix_temp)

# # # A2 Multiple APRX all in one
# # # THIS!!! Re-up the lyr_2 lyr_1 lyr_0
# pro_obj.aprx_map_inv2(fp_pathlist_aprx, fp_lyR_inv_all)
# pro_obj.add_df(fp_lyR_inv_all, df_lyR_all_str, 'DATA_LOCATION_MCMILLEN')
# cf = ['ITEM','IS_RASTER','IS_BROKEN']
# pro_obj.concatenate_aggregate(fp_lyR_inv_all, fp_lyR_inv_map, 'APRX', 'DATA_LOCATION_MCMILLEN', 'MAP_NAME', carry_fields=cf)
# df_lyR_all=pd.read_csv(fp_lyR_inv_all)
# df_aggregated = pro_obj.aggregate_rows(df_lyR_all,'DATA_LOCATION_MCMILLEN', 'APRX', carry_fields=cf)
# df_aggregated.to_csv(fp_lyR_inv_maestro)

# # A3) After creating lyR_inv
# df_lyR_str = f"df_{subproject}_lyR_maestro"
# pro_obj.add_aprx(subproject, lyR_maestro=use_maestro)

# # A2) Create fixed path column
# # Manually add 'target' and 'replace' vals for DATA_LOCATION.replace('target','replace')
# # to iterate and create DATA_LOCATION_RESOURCE
# pro_obj.selection_idx('df_PAD_aerials_lyR', target_action='fix')
# pro_obj.aprx_broken_source_inv2(subproject, lyR_maestro=True)

# --------DF TO DF TRANSFERS------

# # Initiate
# df_lyR_str=f"df_{subproject}_aprx_lyR"
# pro_obj.add_df(fp_lyR_inv_maestro, df_lyR_aprx_str, 'DATA_LOCATION_MCMILLEN')

# B0) UPDATE - like outer join but replacing back and forth between maestro and aprx_maestro
# Note this will add ALL data sources, i.e. HydrMcM_Streams and Tolt_Streams_2024
# Used Jan 2026, umsure on the Ommitted argument purpose
csv_2=fp_lyR_inv_maestro
csv_1=fp_maestro
df_str_2 = df_lyR_aprx_str
df_str_1 = 'df'
pro_obj.add_df(csv_1, df_str_1, 'DATA_LOCATION_MCMILLEN')
pro_obj.add_df(csv_2, df_str_2, 'DATA_LOCATION_MCMILLEN')
tc_1, tc_2 ='DATA_LOCATION_MCMILLEN', 'DATA_LOCATION_MCMILLEN'
d={'ACTION':'resource_others','ACTION':'rename','ACTION':'copy_rd4','ACTION':'lebron'}
d={'ACTION':'rename_geosyntec'}
cols_update = ['ITEM','ACTION', 'geosyntec_pad_H20_p2']
pro_obj.custom_merge(df_str_2, df_str_1, tc_2, tc_1, cols_update,
                     True, True, subset=d)
df_updated=getattr(pro_obj, df_str_1)
csv_1 = r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\gdb_inventories\tolt_devel_maestro_temp.csv"
df_updated.to_csv(csv_1)
# #
# # B1) JOINS manual - lyR to df_maestro
# csv_temp=r"C:\Users\UhlmannZachary\Documents\fuck.csv"
# csv_left=r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\sharepoint\templates\SCL_data_package_devel\staging\SFT_lyR_DELETE_maestro.csv"
# df_left=pd.read_csv(fp_lyR_inv_maestro, index_col=['DATA_LOCATION_MCMILLEN'])
# df_right=pd.read_csv(fp_maestro, index_col=['DATA_LOCATION_MCMILLEN'])
# cols=['ACTION','DATA_LOCATION_MCM_RESOURCE','workspace_factory','feature_dataset','dataset','dbase_connection' ]
# cols=['ACTION']
# # If masking df_maestro to join DATA_lOCATION_MCM_RESOURCE. NOTE change index col in read_csv 20250414
# # mask=df_right[~pd.isnull(df_lyR_maestro_orig[['DATA_LOCATION_MCM_RESOURCE', 'ACTION']]).all(1)]
# # subset=df_right.loc[mask.index,cols]
# # idx = [i for i in df_right.index if df_right.loc[i, 'ACTION'] in ['rename_again','rename_psp2']]
# # subset=df_right.loc[idx, cols]
# subset=df_right['ACTION']
# df_merged = pd.merge(df_left, subset, left_index=True, right_index=True, how='left')
# df_merged.to_csv(csv_temp)

# # # # B2_copy/move APPX) TAKE_ACTION
# # # # Probably best performed in Pro to confirm everything was moved
# # # pro_obj.selection_idx('df', target_action='rename_master')
# # # pro_obj.take_action('df','move', dry_run = False, save_df = True)
# # B1) Transfer Action from df to df_LYr_maestro
# df2 = getattr(pro_obj, 'df')
# df1 = getattr(pro_obj, df_lyR_aprx_str)
# mc_dict={'ACTION':'ACTION','DATA_LOCATION_MCMILLEN':'DATA_LOCATION_MCM_RESOURCE'}
# # mc_dict={'ACTION':'ACTION'}
# tc1 = 'DATA_LOCATION_MCM_STAGING'
# tc2 = 'DATA_LOCATION_MCMILLEN'
# df2 = pro_obj.df_to_df_transfer_v2(df1, df2, 'ACTION', 'rename_rd3', tc1, tc2, mc_dict, False)
# df2.to_csv(fp_lyR_inv_maestro)
# # df1.to_csv(fp_maestro)

#----------RESOURCING TRANSFERS------------
# # Add Resourcing vals to df_reSource
# # Indices for reSource
# df_base_str = df_reSource_str.replace('df_', '')
# ta = 'resource_info'
# prop_str_indices = '{}_indices'.format(df_base_str)
# pro_obj.add_df(fp_reSource, df_reSource_str, 'DATA_LOCATION_MCMILLEN')
# pro_obj.selection_idx(df_reSource_str, target_action=ta)
# pro_obj.format_lyR_inv_datasource_standard(subproject, df_reSource_str, prop_str_indices)
# t = getattr(pro_obj, df_reSource_str)
# t.to_csv(fp_reSource)

# D) Resource Time
# Indices for lyR
df_lyR_str=f"df_{subproject}_aprx_lyR"
df_base_str = df_lyR_str.replace('df_', '')
ta = 'resource_geosyntec'
prop_str_indices = '{}_indices'.format(df_base_str)
pro_obj.add_df(fp_lyR_inv_maestro, df_lyR_aprx_str, 'DATA_LOCATION_MCMILLEN')
pro_obj.selection_idx(df_lyR_str, target_action=ta)
#
# load maps
pro_obj.add_aprx(subproject,lyR_maestro=True)
pro_obj.add_maps(subproject)
fp_log_prop_str = f"fp_log_{subproject}_aprx_lyR"
pro_obj.re_source_lyR_maestro(subproject,prop_str_indices, fp_log_prop_str)
# # SAVE
df_lyR_inv_all = getattr(pro_obj, df_lyR_all_str)
df_lyR_inv_all.reset_index(inplace=True)
df_lyR_inv_map = getattr(pro_obj, df_lyR_map_str)
df_lyR_inv_map.reset_index(inplace=True)
df_lyR_inv_aprx = getattr(pro_obj, df_lyR_aprx_str)
df_lyR_inv_aprx.reset_index(inplace=True)
df_map_matrix = getattr(pro_obj, df_map_matrix_str)
df_map_matrix.reset_index(inplace=True)
df_lyR_inv_all.to_csv(fp_lyR_inv_all)
df_lyR_inv_map.to_csv(fp_lyR_inv_map)
df_lyR_inv_aprx.to_csv(fp_lyR_inv_maestro)
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
#

# # E_a) write_xml
# df_str = 'df'
# pro_obj.write_xml('df', offline=False)

# FLAGGING DFs FOR RESOURCE, RENAMING ETC

# # 20250820
# # Step 1 lag cols containing csString vals i.e. PSP_2024
# pro_obj.add_df(fp_lyR_inv_maestro, 'df_lyR_maestro', 'DATA_LOCATION_MCMILLEN')
# df = pro_obj.flag_csString_val('df_lyR_maestro', 'APRX', 'swca_economics', 'swca_econommics')
# df.to_csv(fp_lyR_inv_maestro)

# # Step 2 Transfer aprx flag column to df_maestro
# pro_obj.add_df(fp_lyR_inv_maestro, 'df_lyR_maestro', 'DATA_LOCATION_MCMILLEN')
# pro_obj.add_df(fp_maestro, 'df_maestro', 'DATA_LOCATION_MCMILLEN')
# df_lyR_inv_maestro=getattr(pro_obj, 'df_lyR_maestro')
# df_lyR_inv_maestro = df_lyR_inv_maestro[df_lyR_inv_maestro['ACTION'].isin(['swca_economics', 'swca_economics_rename'])]
# left_table = df_lyR_inv_maestro[['ACTION','ITEM']]
# # left_table = left_table.reset_index().set_index('ITEM')
# df_maestro=getattr(pro_obj, 'df_maestro')
# df_new = df_maestro.merge(left_table, how='outer', left_index=True, right_index=True)
# df_new.to_csv(r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\gdb_inventories\tolt_devel_maestro_temp.csv")

# # Step 3 Flag if already resourced
# pro_obj.add_df(fp_maestro, 'df_maestro', 'DATA_LOCATION_MCMILLEN')
# csv_reSource = r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\sharepoint\templates\SCL_data_package_devel\SFT_lyR_reSourcing.csv"
# df_resource=pd.read_csv(csv_reSource)
# df_maestro=getattr(pro_obj, 'df_maestro')
# flag_resource = df_resource[['DATA_LOCATION_MCMILLEN']]
# df_new = df_maestro.merge(flag_resource, how='left', left_on='DATA_LOCATION_MCMILLEN', right_on='DATA_LOCATION_MCMILLEN')
# flag_resource.set_index('DATA_LOCATION_MCMILLEN',inplace=True)
# flag_resource['ALREADY_RENAMED']=True
# df_new.to_csv(r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\sharepoint\templates\SCL_data_package_devel\SFT_lyR_deliverable_inv2_v3_0_temp.csv")

# # Step 2b After maestro Action populated, copy back to df_lyR_maestro
# pro_obj.add_df(fp_lyR_inv_maestro, 'df_lyR_maestro', 'DATA_LOCATION_MCMILLEN')
# pro_obj.add_df(fp_maestro, 'df_maestro', 'DATA_LOCATION_MCMILLEN')
# df_lyR_inv_maestro=getattr(pro_obj, 'df_lyR_maestro')
# df_maestro=getattr(pro_obj, 'df_maestro')
# df_maestro = df_maestro[['ACTION']]
# df_new = df_lyR_inv_maestro.merge(df_maestro, how='left', left_index=True, right_index=True)
# df_new.to_csv(fp_lyR_inv_maestro)
#
# # GENERAL JOIN / MERGE POST UPDATE
# # Step 2 Transfer aprx flag column to df_maestro
# csv_orig = r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\sharepoint\templates\SCL_data_package_devel\SFT_lyR_deliverable_inv2_v3_0_backup20250820.csv"
# df_src = pd.read_csv(csv_orig, index_col='DATA_LOCATION_MCMILLEN')
# df_src = df_src[['ACTION']]
# pro_obj.add_df(fp_lyR_inv_maestro, 'df_lyR_maestro', 'DATA_LOCATION_MCMILLEN')
# df_lyR_inv_maestro=getattr(pro_obj, 'df_lyR_maestro')
# df_new = df_lyR_inv_maestro.merge(df_src, how='left', left_index=True, right_index=True)
# df_new.to_csv(r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\sharepoint\templates\SCL_data_package_devel\SFT_lyR_deliverable_inv2_v3_0_temp.csv")