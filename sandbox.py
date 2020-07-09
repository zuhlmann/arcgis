import arcpy
# import pandas as pd
import os
from compare_data import *
from utilities import *
import copy


fp_compare_vers = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers'
fp_KRRP_project = get_path('fp_KRRP_project')
fp_KRRP_project_scratch = get_path(19)
fp_working = get_path(18)


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
# fp1 = os.path.join(get_path('fp_Klamath_Vector'), 'Project_Feature_Def_Plan/Access_Routes_DefPlan')
# fp2 = os.path.join(get_path('fp_CDM_20200428'),'Project_Data/Access_Routes')
# df = summary_data(fp1, fp2)
# pd.DataFrame.to_csv(df, '{}/{}'.format(fp_compare_vers, 'Access_Routes_Klamath_Vector_vs_CDM_20200428.csv'))
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

# # 6/2 Water Quality Map
# from utilities import *
# fp_kml_waterQ = "C:\Users\uhlmann\Box\GIS\Project_Based\Klamath_River_Renewal_MJA" \
#                     "\GIS_Request_Tracking\GIS_Requests_RES\\2020_06_02\\" \
#                     "Klamath Water Quality Stations-060120.gdb\Placemarks\Points"
#
# fp_out = os.path.join(get_path('fp_KRRP_project'), 'klam_water_qual_stations_not_pacificorp')
# fp_feat = copy.copy(fp_kml_waterQ)
# field = 'Name'
# substring = 'Station'
# # sql_statement(fp_feat, field, substring, fp_out)
# fp_selected = 'path/to/ndd'
# fp_location = fp_kml_waterQ
# fp_selected = get_path('fp_nhd')
# fp_location = copy.copy(fp_kml_waterQ)
# within_dist = 1
# fp_out = os.path.join(fp_KRRP_project, 'NHD_within_{}mile_water_qual_stations'.format(within_dist))
# select_by_location(fp_selected, 'within_a_distance', fp_location, fp_out, search_distance = '{} Miles'.format(within_dist))
#
# import arcpy
# sql_stat = "(Visibility = 5000000) AND (GNIS_NAME = 'Trinity River')"
# fp_flowline = 'C:\Users\uhlmann\Box\GIS\Project_Based\Klamath_River_Renewal_MJA\GIS_Data\\new_data_downloads\NHD_H_18010211_HU8_Shape\Shape\NHDFlowline.shp'
# arcpy.MakeFeatureLayer_management(fp_flowline, 'fp_flow', sql_stat)
# arcpy.CopyFeatures_management('fp_flow', os.path.join(fp_KRRP_project, 'NHD_H_18010211_triniteyR'))

# # 6/5/20 Water Quality Stations Map
# # Delete once map is signed off.
# def fix_names(feat):
#     with arcpy.da.
# Cursor(feat, ['Name', 'callout']) as cursor:
#         for row in cursor:
#             name = copy.copy(row[0])
#             idx = name.find('USGS')
#             if idx == -1:
#                 row[1] = name
#             else:
#                 idx_gaugeID = name.find('[') +1
#                 idx_gaugeID2 = name.find(']') -1
#                 temp = 'USGS ' + name[idx_gaugeID : idx_gaugeID2]
#                 row[1] = temp
#             cursor.updateRow(row)
#
# fp_water_gauge_not_pac = os.path.join(fp_KRRP_project, 'klam_water_qual_stations_not_pacificorp')
# fp_water_gauge_pac = os.path.join(get_path('fp_KRRP_project'), 'klam_water_qual_stations_pacificorp_only')
# # fix_names(fp_water_gauge_pac)
#
# fp_select = os.path.join(get_path(4), 'Roads_Consolidated_Draft_copy')
# fp_location = os.path.join(get_path(4), 'States_OR_CA_dissolve')
# spatial_slxn_type = 'intersect'
# fp_out = os.path.join(get_path(4), 'Roads_Consolidated_draft_intersect_OR_CA')
# select_by_location(fp_select, spatial_slxn_type, fp_location, fp_out)

# # 8) Copy all feature classes within gdb to new gdb
# arcpy.env.workspace = 'C:\Users\uhlmann\Box\GIS\Project_Based\Klamath_River_Renewal_MJA\GIS_Data\\new_data_downloads\\20200508_KRRP_Hazmat\Klamath Hazmat Data.gdb'
# feats = arcpy.ListFeatureClasses()
# # create feature paths to features
# feat_paths = [os.path.join(arcpy.env.workspace, feat) for feat in feats]
# fp_out = get_path(18)
# for fp, feat in zip(feat_paths, feats):
#     arcpy.FeatureClassToFeatureClass_conversion(fp, fp_out, feat)

# # 9) copy feature class to new location
# fp_CDM_20200428 = get_path(6)
# arcpy.env.workspace = fp_CDM_20200428
# feats = arcpy.ListFeatureClasses(feature_dataset = 'Project_Data')
# fp_dsets = [os.path.join(fp_CDM_20200428, feat) for feat in feats]
# fp_out = os.path.join(get_path(20), '2020_06_29\project_data_20200629.gdb')
# # arcpy.env.workspace = fp_CDM_20200428
# # print(fp_dsets)
# arcpy.FeatureClassToGeodatabase_conversion(fp_dsets, fp_out)

# 10) Append Special Plants layers onto each other
# # A. First output fields for both layers and cut paste into csv
# arcpy.env.workspace = fp_KRRP_project_scratch
# # https://desktop.arcgis.com/en/arcmap/latest/analyze/arcpy-classes/fieldmappings.htm
# import arcpy
#
# # Set the workspace
# arcpy.env.workspace = 'c:/base'
#
# fp_target = os.path.join(get_path(6), 'Observations\Special_Status_Plant_Pts')
# # target_feat = arcpy.CopyFeatures_management(fp_target, 'target_lyr')
# append_feat = os.path.join(fp_KRRP_project_scratch, 'Special_Status_Plants_2018_append_2019')
# fp_out = os.path.join(fp_KRRP_project_scratch)
#
# fields = arcpy.ListFields(append_feat)
# with open('C:\Users\\uhlmann\Desktop\\fields_append.txt', 'w') as f:
#     for field in fields:
#         print >> f, field.name
# B. Now run function
fp_target = os.path.join(get_path(6), 'Observations/Special_Status_Plant_Pts')
fp_append = os.path.join(get_path(19), 'Special_Status_Plants_2018_append_2019')
mapping_csv = os.path.join(get_path(5), 'dataframe_special_status_plants.csv')
fp_out = os.path.join(get_path(19), 'Special_Status_Plants_2018_2019_allFields')
field_mappings(fp_target, fp_append, mapping_csv, fp_out, True)


# # Create the required FieldMap and FieldMappings objects
# fm_type = arcpy.FieldMap()
# fm_diam = arcpy.FieldMap()
# fms = arcpy.FieldMappings()
#
# # Get the field names of vegetation type and diameter for both original
# # files
# tree_type = "Tree_Type"
# plant_type = "Plant_Type"
#
# tree_diam = "Tree_Diameter"
# plant_diam = "Diameter"
#
# # Add fields to their corresponding FieldMap objects
# fm_type.addInputField(in_file1, tree_type)
# fm_type.addInputField(in_file2, plant_type)
#
# fm_diam.addInputField(in_file1, tree_diam)
# fm_diam.addInputField(in_file2, plant_diam)
#
# # Set the output field properties for both FieldMap objects
# type_name = fm_type.outputField
# type_name.name = 'Veg_Type'
# fm_type.outputField = type_name
#
# diam_name = fm_diam.outputField
# diam_name.name = 'Veg_Diam'
# fm_diam.outputField = diam_name
#
# # Add the FieldMap objects to the FieldMappings object
# fms.addFieldMap(fm_type)
# fms.addFieldMap(fm_diam)
#
# # Merge the two feature classes
# arcpy.Merge_management([in_file1, in_file2], output_file, fms)
#
#
#
# Append_management (input, fp_out, 'NO_TEST', {field_mapping}, {subtype})
#
