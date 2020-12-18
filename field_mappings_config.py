# append and field mapping script
import os
import utilities
import arcpy
import copy
import pandas as pd

# https://gis.stackexchange.com/questions/328425/understanding-and-using-fieldmapping-with-arcpy
# Beast of way append/merge multiple datasets while dealing with field mappings
# First create csv with all feats, then run meat of funciton using csv
fp_working = utilities.get_path(18)
fp_gis_data = utilities.get_path(23)
fp_cdm = utilities.get_path(6)
fp_in = os.path.join(fp_working, 'Project_Data//Disposal_60_Design_CDM')
fp_out_csv = os.path.join(fp_gis_data, 'compare_vers//field_mapping_tables/temp.csv')
fp_cp = os.path.join(fp_working, 'Project_Data//disposal_site_copco2_phouse_tailrace_copy')
fp_ig = os.path.join(fp_working, 'Project_Data//disposal_site_IG_powerhouse_tailrace_copy')
fp_out = os.path.join(fp_working, 'Project_Data//disposal_100')

# utilities.return_fields(fp_ig, fp_out_csv)

# scratch field mappings
# arcpy.env.workspace = os.path.join(utilities.get_path(18), 'Project_Data')
fp_disposal_60 = copy.copy(fp_in)
fp_csv = os.path.join(fp_gis_data, 'compare_vers//field_mapping_tables//disposal_sites_100des.csv')

# data type reads in as L if don't set explicitly
df = pd.read_csv(fp_csv, dtype = {'feature_id':int})

fc_list = [fp_cp, fp_ig, fp_disposal_60]
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
# this gets the row indices for first occurence of field
all_fields_indices = [df.mapping.eq(f).idxmax() for f in all_fields_list]

# now let's find which lyr this is
all_fields_feature_id = [df.iloc[id].feature_id for id in all_fields_indices]

for id, name in zip(all_fields_indices, all_fields_feature_id):
    print('row id {}, feat id {}'.format(id, name))
# list of lists - one per lyr with ALL Fields for each
field_obj_list = [[f_list for f_list in arcpy.ListFields(lyr)] for lyr in all_lyrs]
# now pull just ListField item for first occurence in lyr list
for id, field_name in zip(all_fields_feature_id, all_fields_list):
    field_obj_matched = field_obj_list[id]
    # temp = [f for field_obj_temp if f.name == field_name][0]
    for f in field_obj_matched:
        if f.name == field_name:
            #initiate dict
            print('-----', f.name)
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
    print('lyr: {}\nadd fields: {}\n'.format(all_lyrs[id], add_fields))
    print('id {}'.format(id))
    for field in list(add_fields):
        fobj = dict1[field]
        print('FEATURE: {} \n adding field: {}\n'.format(all_lyrs[id], fobj.name))
        arcpy.AddField_management(all_lyrs[id], fobj.name, fobj.type, fobj.precision,
                                        fobj.scale, fobj.length, fobj.aliasName,
                                        fobj.isNullable, fobj.required)

icur = arcpy.da.InsertCursor(all_lyrs[0], all_fields_list + ['SHAPE@'])

for lyr in all_lyrs[1:]:
    with arcpy.da.SearchCursor(lyr, all_fields_list + ['SHAPE@']) as cursor:
        print('insert row for: {}'.format(lyr))
        for row in cursor:
            icur.insertRow(row)
del icur

# not sure the order of del icur and copyfeatures
arcpy.CopyFeatures_management(all_lyrs[0], fp_out)
