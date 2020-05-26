import pandas as pd
import os
from utilities import *

paths_table = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers/path_list.csv'
# INITIAL CREATION

path_to_project_base = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/'
path_to_data_received = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/'
path_out = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/LoW_from_CAD.gdb'
path_to_cdm_20191004 = os.path.join(path_to_data_received, 'AECOM/100719/WetlandAndBio_GISData_20191004/Klamath_CDM_20191004.gdb')
path_to_klamath_vector= os.path.join(path_to_data_received, 'Klamath_Vector_Data.gdb')
path_to_KRRP_proj = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/KRRP_Project.gdb'
path_to_compare_vers = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers'

path_list = [path_to_project_base, path_to_data_received, path_to_cdm_20191004,
            path_to_klamath_vector, path_to_KRRP_proj, path_to_compare_vers]
alias_list = ['fp_project_base', 'fp_DataReceived', 'fp_CDM_20191004',
        'fp_Klamath_Vector', 'fp_KRRP_proj', 'fp_compare_vers']
desc_list = ['Klamath_River_Renewal_MJA',
            'DataReceived', 'CDM_20191004', 'klamath_vector', 'Zachs base gdb for AGOL',
            'lots of tables comparing datasets']
df = pd.DataFrame(columns = ['alias', 'desc', 'path'])
df.iloc[:]['alias'] = alias_list
df.iloc[:]['desc'] = desc_list
df.iloc[:]['path'] = path_list
pd.DataFrame.to_csv(df, paths_table)

# When we want to concatenate new rows
alias_add = 'fp_CDM_20200428'
desc_add = 'CDM 20200428 from data verification request'
path_add = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/NEW DATA DOWNLOADS/CDM_20200429_Current/Klamath_20200428.gdb'

df = add_table_entry(paths_table, alias_add, desc_add, path_add)
pd.DataFrame.to_csv(df, paths_table)
