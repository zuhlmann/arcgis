# Resourceing after move
# FLA road improvement greengen
# 20241017
subproject='FLA_road_improvement'
prj_file = r"C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\prj_files\CA_sp_II_nad83_ft_esri102642.prj"
fp_pathlist=fp_pathlist = r"C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\df_utility_csvs\path_list_updated.csv"
aprx_str = 'aprx_FLA_road_improvement'
fp_aprx=r'C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Maps\FLA\map_docs\FLA_road_improvement\FLA_road_improvement.aprx'
fp_lyR_inv = r'C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Maps\FLA\data_inv\broken_aprx_agg3.csv'

import importlib
import spyder_arcgis_oop as agolZ
importlib.reload(sys.modules['spyder_arcgis_oop'])

# Initiaate
pro_obj = agolZ.proProject()
pro_obj.dbase_init(prj_file,subproject,fp_pathlist, use_item_desc=False)

# # A2) If need to Create
# # Create in Pro Utilities
# df_layers = pro_obj.aprx_map_inv(fp_aprx)
# df_aggregated = pro_obj.aggregate_rows(df_layers,'DATA_LOCATION_MCMILLEN', 'MAP_NAME', carry_fields=True)
# df_aggregated.to_csv(fp_lyR_inv)

# A3) After creating lyR_inv
# Can set to False if no inv yet, then set to True
pro_obj.add_aprx(fp_aprx, fp_lyR_inv,True, 'DATA_LOCATION_MCMILLEN')
pro_obj.get_base_aprx_content(aprx_str)
#
# # Create Broken Filepath Inv
# # A) Inventory broken layers
# pro_obj.aprx_broken_source_inv(aprx_str, fp_lyR_inv)

# # A2) Create fixed path column
# # Manually add 'target' and 'replace' vals for DATA_LOCATION.replace('target','replace')
# # to iterate and create DATA_LOCATION_RESOURCE
# pro_obj.selection_idx('df_FLA_road_improvement_lyR', target_action='fix')
# pro_obj.aprx_broken_source_inv2(fp_lyR_inv,'aprx_FLA_road_improvement')
#
# # # Add ReSource info
# # # pro_obj.add_df(fp_lyR_inv, 'df_greengen_ferc_lyR', 'random')
# pro_obj.selection_idx('df_FLA_road_improvement_lyR', target_action='fix')
# pro_obj.format_lyR_inv_datasource_standard('aprx_FLA_road_improvement')

# # # # Z) Create map matrix - just do once
csv_map_matrix = r'C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Maps\FLA\data_inv\map_matrix.csv'
# pro_obj.expand_rows(aprx_str, csv_map_matrix)

# D) Resource Time
# load maps
import pandas as pd
pro_obj.selection_idx('df_FLA_road_improvement_lyR', target_action='fix')
# pro_obj.get_base_aprx_content(aprx_str)
df_map_matrix = pd.read_csv(csv_map_matrix, index_col='DATA_LOCATION_MCMILLEN')
pro_obj.re_source_lyR_maestro(aprx_str, df_map_matrix)




