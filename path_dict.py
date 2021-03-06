import pandas as pd
import os
from utilities import *

paths_table = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers/path_list.csv'

# # INITIAL CREATION
path_to_project_base = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/'
path_to_data_received = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/'
path_out = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/LoW_from_CAD.gdb'
path_to_cdm_20191004 = os.path.join(path_to_data_received, 'AECOM/100719/WetlandAndBio_GISData_20191004/Klamath_CDM_20191004.gdb')
fp_klamath_vector= os.path.join(path_to_data_received, 'Klamath_Vector_Data.gdb')
fp_KRRP_proj = get_path('fp_KRRP_project')
fp_compare_vers = get_path('fp_compare_vers')
path_to_compare_vers = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers'
fp_index = os.path.join(fp_KRRP_proj, 'index_medium_zoom')
fp_ROW_BLM_intersect_index = os.path.join(fp_KRRP_proj, 'ROW_SECDIV_Q_FRSTDIV_selected_index')
fp_relative_parcels_master = 'Administrative/Parcels_2019_Master_Rectified'

# path_list = [path_to_project_base, path_to_data_received, path_to_cdm_20191004,
#             fp_klamath_vector, path_to_KRRP_proj, path_to_compare_vers]
# alias_list = ['fp_project_base', 'fp_DataReceived', 'fp_CDM_20191004',
#         'fp_Klamath_Vector', 'fp_KRRP_proj', 'fp_compare_vers']
# desc_list = ['Klamath_River_Renewal_MJA',
#             'DataReceived', 'CDM_20191004', 'klamath_vector', 'Zachs base gdb for AGOL',
#             'lots of tables comparing datasets']
# df = pd.DataFrame(columns = ['alias', 'desc', 'path'])
# df.iloc[:]['alias'] = alias_list
# df.iloc[:]['desc'] = desc_list
# df.iloc[:]['path'] = path_list
# pd.DataFrame.to_csv(df, paths_table)

#When we want to concatenate new rows
alias_add = 'fp_box_offline'
desc_add = 'place to copy big gdb and files like DataHD_Upload klamath_raster.gdb'
path_add = 'C:\Users\uhlmann\\box_offline'
add_table_entry(alias_add, desc_add, path_add)

# # replace entry
# alias_idx_replace = 'fp_nhd'
# replacement = os.path.join(get_path(4), 'NHD')
# replace_table_entry('path', alias_idx_replace, replacement)
