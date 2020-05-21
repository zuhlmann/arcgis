
# import fnmatch
# import copy
# import pandas as pd
# import numpy as np
# import os
# from compare_data_utilities import add_path_multiIndex
# from compare_data import *
# from utilities import *
# import arcpy

# base_dataReceived = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived'
# klamath_vector = os.path.join(base_dataReceived, 'Klamath_Vector_Data.gdb')
# base_new_data = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/NEW DATA DOWNLOADS'

# # 1) NAVITATING DIRECTORIES
# folder = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/'
# folder2 = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/AGOL_DataUploads'
# # # get folders with potential shapefiles or gdb
# # contents = os.listdir(folder)
# # valid_folders = [str for str in contents if '.' not in str]
# # [valid_folders.append(str) for str in contents if '.gdb' in str]
# # for valid_folder in valid_folders:
#
# test_folder = os.path.join(folder2, 'CDM')
# startdir=copy.copy(folder)
#
# res = []
# for here, dirs, files in os.walk(startdir, topdown=True):
#     if here.endswith('.gdb'):
#         res.append(here)
#     elif any([file.endswith('.prj') for file in files]):
#         res.append(here)
# print(res)


# # 2) DATAFRAME SELECT BY BOOL
# # find added and removed to Klamath_CDM gdb
# # ZRU 5/8/2020
# path_to_compare_vers = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers'
# df_in = 'Features_Klamath_CDM_20200428_20191004.csv'
# df = pd.read_csv(os.path.join(path_to_compare_vers, df_in), index_col = 0)
# # access col with name
# df_added = df.loc[df.loc[:,'feature_20191004'].isnull()]
# df_removed = df.loc[df.loc[:,'feature_20200428'].isnull()]
# df_out_added = 'Features_Klamath_CDM_20200428_20191004_added.csv'
# df_out_removed = 'Features_Klamath_CDM_20200428_20191004_removed.csv'
# pd.DataFrame.to_csv(df_added, os.path.join(path_to_compare_vers, df_out_added))
# pd.DataFrame.to_csv(df_removed, os.path.join(path_to_compare_vers, df_out_removed))

# # 3) MULTIINDEXING Examples of Indexing
# index = pd.MultiIndex.from_product([['LoW', 'LoW2','Low3'], ['kentucky', 'albuquerque']], names = ['first', 'second'])
# data = np.arange(2 * 6).reshape((6,2))
# df = pd.DataFrame(data, index = index, columns = ['col1', 'col2'])
#
# # multiindexing from: https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html
# # go to section 'Advanced indexing with hierarchical index'
# print(df.loc[('LoW2','kentucky')])
# # and with specific cols
# print(df.loc[('LoW2', 'kentucky'), 'col1'])
# # exact same output for both, but df.loc is more explicit; better coding practice
# print(df.loc['LoW':'LoW2'])
# print(df['LoW':'LoW2'])
#
# # Example from https://jakevdp.github.io/PythonDataScienceHandbook/03.05-hierarchical-indexing.html
# index = [('California', 2000), ('California', 2010),
#          ('New York', 2000), ('New York', 2010),
#          ('Texas', 2000), ('Texas', 2010)]
# populations = [33871648, 37253956,
#                18976457, 19378102,
#                20851820, 25145561]
# pop = pd.Series(populations, index=index)
#
# index = pd.MultiIndex.from_tuples(index)
#
# pop = pop.reindex(index)
#
# pop_df = pd.DataFrame({'total': pop,
#                        'under18': [9267089, 9284094,
#                                    4687374, 4318033,
#                                    5906301, 6879014]})
# print(pop_df['New York':'Texas'])
#
# 3b) Multi-level APPLIED
# # NOT NEEDED ANYMORE - How dframes were created and multiindex stuff
# category = ['wetlands', 'ferc', 'transmission']
# fp_trans_lines = """C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/
#                     GIS_Data/camas_transLines_20200422.gdb"""
# fp_trans_line2 = """C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/Klamath_Vector_Data.gdb/
#                 Project_Feature_Def_Plan/Transmission_Lines_DefPlan"""
# fp_wetlands = """C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/AECOM/
#                 100719/WetlandAndBio_GISData_20191004/Klamath_CDM_20191004.gdb"""
# fp_ferc = """C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/Klamath_Vector_Data.gdb/
#                 Boundaries/FERC_Project_Footprint"""
#

# multiI = pd.MultiIndex.from_product([category, ['loc1', 'loc2']])
# path_to = pd.DataFrame([fp_wetlands, None, fp_ferc, None, fp_trans_lines, fp_trans_line2], index = multiI)

# path_out = 'C:/Users/uhlmann/Desktop/test.csv'
# # pd.DataFrame.to_csv(path_to, 'C:/Users/uhlmann/Desktop/test.csv')
#
# path_inventory = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/KRRP_GIS_Data_Priority_List_ArcGIS_Online_copy.csv'
# # df_read_multiI = pd.read_csv(path_inventory, skipfooter=1, index_col=[0,1])
# df_read = pd.read_csv(path_inventory, skipfooter=2, index_col = 0)
# # print(df_read.index.values)
# df_read = df_read.loc[[itm2 for itm in df_read.index.values for itm2 in [itm, itm]]]
# # ser = pd.Series({'Locations':['loc1', 'loc1'] * (len(df_read)/2)})
# # df_read['Locations'] = [item2 for iter in range(len(df_read)/2) for item2 in ['loc1', 'loc2']]
# loc_vals = ['loc1', 'loc2'] * 26
# df_read.insert(0, 'Locations', loc_vals)
# # pd.DataFrame.to_csv(df_read, path_out)

# # 4) Build inventory df and csv
# fp_dataReceived = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived'
# klamath_vector = os.path.join(fp_dataReceived, 'Klamath_Vector_Data.gdb')
# base_new_data = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/NEW DATA DOWNLOADS'
# fp_compare_vers = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers'
# file_inventory = 'KRRP_GIS_Data_Priority_List_ArcGIS_Online_working.csv'
# fp_inventory =os.path.join(fp_compare_vers, file_inventory)
# # read in csv as multindex
# df = pd.read_csv(fp_inventory, index_col = [0,1])
# # grab level labels for confirmation and fun
# print(df.index.get_level_values(0)[2]=='FERC Boundary')
# df.loc[('FERC Boundary', 'loc2'), 'Original_Location']
# # How we add a path via dataframes
# df = add_path_multiIndex(df, 'FERC Boundary', 2, 'test', True)
# # # basic get indices as array of condition
# # # Note that dataframes cols are decomposed into series, so once cols are selected
# # # i.e. df['col_name'] then operate on as a series
# df1 = df.iloc[np.where(df['Uploaded']=='5/14/2020')]
# # paths to features for date uploaded
# paths_list = df1['Original_Location'].tolist()
# path_list_temp = []
# for path in paths_list:
#     # if a gdb NOT a feature class, list out feature layers
#     if path[-3:]== 'gdb':
#         feat_paths_within_gdb = file_paths_arc(path, False)[0]
#         # [path_list_temp.append(feat_paths) for feat_paths in feat_paths_within_gdb]
#         [path_list_temp.append(feat_paths.split('/')[-1]) for feat_paths in feat_paths_within_gdb]
#     else:
#         path_list_temp.append(path)
# for path in path_list_temp:
#     print(path)
# gdb_out = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/AGOL_DataUploads/2020_05_addDate/2020_05_14.gdb'
# items = [item for item in path_list_temp]
# for path in items[6:]:
#     arcpy.FeatureClassToGeodatabase_conversion (path, gdb_out)
from utilities import *
show_table()
path = get_path(0)
print(path)
