# import arcpy
# import pandas as pd
import os
from compare_data import *
import copy

# # COMPARISON FILES
# BASE PATHS
fp_CDM_20191004 = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/AECOM/100719/WetlandAndBio_GISData_20191004/Klamath_CDM_20191004.gdb'
fp_Klamath_20200428 = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/NEW DATA DOWNLOADS/CDM_20200429_Current/Klamath_20200428.gdb'
fp_Klamath_CDM_20191004 = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/AECOM/100719/WetlandAndBio_GISData_20191004/Klamath_CDM_20191004.gdb'
fp_klamath_vector = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/Klamath_Vector_Data.gdb'
fp_compare_vers = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers'

# # i) wetlans, riparian, etc
# Wetlands = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/AECOM/100719/WetlandAndBio_GISData_20191004/Klamath_CDM_Wetlands_20191004.gdb/Copco/Copco_Wetlands'
# Wetlands_Draft = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/CDM/Klamath_Wetlands_2019_DRAFT.gdb/Copco_Wetlands'
# Wetlands_09302020 = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/NEW DATA DOWNLOADS/Klamath_Wetlands_09302019/Klamath_Wetlands_09302019.gdb/Copco/Copco_Wetlands'
#
# Irongate_Wetlands = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/AECOM/100719/WetlandAndBio_GISData_20191004/Klamath_CDM_Wetlands_20191004.gdb/Iron_Gate_Wetlands'
# Irongate_Wetlands_CDM = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/NEW DATA DOWNLOADS/CDM_WETLANDS_DRAFT_Iron_Gates_Stream_Channels_01-29-20/CDM_WETLANDS_DRAFT_Iron_Gate_Wetlands.shp'
#
# Irongate_Riparian = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/AECOM/100719/WetlandAndBio_GISData_20191004/Klamath_CDM_Wetlands_20191004.gdb/Iron_Gate_Riparian'
# Irongate_Riparian_CDM = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/NEW DATA DOWNLOADS/CDM_WETLANDS_DRAFT_Iron_Gates_Stream_Channels_01-29-20/CDM_WETLANDS_DRAFT_Iron_Gate_Riparian.shp'
#
# # ii) Project_Data
# dataset_BA = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/NEW DATA DOWNLOADS/temp_DRAFT_Klamath_BA_GIS_updates/DRAFT_Klamath.gdb/Project_Data'
# feat_list_BA = ['DRAFT_Cut_Areas_60_Design','DRAFT_Cut_Fill_Areas_60_Design', 'DRAFT_Demolition_60_Design',
# 'DRAFT_Disposal_60_Design', 'DRAFT_Fill_Areas_60_Design','DRAFT_Yreka_Pipeline_Options_60_Design']
#
# dataset_20200428 = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/NEW DATA DOWNLOADS/CDM_20200429_Current/Klamath_20200428.gdb/Project_Data'
# feat_list_20200428 = ['Cut_Areas_60_Design','Cut_Fill_Areas_60_Design', 'Demolition_60_Design',
#             'Disposal_60_Design', 'Fill_Areas_60_Design',
#             'Yreka_Pipeline_Options_60_Design']
#
# feat_paths_project_data_BA = []
# feat_paths_project_data_20200428 = []
# [feat_paths_project_data_BA.append(os.path.join(dataset_BA, feat)) for feat in feat_list_BA]
# [feat_paths_project_data_20200428.append(os.path.join(dataset_20200428, feat)) for feat in feat_list_20200428]
#
# # iii) wetlands
# wetlands20191004_gdb = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/AECOM/100719/WetlandAndBio_GISData_20191004/Klamath_CDM_Wetlands_20191004.gdb'
# wetlands20190930_gdb = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/NEW DATA DOWNLOADS/Klamath_Wetlands_09302019/Klamath_Wetlands_09302019.gdb'
# wetlands_2019_draft = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/CDM/Klamath_Wetlands_2019_DRAFT.gdb'
# feat_paths_wetlands_20191004 = file_paths_arc(wetlands20191004_gdb, False)[0]
# # feat_paths_wetlands_20190930 = file_paths_arc(wetlands20190930_gdb, False)[0]
# feat_paths_wetlands_2019_draft = file_paths_arc(wetlands_2019_draft, False)[0]
# feat_paths_wetlands_20191004, feat_paths_wetlands_2019_draft = intersection_feats(feat_paths_wetlands_20191004, feat_paths_wetlands_2019_draft)

# # iv) CDM Datasets
# Klamath_20200428 = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/NEW DATA DOWNLOADS/CDM_20200429_Current/Klamath_20200428.gdb'
# Klamath_CDM_20191004 = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/AECOM/100719/WetlandAndBio_GISData_20191004/Klamath_CDM_20191004.gdb'

# # FIRST we need ONLY features that are matched to both dates because later CDM_Klamath datasets added data and changed names
# # Semi-supervised creation of table with features and matching features of Klamath gdbs
# Klamath_feature_file = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers/Features_Klamath_CDM_20191004.csv'
# # read in csv and get to work
# fp_compare_vers = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers'
# df = pd.read_csv(os.path.join(fp_compare_vers, 'Features_Klamath_CDM_20200428_20191004.csv'))
# df_clean = df.dropna()
# dset_clean = df_clean['dataset']
# feats1_clean = df_clean['feature_20191004']
# feats2_clean = df_clean['feature_20200428']
# # features from both datsets that are matched; names differ but n features1 = n features2
# feat_paths_Klamath_20191004 = ['{}/{}/{}'.format(Klamath_CDM_20191004, dset, feats) for dset, feats in zip(dset_clean, feats1_clean)]
# feat_paths_Klamath_20200428 = ['{}/{}/{}'.format(Klamath_20200428, dset, feats) for dset, feats in zip(dset_clean, feats2_clean)]

# # # vi) one offs
# feat_path_low1 = os.path.join(fp_Klamath_20200428, 'Observations/Osprey_Observations')
# feat_path_low2 = os.path.join(fp_klamath_vector, 'Biology_SurveyData2018/Osprey_Observations')
# feat_path1 = copy.copy(feat_path_low1)
# feat_path2 = copy.copy(feat_path_low2)
# df = summary_data(feat_path1, feat_path2)
# pd.DataFrame.to_csv(df, '{}/{}'.format(fp_compare_vers, 'Osprey_Observations_KlamathVector_vs_20200428.csv'))
# # Pretty sure delete
# # # pre cleaned feat paths to find added and/or removed
# # # original path/to/dataset/feat
# # feat_paths_Klamath_20191004_orig = file_paths_arc(Klamath_CDM_20191004, False)[0]
# # feat_paths_Klamath_20200428_orig = file_paths_arc(Klamath_20200428, False)[0]
# # set_20200428_orig = set(feat_paths_Klamath_20200428_orig)
# # set_20200428 = set(feat_paths_Klamath_20200428)
# # added = set_20200428_orig - set_20200428



# # v)
# klamath_vector = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/Klamath_Vector_Data.gdb'

# vi) Borings
# Borings_20201004 = '{}{}'.format(fp_CDM_20191004, '/Project_Data/Borings')
# project_data in Klamath_20200428
# geology in klamath_vector.g

# # Finally
# # # Summarize differences gdb
# d1 = copy.copy(feat_paths_Klamath_20200428)
# d2 = copy.copy(feat_paths_Klamath_20191004)
# # #
# df = summary_data(d1, d2)
# #
# # # OR, list gdb contents
# # # df = file_paths_arc(klamath_vector, True)[1]
# #
# fp_compare_vers = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers'
# fp_database_contents = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers/database_contents'

# df = pd.read_csv(os.path.join(path_out, 'Features_Klamath_CDM_20200428_20190930.csv'))
# print(df.dropna().shape)

# # 6) create shapefiles in bulk
# fp_temp = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/camas_transLines_20200422.gdb/'
# dset = 'transLines_categories'
# arcpy.env.workspace = fp_temp
# feats = arcpy.ListFeatureClasses()
#
# scratch_dir = copy.copy('C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/AGOL_DataUploads/scratch')
# if not os.path.exists(scratch_dir):
#     os.mkdir('C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/AGOL_DataUploads/scratch')
# arcpy.FeatureClassToShapefile_conversion(feats, scratch_dir)

# # 7) 5/26/20 inventory attributes
# # Seedlings of database creation.  List unique values using attribe_values function
# from utilities import *
# paths_table = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers/path_list.csv'
# path_key = 'fp_ROW_BLM_intersect_index'
# fp_feat = os.path.join(get_path('fp_KRRP_project'), 'ROW_SECDIV_Q_FRSTDIV_from_camas_intersect_projectArea')
# fp_out = get_path('fp_compare_vers')
# include_fields = ['Cust_NM']
# attribute_inventory(fp_feat, fp_out, False, include_fields)

# 6/2 DELETE!   just decomposing a function for diagnosis
from utilities import *
fp_roads_consolidated_draft = os.path.join(get_path('fp_KRRP_project'), 'Roads_Consolidated_Draft_copy')
fp_selected = copy.copy(fp_roads_consolidated_draft)
print([obj.name for obj in arcpy.ListFields(fp_selected)])
with arcpy.da.SearchCursor(fp_selected, ['OBJECTID', 'name']) as cursor:
    # This row[0] will access teh object to grab the field.  If n fields > 1, n idx >1
    name = [row[1] for row in cursor]
    print(name)
