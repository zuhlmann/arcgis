import arcpy
import pandas as pd



# def path_create(data1, data2):
#   parent_dirs1 = data1.split('/')[:].append('_')
#   path1_components = data1.split('/')
#   path2_components = data2.split('/')
#   path1_components.reverse()
#   path2_components.reverse()
#   num_comps = min(len(path1_components), len(path2_components))
#   sent = 1
#   for idx, pzip in enumerate(zip(path1_components, path2_components)):
#       if pzip[0]!=pzip[1]:
#           break
#       elif idx == num_comps -1:
#           break
#       else:
#           pass
#   # shortest unique file path with underscores
#   unique1 = '_'.join(path1_components[:idx + 1])
#   unique2 = '_'.join(path2_components[: idx + 1])
#   new_file_name = '{}_VS_{}.csv'.format(unique1, unique2)
#
#   return(unique1, unique2, new_file_name)

# can we save text and nums in list to df
path_out = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers/test.csv'
d2 = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/CDM/Klamath_Wetlands_2019_DRAFT.gdb/Copco_Wetlands'
d1 = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/AECOM/100719/WetlandAndBio_GISData_20191004/Klamath_CDM_Wetlands_20191004.gdb/Copco_Wetlands'

# unique1, unique2, combined = path_create(d1, d2)

# d1_num_feat = arcpy.GetCount_management(d1)
feat_obj = arcpy.ListFields(d1)
feat_obj2 = arcpy.ListFields(d2)

test = [isinstance(feat, arcpy.arcobjects.arcobjects.Field) for feat in feat_obj]
print(test)
# df = pd.DataFrame({'unique1':list(unique1)})
# df = pd.DataFrame({'num_count': [d1_num_feat]})
