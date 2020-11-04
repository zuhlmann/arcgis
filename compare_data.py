
import copy
import pandas as pd
import os
import numpy as np
import sys
# sys.path = [p for p in sys.path if '86' not in p]
# sys.path.append('C:\Program Files\ArcGIS\Pro\Resources\ArcPy')
# sys.path.append('C:\Program Files\ArcGIS\Pro\Resources\ArcToolBox\Scripts')
# sys.path.append('C:\Program Files\ArcGIS\Pro\\bin\Python')
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
    '''
    ARGS
    feat_path1      self explanatory
    feat_path2      self explanatory
    RETURNS
    df              returns but does not save dataframe
    '''
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
    ZRU 5/6/2020. Updated (shittilly) on 10/13/2020.  Jerry rigged for my purposes
    not very robust
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
                fields_temp.append(field.name)
            # Needs work.  If not string don't encode
            else:
                if isinstance(field, str):
                    fields_temp.append(field)
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
    # change to specified folder
    arcpy.env.workspace = folder_or_gdb
    # find standalone features within folder, if they exist
    # NOTE have not done anything yet with standalone_feats
    # standalone_feats = arcpy.ListFeatureClasses()
    # dsets = [dset.decode('utf-8') for dset in arcpy.ListDatasets()]
    # # note python 2.7 likes:
    dsets = [dset for dset in arcpy.ListDatasets()]
    path_to_dset = []
    path_to_feat = []
    feats_df = []
    dsets_df =[]
    for dset in dsets:
        feats = arcpy.ListFeatureClasses(feature_dataset = dset)
        for feat in feats:
            print(feat)
            path_to_dset.append('{}//{}'.format(folder_or_gdb, dset))
            if want_df:
                # append feat name
                feats_df.append(feat)
                # repeat dset name for every feature layer within it
                dsets_df.append(dset)
                # returns a dataframe for manually comparing tables with changed feature names
                path_to_feat.append(os.path.join(folder_or_gdb, dset, feat))
            else:
                df = 'FIX LATER'
    if want_df:
        df = pd.DataFrame(np.column_stack([feats_df, dsets_df, path_to_feat]),
                            columns = ['feature_name', 'feature_dataset', 'fp_feat'])
    return(df)
    print(df)

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

def select_by_location(fp_select, spatial_slxn_type, fp_location, fp_out, **kwargs):
    '''
    select features within boundary and output as new feature class
    ZRU 5/27/2020
    ARGS:
    fp_select           file path to feature being locationally selected
    spatial_slxn_typ    'intersect'
    fp_location         file path to feature location is referenced to - kind've the clip feature
    fp_out              file path out
    '''
    arcpy.MakeFeatureLayer_management(fp_select, 'in_lyr')
    arcpy.MakeFeatureLayer_management(fp_location, 'location_lyr')
    if spatial_slxn_type.lower() == 'within_a_distance':
        arcpy.SelectLayerByLocation_management('in_lyr', spatial_slxn_type, 'location_lyr', kwargs['search_distance'])
    elif spatial_slxn_type.lower() == 'intersect':
        arcpy.SelectLayerByLocation_management('in_lyr', spatial_slxn_type, 'location_lyr')
    arcpy.CopyFeatures_management('in_lyr', fp_out)

def select_by_attribute(fp_in, atts, ):
    arcpy.SelectLayerByAttribute_management()

def sql_statement(fp_feat, field, substring, fp_out):
    '''
    ZRU 6/3/2020
    One day this will all be organized.  Expand to allow multiple fields and
    substrings
    ARGS
    df          dataframe from feature class
    field       field to search for substrings
    substring   substring
    '''
    from utilities import list_unique_fields
    df = list_unique_fields(fp_feat, field)
    val = df[field][~df[field].str.contains(substring)].tolist()
    # diff sql statement conventions for diff val types
    if isinstance(val[0], int):
        sql_sub = ','.join([str(val) for val in val])
    elif (isinstance(val[0], str)) or (isinstance(val[0], unicode)):
        sql_sub = ','.join(["'" + str(val) + "'" for val in val])
    sql_statement = '"{}" in ({})'.format(field, sql_sub)
    arcpy.MakeFeatureLayer_management(fp_feat, 'feat_lyr')
    arcpy.SelectLayerByAttribute_management('feat_lyr', 'ADD_TO_SELECTION', sql_statement)
    arcpy.CopyFeatures_management('feat_lyr', fp_out)

def parse_gdb_dsets(fp_gdb, **kwargs):
    '''
    similiar to file_paths_arc function here but didn't want to spend time
    assimilating them.  Used for gdb with datasets.  Unpacks, creates file path
    for all feature classes.  Option to create shapefiles
     Saves in folder specified as shapfiles individually
    - note will add option to detect all datasets from gdb using arcpy.
    ZRU 7/23/2020

    ARGS:
    fp_gdb          file path (string) to geodatabase of interest
    fp_out          file path (string) to save shapefiles
    **kwargs        only option is datasets which = list of strings - names of datasets
                    if no dataset kwarg is passed then all datasets within gdb
                    are used
    RETURNS:
    fcs_names       returns a list of feature class names (sans path)
    '''
    arcpy.env.workspace = copy.copy(fp_gdb)

    # datasets can be passed as a list or selected wholesale from gdb
    try:
        dsets = kwargs['dsets']
    except KeyError:
        dsets = arcpy.ListDatasets()

    # file paths created to feature classes i.e. fp_gdb/dataset/fc_name
    fp_fcs = []
    # grab and flatten all names sans root path
    fcs_names =[]
    for dset in dsets:
        # print('dset: {}'.format(dset))
        fcs = arcpy.ListFeatureClasses(feature_dataset = dset)
        [fp_fcs.append('{}\\{}\\{}'.format(fp_gdb, dset, fc)) for fc in fcs]
        fcs_names.append(fcs)
    # Convert to shapefiles in specified file path
    fcs_names = [item for sublist in fcs_names for item in sublist]
    for name in fcs_names:
        print('name fc:  {}'.format(name))

    # save to shapefile if fp_out passed kwarg
    try:
        fp_out = kwargs['fp_out']
        for fp_fc in fp_fcs:
            # feature_name + .shp extension
            shp_name = '{}.shp'.format(fp_fc.split('\\')[-1])
            # create shapefiles from fc and output to AGOL data_upload folder
            arcpy.FeatureClassToFeatureClass_conversion(fp_fc, fp_out, shp_name)
    except KeyError:
        pass
    # return fcs_names
    return(fcs_names)
