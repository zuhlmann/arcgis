import pandas as pd
import os

# CREATE

path_to_project_base = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/'
path_to_data_received = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/'
path_out = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/LoW_from_CAD.gdb'
path_to_cdm_20191004 = os.path.join(path_to_data_received, 'AECOM/100719/WetlandAndBio_GISData_20191004/Klamath_CDM_20191004.gdb')
path_to_klamath_vector= os.path.join(path_to_data_received, 'Klamath_Vector_Data.gdb')
path_to_KRRP_proj = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/KRRP_Project.gdb'
path_to_compare_vers = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers'

path_list = [path_to_project_base, path_to_data_received, path_to_cdm_20191004,
            path_to_klamath_vector, path_to_KRRP_proj, path_to_compare_vers]
key_list = ['fp_project_base', 'fp_DataReceived', 'fp_cdm_20191004',
        'fp_klamath_vector', 'fp_KRRP_proj', 'fp_compare_vers']
desc_list = ['Klamath_River_Renewal_MJA',
            'DataReceived', 'CDM_20191004', 'klamath_vector', 'Zachs base gdb for AGOL',
            'lots of tables comparing datasets']
df = pd.DataFrame(columns = ['path', 'desc'], index = key_list)
df.iloc[:]['desc'] = desc_list
df.iloc[:]['path'] = path_list
print(df.loc[:]['desc'])
pd.DataFrame.to_csv(df, os.path.join(df.loc['fp_compare_vers']['path'], 'path_list.csv'))
