# append and field mapping script
import os
import utilities
import arcpy
import copy
import pandas as pd

# https://gis.stackexchange.com/questions/328425/understanding-and-using-fieldmapping-with-arcpy
# Beast of way append/merge multiple datasets while dealing with field mappings
# First create csv with all feats, then run meat of funciton using csv
# Used to create Disposal Sites 12/18/2020 ZRU

fp_working = utilities.get_path(18)
fp_gis_data = utilities.get_path(23)
fp_cdm = utilities.get_path(6)
fp_in = os.path.join(fp_working, 'Project_Data//staging_60des')
fp_out_csv = os.path.join(fp_gis_data, 'compare_vers//field_mapping_tables/temp.csv')
fp_cp = os.path.join(fp_working, 'Project_Data//disposal_site_copco2_phouse_tailrace_copy')
fp_ig = os.path.join(fp_working, 'Project_Data//disposal_site_IG_powerhouse_tailrace_copy')
fp_jcb_forebay = os.path.join(fp_working, 'staging_jcb_forebay_digitized')

# UTILITY TO REMOVE FIELDS ONCE MAYHEIM is over 12/18/2020
# arcpy.env.workspace = os.path.join(fp_working, 'Project_Data')
# fp_project_data = os.path.join(fp_working, 'Project_Data')
# temp = [os.path.join(fp_project_data, p) for p in arcpy.ListFeatureClasses()]
# df = pd.DataFrame(temp, columns = ['feature_class'])
# pd.DataFrame.to_csv(df, os.path.join(fp_gis_data, 'compare_vers//field_mapping_tables/temp.csv'))

# # UTILITY TO REMOVE FEATURE CLASSES
# fcn = ['Staging_100_{}'.format(idx) for idx in list(range(12))]
# fc_path = [os.path.join(fp_working, 'Project_Data//{}'.format(nm)) for nm in fcn]
#
# for fc in fc_path:
#     if arcpy.Exists(fc):
#         print('DELETEING {}'.format(fc))
#         arcpy.Delete_management(fc)


# utilities.return_fields(fp_jcb_forebay, fp_out_csv)

# scratch field mappings
# arcpy.env.workspace = os.path.join(utilities.get_path(18), 'Project_Data')
fp_staging_60 = copy.copy(fp_in)
fp_csv = os.path.join(fp_gis_data, 'compare_vers//field_mapping_tables//staging_100des.csv')

# data type reads in as L if don't set explicitly
df = pd.read_csv(fp_csv, dtype = {'feature_id':int})

fc_list = [fp_staging_60, fp_jcb_forebay]
# initiate empty list to accumulate lyr names
target_lyr_name_list = []
for id, fc in enumerate(fc_list):
    # make append layer
    if id == 0:
        arcpy.MakeFeatureLayer_management(fc, 'append_lyr')
    # create additional target layers
    else:
        target_lyr_name = 'target_lyr{}'.format(id)
        arcpy.MakeFeatureLayer_management(fc, target_lyr_name)
        target_lyr_name_list.append(target_lyr_name)
# add append_lyr to list
all_lyrs = ['append_lyr'] + target_lyr_name_list

# arbitrary ids
feature_id = list(df.feature_id)
# should just be basically range(num_fcs)
feature_id_unique = set(feature_id)
# yields a dataframe
append_df = df[df.feature_id == 0]
append_mapping_set = set(append_df.mapping)
# drop na because empty cells because na
all_fields_set = set(df.mapping.dropna())
all_fields_list = list(all_fields_set)

all_fields_orig = set(df.original_field.dropna())
# remove fields from schema
remove_fields = all_fields_orig.intersection(all_fields_set)
remove_fields = all_fields_orig - remove_fields

# this gets the row indices for first occurence of field
all_fields_indices = [df.mapping.eq(f).idxmax() for f in all_fields_list]

# now let's find which lyr this is
all_fields_feature_id = [df.iloc[id].feature_id for id in all_fields_indices]

# list of lists - one per lyr with ALL Fields for each
field_obj_list = [[f_list for f_list in arcpy.ListFields(lyr)] for lyr in all_lyrs]
# now pull just ListField item for first occurence in lyr list
for id, field_name in zip(all_fields_feature_id, all_fields_list):
    field_obj_matched = field_obj_list[id]
    # temp = [f for field_obj_temp if f.name == field_name][0]
    for f in field_obj_matched:
        if f.name == field_name:
            #initiate dict
            if 'dict1' not in locals():
                dict1 = {field_name: f}
            # After dict is initiated
            else:
                dict1[field_name] = f
        else:
            pass

# Add missing fields to each feature class
for id in feature_id_unique:
    df_temp = df[df.feature_id == id]
    lyr_fields = set(df_temp.mapping)
    add_fields = all_fields_set- lyr_fields
    for field in list(add_fields):
        fobj = dict1[field]
        print('FEATURE: {} \n adding field: {}\n'.format(all_lyrs[id], fobj.name))
        arcpy.AddField_management(all_lyrs[id], fobj.name, fobj.type, fobj.precision,
                                        fobj.scale, fobj.length, fobj.aliasName,
                                        fobj.isNullable, fobj.required)

# Not sure this is the best protocol
# BUT 1) create new empty feature class with existing schema.
# 2) delete fields not included
# from here (listed at top too):
fp_out = os.path.join(fp_working, 'Project_Data')
fc_name = 'Staging_100_11'
print('Creating New Feature Class\n')

# half ass way to add appendix if feature already exists
try:
    arcpy.CreateFeatureclass_management(fp_out, fc_name, 'POLYGON', template = all_lyrs[0])
    # pass
except arcpy.ExecuteError:
    id_last = fc_name.rfind('_') + 1
    append_num = int(fc_name[id_last:]) + 1
    fc_name = fc_name[:id_last] + str(append_num)
    arcpy.CreateFeatureclass_management(fp_out, fc_name, 'POLYGON', template = all_lyrs[0])

fp_fc = os.path.join(fp_out, fc_name)

# remove fields from schema
#obviously must retain required fields
required_list = ['Shape', 'Shape_Area', 'Shape_Length', 'OBJECTID', 'Shape_Are', 'Shape_Len',
                'Shape__Len', 'Shape__Are', 'SHAPE']
# required_list = [item.lower() for item in required_list]
print('the resuired list before anything', required_list)
print('the removed list before anything', list(remove_fields))

# try with sets
# create lower case required
required_set = set([item.lower() for item in required_list])
# values that overlap
# lower case remove
remove_fields_lc = set([item.lower() for item in list(remove_fields)])
remove_fields_lc = remove_fields_lc - remove_fields_lc.intersection(required_set)

remove_fields_clean = []
for item in list(remove_fields):
    if item.lower() in remove_fields_lc:
        remove_fields_clean.append(item)

# now delete
print('THESE ARE REMOVE FIELDS:\n{}'.format('\n'.join(remove_fields_clean)))
arcpy.DeleteField_management(fp_fc, remove_fields_clean)
# start adding rows to new feat class
icur = arcpy.da.InsertCursor(fp_fc, all_fields_list + ['SHAPE@'])

for lyr in all_lyrs:
    with arcpy.da.SearchCursor(lyr, all_fields_list + ['SHAPE@']) as cursor:
        print('insert row for: {}'.format(lyr))
        for row in cursor:
            icur.insertRow(row)
del icur

not sure the order of del icur and copyfeatures
