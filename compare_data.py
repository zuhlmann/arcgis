# import arcpy
import copy
import pandas as pd
import os
import numpy as np
import arcpy


def path_create(data1, data2):
    parent_dirs1 = data1.split('/')[:].append('_')
    path1_components = data1.split('/')
    path2_components = data2.split('/')
    path1_components.reverse()
    path2_components.reverse()
    num_comps = min(len(path1_components), len(path2_components))
    # will yield index of shallowest file path level with unique name
    for idx, pzip in enumerate(zip(path1_components, path2_components)):
      if pzip[0]!=pzip[1]:
          break
      elif idx == num_comps -1:
          break
      else:
          pass
    # shortest unique file path with underscores
    unique1 = '_'.join(path1_components[:idx + 1])
    unique2 = '_'.join(path2_components[: idx + 1])
    new_file_name = '{}_VS_{}.csv'.format(unique1, unique2)

    return(unique1, unique2, new_file_name)

# Start comparing files
# get paths to features
# Method 1
# Manually from desired feature names list
def summary_data(feat_path1, feat_path2):
    # Check if we are passing one path to compare or multiple.  Multiple ar passed
    # as a list which is requirement for this function
    if (type(feat_path1) is list) & (type(feat_path2) is list):
        pass
    else:
        feat_path1 = [feat_path1]
        feat_path2 = [feat_path2]
    for fp1, fp2 in zip(feat_path1, feat_path2):
        # find fields added and removed and common
        fields1 = arcpy.ListFields(fp1)
        fields2 = arcpy.ListFields(fp2)
        # find common fields and those added/removed by using sets
        d1_fields_set = set([itm.name.lower() for itm in fields1])
        d2_fields_set = set([itm.name.lower() for itm in fields2])
        d1_d2_removed = list(d1_fields_set - d2_fields_set)
        d1_d2_added = list(d2_fields_set - d1_fields_set)
        common_fields = list(d2_fields_set.intersection(d1_fields_set))

        # Add feature count for each feature class
        d1_num_feat = arcpy.GetCount_management(fp1)
        d2_num_feat = arcpy.GetCount_management(fp2)

        # Make a dataframe
        unique1, unique2 = path_create(fp1, fp2)[:2]
        # initiate dataframe

        # unpack fields to be one list with comma separated using unpack_list fctn
        unique1 = [unique1]
        unique2 = [unique2]
        fields1 = unpack_list(fields1, True)
        fields2 = unpack_list(fields2, True)
        common_fields = unpack_list(common_fields, False)
        d1_d2_removed = unpack_list(d1_d2_removed, False)
        d1_d2_added = unpack_list(d1_d2_added, False)
        # create dataframe if first feature in list
        if 'df' not in locals():
            # when initiating dataframe, the string needs to be a list to generate index
            df = pd.DataFrame({'unique_d1':unique1})
            # unpack fields to be one list with comma separated using unpack_list fctn
            df['d1_fields'] = fields1
            df['d1_num_features'] = d1_num_feat
            df['unique_d2'] =unique2
            df['d2_fields'] = fields2
            df['d2_num_features'] = d2_num_feat
            df['common_fields'] = common_fields
            df['d1_d2_removed'] = d1_d2_removed
            df['d1_d2_added'] = d1_d2_added
        # now add an entire row with cols in order as above
        else:
            new_row = [unique1, fields1, d1_num_feat, unique2, fields2, d2_num_feat,
                        common_fields, d1_d2_removed, d1_d2_added]
            df.loc[len(df)] = new_row

    return(df)

def unpack_list(list_in, arcobj):
    '''
     unpacks lists
     arcobj:    bullshit because can't check custom types. Hack to say this is a wierd arcobject
    '''
    if len(list_in) > 0:
        fields_temp=[]
        for field in list_in:
            # if an arcpy featlist object
            if arcobj:
                fields_temp.append(field.name.encode('utf-8'))
            else:
                fields_temp.append(field.encode('utf-8'))
        fields_out = ', '.join(fields_temp)
    else:
        fields_out = 'NULL'
    return(fields_out)


def file_paths_arc(folder_or_gdb):
    '''
    ZRU 5/6/2020
    returns list of all paths to feature classes including path/to/featureDataset/features
    Note Will change environment temporarilly
    '''
    # get current workspace
    current_workspace = arcpy.env.workspace
    # change to specified folder
    arcpy.env.workspace = folder_or_gdb
    # find standalone features within folder, if they exist
    # NOTE have not done anything yet with standalone_feats
    standalone_feats = arcpy.ListFeatureClasses()
    dsets = [dset.encode('utf-8') for dset in arcpy.ListDatasets()]
    dset_feats=[]
    for dset in dsets:
        feats = arcpy.ListFeatureClasses(feature_dataset = dset)
        for feat in feats:
            dset_feats.append('{}/{}'.format(dset, feat.encode('utf-8')))
    return(dset_feats)


# COMPARISON FILES
# i) wetlans, riparian, etc
Wetlands = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/AECOM/100719/WetlandAndBio_GISData_20191004/Klamath_CDM_Wetlands_20191004.gdb/Copco/Copco_Wetlands'
Wetlands_Draft = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/CDM/Klamath_Wetlands_2019_DRAFT.gdb/Copco_Wetlands'
Wetlands_09302020 = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/NEW DATA DOWNLOADS/Klamath_Wetlands_09302019/Klamath_Wetlands_09302019.gdb/Copco/Copco_Wetlands'

Irongate_Wetlands = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/AECOM/100719/WetlandAndBio_GISData_20191004/Klamath_CDM_Wetlands_20191004.gdb/Iron_Gate_Wetlands'
Irongate_Wetlands_CDM = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/NEW DATA DOWNLOADS/CDM_WETLANDS_DRAFT_Iron_Gates_Stream_Channels_01-29-20/CDM_WETLANDS_DRAFT_Iron_Gate_Wetlands.shp'

Irongate_Riparian = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/AECOM/100719/WetlandAndBio_GISData_20191004/Klamath_CDM_Wetlands_20191004.gdb/Iron_Gate_Riparian'
Irongate_Riparian_CDM = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/NEW DATA DOWNLOADS/CDM_WETLANDS_DRAFT_Iron_Gates_Stream_Channels_01-29-20/CDM_WETLANDS_DRAFT_Iron_Gate_Riparian.shp'

# ii) Project_Data
dataset_BA = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/NEW DATA DOWNLOADS/temp_DRAFT_Klamath_BA_GIS_updates/DRAFT_Klamath.gdb/Project_Data'
feat_list_BA = ['DRAFT_Cut_Areas_60_Design','DRAFT_Cut_Fill_Areas_60_Design', 'DRAFT_Demolition_60_Design',
'DRAFT_Disposal_60_Design', 'DRAFT_Fill_Areas_60_Design','DRAFT_Yreka_Pipeline_Options_60_Design']

dataset_20200428 = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/NEW DATA DOWNLOADS/CDM_20200429_Current/Klamath_20200428.gdb/Project_Data'
feat_list_20200428 = ['Cut_Areas_60_Design','Cut_Fill_Areas_60_Design', 'Demolition_60_Design',
            'Disposal_60_Design', 'Fill_Areas_60_Design',
            'Yreka_Pipeline_Options_60_Design']

feat_paths_project_data_BA = []
feat_paths_project_data_20200428 = []
[feat_paths_project_data_BA.append(os.path.join(dataset_BA, feat)) for feat in feat_list_BA]
[feat_paths_project_data_20200428.append(os.path.join(dataset_20200428, feat)) for feat in feat_list_20200428]

# go through wetlands
wetlands20191004_gdb = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/AECOM/100719/WetlandAndBio_GISData_20191004/Klamath_CDM_Wetlands_20191004.gdb'
wetlands20190930_gdb = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/NEW DATA DOWNLOADS/Klamath_Wetlands_09302019/Klamath_Wetlands_09302019.gdb'

feat_paths_20191004 = file_paths_arc(wetlands20191004_gdb)
feat_paths_20190930 = file_paths_arc(wetlands20190930_gdb)

d1 = copy.copy(feat_paths_20191004)
d2 = copy.copy(feat_paths_20190930)
path_out = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers'
file_name_out = 'Wetlands_20201004_Vs_20200930.csv'

df = summary_data(d1, d2)

pd.DataFrame.to_csv(df, os.path.join(path_out, file_name_out))
