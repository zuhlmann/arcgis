
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
def summary_data(feat_path1, feat_path2):
    # Check if we are passing one path to compare or multiple.  Multiple ar passed
    # as a list which is requirement for this function
    if (type(feat_path1) is list) & (type(feat_path2) is list):
        pass
    else:
        feat_path1 = [feat_path1]
        feat_path2 = [feat_path2]
    for fp1, fp2 in zip(feat_path1, feat_path2):
        feat1 = fp1.split('/')[-1]
        feat2 = fp2.split('/')[-1]
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

        # unpack fields to be one list with comma separated using unpack_list fctn
        # needs to be list like obj
        fields1 = unpack_list(fields1, True)
        fields2 = unpack_list(fields2, True)
        common_fields = unpack_list(common_fields, False)
        d1_d2_removed = unpack_list(d1_d2_removed, False)
        d1_d2_added = unpack_list(d1_d2_added, False)
        # create dataframe if first feature in list
        if 'df' not in locals():
            df = pd.DataFrame({'feature_1':[feat1]})
            # when initiating dataframe, the string needs to be a list to generate index
            df['d1_path'] = fp1
            # unpack fields to be one list with comma separated using unpack_list fctn
            df['d1_fields'] = fields1
            df['d1_num_features'] = d1_num_feat
            df['feature_2'] = feat2
            df['d2_path'] =fp2
            df['d2_fields'] = fields2
            df['d2_num_features'] = d2_num_feat
            df['common_fields'] = common_fields
            df['d1_d2_removed'] = d1_d2_removed
            df['d1_d2_added'] = d1_d2_added
        # now add an entire row with cols in order as above
        else:
            new_row = [feat1, fp1, fields1, d1_num_feat, feat2, fp2, fields2, d2_num_feat,
                        common_fields, d1_d2_removed, d1_d2_added]
            # add new row to dataframe
            df.loc[len(df)] = new_row

    return(df)

def unpack_list(list_in, arcobj):
    '''
    ZRU 5/6/2020
    unpacks lists
    ARGS:
    arcobj:    bullshit because can't check custom types. Bool = True if list_in is arcobject
    RETURNS:
    fields_out: list converted into 'item, item2, item3' for item in list_in
    '''
    if len(list_in) > 0:
        fields_temp=[]
        for field in list_in:
            # if an arcpy featlist object
            if arcobj:
                fields_temp.append(field.name.encode('utf-8'))
            # Needs work.  If not string don't encode
            else:
                if isinstance(field, basestring):
                    fields_temp.append(field.encode('utf-8'))
            # isinstance does not work on int
                else:
                    fields_temp.append(str(field))
        fields_out = ', '.join(fields_temp)
    # if list blank, then set to NULL
    else:
        fields_out = 'NULL'
    return(fields_out)


def file_paths_arc(folder_or_gdb, want_df):
    '''
    ZRU 5/6/2020
    returns list of all paths to feature classes including path/to/featureDataset/features
    Note Will change environment temporarilly
    ARGS:
    folder_or_gdb       Currently designed for a gdb
    want_df                  boolean - if True, output dataframe
    RETURNS:
    path_to_dset_feats          list of paths/to/dataset/feature
    '''
    # get current workspace
    current_workspace = arcpy.env.workspace
    # change to specified folder
    arcpy.env.workspace = folder_or_gdb
    # find standalone features within folder, if they exist
    # NOTE have not done anything yet with standalone_feats
    standalone_feats = arcpy.ListFeatureClasses()
    dsets = [dset.encode('utf-8') for dset in arcpy.ListDatasets()]
    path_to_dset_feats = []
    feats_df = []
    dsets_df =[]
    for dset in dsets:
        feats = arcpy.ListFeatureClasses(feature_dataset = dset)
        for feat in feats:
            feat = feat.encode('utf-8')
            path_to_dset_feats.append('{}/{}/{}'.format(folder_or_gdb, dset, feat))
            if want_df:
                # append feat name
                feats_df.append(feat)
                # repeat dset name for every feature layer within it
                dsets_df.append(dset)
                # returns a dataframe for manually comparing tables with changed feature names
                df = pd.DataFrame({'dataset':dsets_df, 'feature':feats_df})
            else:
                df = 'FIX LATER'
    return(path_to_dset_feats, df)

def intersection_feats(path_to_dset_feats1, path_to_dset_feats2):
    '''
    ZRU 5/7/2020
    For finding intersections in path/to/gdb/dataset/feature in to
    path_to_features lists i.e. CDM_20191004 vs. CDM_Draft
    ARGS:
    path_to_dset_feats1     path list gdb1
    path_to_dset_feats2     path list gdb2
    RETURNS:
    feat_list1              intersection paths (common paths
    feat_list2              intersection paths (common paths)
    '''
    dset_feat1 = []
    dset_feat2 = []
    path1_gdb = []
    path2_gdb = []
    for path in path_to_dset_feats1:
        path1_components = path.split('/')
        dset_feat1.append('/'.join(path1_components[-2:]))
    for path in path_to_dset_feats2:
        path2_components = path.split('/')
        dset_feat2.append('/'.join(path2_components[-2:]))
    set1 = set(dset_feat1)
    set2 = set(dset_feat2)
    common_dset_feats = list(set1.intersection(set2))
    path1_gdb = '/'.join(path1_components[:-2])
    path2_gdb = '/'.join(path2_components[:-2])
    feat_paths1 = []
    feat_paths2 = []
    [feat_paths1.append(os.path.join(path1_gdb, dset_feat)) for dset_feat in common_dset_feats]
    [feat_paths2.append(os.path.join(path2_gdb, dset_feat)) for dset_feat in common_dset_feats]
    return (feat_paths1, feat_paths2)

def select_by_location(fp_in, fp_location, spatial_slxn_type, fp_out):
    '''
    select features within boundary and output as new feature class
    ZRU 5/27/2020
    ARGS:
    fp_in               file path to feature being locationally selected
    fp_location         file path to feature location is referenced to - kind've the clip feature
    fp_out              file path out
    '''
    arcpy.MakeFeatureLayer_management(fp_in, 'in_lyr')
    arcpy.MakeFeatureLayer_management(fp_location, 'location_lyr')
    arcpy.SelectLayerByLocation_management('in_lyr', spatial_slxn_type, 'location_lyr')
    arcpy.CopyFeatures_management('in_lyr', fp_out)
