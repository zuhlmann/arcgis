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
  sent = 1
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
    # grab feat name
    feat_names = [feat_path1[-1], feat_path2[-1]]

    # find fields added and removed and common
    fields1 = arcpy.ListFields(feat_path1)
    fields2 = arcpy.ListFields(feat_path2)
    d1_fields_set = set([itm.name.lower() for itm in fields1])
    d2_fields_set = set([itm.name.lower() for itm in fields2])
    d1_d2_removed = list(d1_fields_set - d2_fields_set)
    d1_d2_added = list(d2_fields_set - d1_fields_set)
    common_fields = list(d2_fields_set.intersection(d1_fields_set))


    # Add feature count for each feature class
    d1_num_feat = arcpy.GetCount_management(feat_path1)
    d2_num_feat = arcpy.GetCount_management(feat_path2)

    # Make a dataframe
    unique1, unique2 = path_create(feat_path1, feat_path2)[:2]
    # when initiating dataframe, the string needs to be a list to generate index
    df = pd.DataFrame({'unique_d1':[unique1]})
    df['unique_d2'] = [unique2]
    # unpack fields to be one list with comma separated using unpack_list fctn
    df['d1_fields'] = unpack_list(fields1, True)
    df['d1_num_features'] = d1_num_feat
    df['d2_fields'] = unpack_list(fields2, True)
    df['d2_num_features'] = d2_num_feat
    df['common_fields'] = unpack_list(common_fields, False)
    df['d1_d2_removed'] = unpack_list(d1_d2_removed, False)
    df['d1_d2_added'] = unpack_list(d1_d2_added, False)

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

# Strip unicode

def strip_unicode(val_list):
    my_values_stripped, my_values_stripped_lower = [], []
    for val_uni in val_list:
        try:
            my_values_stripped_lower.append(val_uni.encode('utf-8').lower())
            my_values_stripped.append(val_uni.encode('utf-8'))  # to use in dataframe
        except AttributeError:
            pass
    return my_values_stripped_lower, my_values_stripped

Copco_Wetlands = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/AECOM/100719/WetlandAndBio_GISData_20191004/Klamath_CDM_Wetlands_20191004.gdb/Copco_Wetlands'
Copco_Wetlands_Draft = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/CDM/Klamath_Wetlands_2019_DRAFT.gdb/Copco_Wetlands'

Irongate_Wetlands = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/AECOM/100719/WetlandAndBio_GISData_20191004/Klamath_CDM_Wetlands_20191004.gdb/Iron_Gate_Wetlands'
Irongate_Wetlands_CDM = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/NEW DATA DOWNLOADS/CDM_WETLANDS_DRAFT_Iron_Gates_Stream_Channels_01-29-20/CDM_WETLANDS_DRAFT_Iron_Gate_Wetlands.shp'

Irongate_Riparian = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/AECOM/100719/WetlandAndBio_GISData_20191004/Klamath_CDM_Wetlands_20191004.gdb/Iron_Gate_Riparian'
Irongate_Riparian_CDM = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/NEW DATA DOWNLOADS/CDM_WETLANDS_DRAFT_Iron_Gates_Stream_Channels_01-29-20/CDM_WETLANDS_DRAFT_Iron_Gate_Riparian.shp'


d1 = copy.copy(Irongate_Riparian)
d2 = copy.copy(Irongate_Riparian_CDM)
path_out = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers'

comp_file_name = path_create(d1, d2)[2]
comp_file_name = os.path.join(path_out, comp_file_name)

df = summary_data(d1, d2)

pd.DataFrame.to_csv(df, os.path.join(path_out, '{}.csv'.format(comp_file_name)))
