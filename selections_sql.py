import arcpy
import pandas as pd
import copy
import os
from utilities import *
from compare_data import select_by_location
# Base Paths
path_to_base = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/'
path_to_data_received = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/'
path_out = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/LoW_from_CAD.gdb'


# # gdb paths
# path_to_cdm_20191004 = os.path.join(path_to_data_received, 'AECOM/100719/WetlandAndBio_GISData_20191004/Klamath_CDM_20191004.gdb')
# path_to_vector= os.path.join(path_to_data_received, 'Klamath_Vector_Data.gdb')
# path_to_benji = os.path.join(path_to_data_received, 'Stantec', '20191204_ToBenji_CurrentLoWs', 'CurrentLoWs_20191204.gdb')
# path_to_cad_low = os.path.join(path_to_base, 'GIS_Data/LoW_from_CAD.gdb')
#
# # Choose workspaces and features
# path_working=copy.copy(path_to_benji)
# # set workspace
# arcpy.env.workspace=copy.copy(path_working)
#
# # CREATE SELECTION AND OUTPUT TO FEATURE CLASS
# # manually list features as opposed to ListFeatureClasses of entire gdb
# feat_names_benji=['CombinedDesign_Boundary', 'LoW_ESAPlantingZones_Restoration']
# # 1) Change whree clause manually
# where_clause_combined = '"Type" = \'Limits of Work\' AND "Current" = \'Yes\' AND "Dam" = \'JC Boyle\''
# where_clause_ESA = '"reservoir" = 'JC Boyle\''
# # 2) Select where_clause and idx
# idx=0
# where_clause = copy.copy(where_clause_combined)
#
# # Create some selections
# # 3) Change string in out_feature to reflect selection
# in_feature=os.path.join(path_to_benji, feat_names_benji[idx])
# out_feature = '{}_slxn_{}'.format(feat_names_benji[idx], 'JC_Boyle')
# out_feature = os.path.join(path_out, out_feature)
# where_clause = copy.copy(where_clause)
# arcpy.Select_analysis(in_feature, out_feature, where_clause)
#
# # Now to LoW from CAD
# # Choose workspaces and features
# path_working=copy.copy(path_to_cad_low)
# # set workspace
# arcpy.env.workspace=copy.copy(path_working)
#
# # datasets
# feat_names = ['Polygon', 'Polyline', 'MultiPatch']
# feat_FID = [46, 55, 46]
# idx = 2
# where_clause =  '"OBJECTID" = {}'.format(feat_FID[idx])
#
# # Create some selections
# # 3) Change string in out_feature to reflect selection
# in_feature=os.path.join(path_working, feat_names[idx])
# out_feature = 'KRRP_Low_CAD_to_{}'.format(feat_names[idx])
# out_feature = os.path.join(path_working, out_feature)
# arcpy.Select_analysis(in_feature, out_feature, where_clause)
#
# # Line to Polygon
# # Choose workspaces and features
# path_working=copy.copy(path_to_cad_low)
# # set workspace
# arcpy.env.workspace=copy.copy(path_working)
# line_feat = os.path.join(path_working, 'KRRP_Low_CAD_to_Polyline')
# target_feat = os.path.join(path_working, 'LoW_Polygon_from_Polyline')
#
# ct=0
# while ct < 5:
#     for coords in line_feat:
#         # arcpy.Append_management(arcpy.Polygon(arcpy.Array(arcpy.Point(*coords))), target_feat)
#         print(coords)
#         ct+=1
#
# # 4) Selections for Michaela_Transmissions   4/28/2020
# # Base Paths
# path_to_gdb = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/KRRP_Project.gdb'
# path_out = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/camas_transLines_20200422.gdb'
# scratch_workspace = 'C:/Users/uhlmann/GIS/data/scratch/scratch.gdb'
#
# path_working=copy.copy(path_out)
# arcpy.env.workspace=copy.copy(path_working)
# arcpy.env.scratchWorkspace = copy.copy(scratch_workspace)
# file_in = 'trans_lines_2019_11'
# path_in = os.path.join(path_to_gdb, file_in)
# name_temp = 'transLines_temp'
#
# # Duplicate feature and add new classification layer feature
# file_copy = arcpy.FeatureClassToFeatureClass_conversion(path_in, path_out, name_temp)
# arcpy.AddField_management(file_copy, 'layer_camas', 'text', '50') #add new field to each shapefile
#
# # new classification = target in existing layer
# pac_power_trans_demo = ['PACIFICORP SCOPE 1', 'E-EXST-TRAN-LINE-AND-POLE-DEMO', 'E-EXST-TRAN-LINE-ONLY-DEMO']
# kiewit = ['KIEWIT SCOPE 1', 'E-EXST-DIST-LINE-DEMO']
# exst_trans_remain = ['E-EXST-TRAN-LINE']
# proposed_trans_built = ['PACIFICORP PROPOSED BUILT']
# target_vals = [pac_power_trans_demo, kiewit, exst_trans_remain, proposed_trans_built]
#
# # NOT fun to read.  Just matches a list of size target_vals with repeated new_vals for zip
# # i.e. ['KIEWIT SCOPE 1', 'E-EXST-DIST-LINE-DEMO'] zips with ['kiewit_distribution_lines_demo', 'kiewit_distribution_lines_demo']
# new_vals = ['pacific_power_transmission_demo', 'kiewit_distribution_lines_demo', 'existing_transmission_lines_remain', 'proposed_transmission_lines']
# new_vals_zip=[]
# for idx, vals in enumerate(target_vals):
#     append_lst=[new_vals[idx]] * len(vals)
#     new_vals_zip.append(append_lst)
#
# # #Simply finds number of rows/features - easiest parsiomonious solution online
# # num_rows = len(list(i for i in arcpy.da.SearchCursor(file_copy, ['layer', 'layer_camas'])))
#
# ct_temp = 0
# with arcpy.da.UpdateCursor(file_copy, ['layer', 'layer_camas']) as cursor:
#     # iterate through list fields from trans_line_2019_11 begin reclassified
#     for row in cursor:
#         ct_inside = 0
#         for target_val, new_val in zip(target_vals, new_vals_zip):
#             num_targ_vals = len(target_val)
#             ct_inside += 1
#             #if layer = target val, add new classification val to new field
#             if row[0] in target_val:
#                 # print('row {} updating'.format(ct_temp))
#                 # print(row[1])
#                 row[1] = new_val[0]
#                 cursor.updateRow(row)
#                 # break inner for loop
#                 break
#             # keep going through row if nothing found
#             else:
#                 row[1]='other'
#                 cursor.updateRow(row)
# del cursor
#
# # 5.  Add a field and populate it
# file_in = 'Index_medium_zoom_copy'
# path_in = os.path.join(path_working, file_in)
# arcpy.AddField_management(path_in, 'page_num', 'text', '10') #add new field to each shapefile
#
# with arcpy.da.UpdateCursor(path_in, ['page_num']) as cursor:
#     for idx, row in enumerate(cursor):
#         row[0] = str(idx+1)
#         cursor.updateRow(row)
# del cursor
#
# # 6. Break apart feature class into new feature classes of single features for legend BS datadriven maps
# path_to_gdb = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/KRRP_Project.gdb'
# path_out = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/camas_transLines_20200422.gdb'
# scratch_workspace = 'C:/Users/uhlmann/GIS/data/scratch/scratch.gdb'
#
# path_working=copy.copy(path_out)
# arcpy.env.workspace=copy.copy(path_working)
# arcpy.env.scratchWorkspace = copy.copy(scratch_workspace)
# file_in = 'transLines_temp'
# path_in = os.path.join(path_working, file_in)
# ind_feats = new_vals = ['pacific_power_transmission_demo', 'kiewit_distribution_lines_demo', 'existing_transmission_lines_remain', 'proposed_transmission_lines']
# path_out_ind_feats=[]
# [path_out_ind_feats.append(os.path.join(path_working, ind_feat)) for ind_feat in ind_feats]
#
#
# selection = "{field} = '{val}'".format(field=field, val=val)
# arcpy.SelectLayerByAttribute_management(fc, "NEW_SELECTION", selection)
#
# field = arcpy.AddFieldDelimiters(path_in, "layer_camas")
# for feat, path_out_ind_feat in zip(ind_feats, path_out_ind_feats):
#     where_clause_camas =  "{field} = '{val}'".format(field=field, val=feat)
#     arcpy.Select_analysis(path_in, path_out_ind_feat, where_clause_camas)

#
# def where_clause_create(fp_list, field_list, val_list):
#     where_clause=[]
#     for fp, field, val in zip(fp_list, field_list, val_list):
#         field_delim = arcpy.AddFieldDelimiters(fp, field)
#         # check here and here to find code and learn unicode background:
#         # https://gis.stackexchange.com/questions/153444/using-select-layer-by-attribute-in-arcpy
#         # https://pro.arcgis.com/en/pro-app/help/data/geodatabases/overview/a-quick-tour-of-unicode.htm
#         where_clause.append("{field} = '{val}'".format(field=field_delim, val=val))
#     return where_clause
#
# def sql_selection(files_in, files_out, where_clauses):
#     for file_in, file_out, where_clause in zip(files_in, files_out, where_clauses):
#         arcpy.Select_analysis(file_in, file_out, where_clause)

# # 1) Selections with where_clause to build Vicinity Maps 5/26/20
#
# fp_klam_vect = get_path('fp_Klamath_Vector')
# fp_feat = os.path.join(fp_klam_vect, 'Transportation', 'Roads_Consolidated_Draft')
# fp_compare_vers = get_path('fp_compare_vers')
# fp_pseudo_dbase = os.path.join(get_path('fp_compare_vers'), 'Roads_Consolidated_Draft_name.csv')
# df = pd.read_csv(fp_pseudo_dbase, header = 0)
# df = df.loc[df.num_vals > 3, ['value']].dropna()
# vals_to_select = df['value'].values.tolist()
# field = arcpy.AddFieldDelimiters(fp_feat, "name")
# where_clause =  ["({field} = '{val}')".format(field=field, val=vals) for vals in vals_to_select]
# where_clause = ' OR '.join(where_clause)
# fp_out = os.path.join(fp_KRRP_project, 'Roads_Consolidated_Draft_selections_names_GT_3rows')
# arcpy.Select_analysis(fp_feat, fp_out, where_clause)

# # 2) selections Roads
# # ZRU 6/1/2020
arcpy.env.workspace = 'in_memory'
fp_roads_consolidated_draft = os.path.join(get_path('fp_KRRP_project'), 'Roads_Consolidated_Draft_copy')
fp_selected = copy.copy(fp_roads_consolidated_draft)
fp_location = get_path('fp_translines_2019_11_temp')
fp_location = copy.copy(fp_location)
fp_scratch = os.path.join(get_path('fp_scratch'), 'Roads_Consolidated_select_names_intersect_translines')
fp_out = os.path.join(get_path('fp_KRRP_project'), 'Roads_Consolidated_select_names_intersect_translines8')
field1 = arcpy.AddFieldDelimiters(fp_selected, "NAME")
field2 = arcpy.AddFieldDelimiters(fp_selected, "OBJECTID")
roads_consolidated_name = ['Copco Rd/Iron Gate Lake Rd', 'Copco Rd', 'HWY 66', 'I-5', 'US Hwy 97', 'Dagget Rd', 'Rogue River National Forest']
roads_consolidated_OBJECTID = [174, 185, 246, 333, 233]
where_clause1  =  ["({field} = '{val}')".format(field=field1, val=vals)
                                    for vals in roads_consolidated_name]
where_clause2 = ["({field} = {val})".format(field=field2, val=vals)
                                    for vals in roads_consolidated_OBJECTID]
where_clause_in_layer = where_clause1 + where_clause2
where_clause_in_layer = ' OR '.join(where_clause_in_layer)
# add these later from 20200429/Transportation/Klamath_Roads
klamath_roads_OBJID = [26936, 53020, 42384]
# basically don't select 'existing lines'
vals_trans = ['kiewit_transmission_lines_demo', 'kiewit_distribution_lines_demo',
                'pacific_power_transmission_demo', 'proposed_transmission_lines']
where_clause_trans  =  ["({field} = '{val}')".format(field='layer_camas', val=vals)
                                    for vals in vals_trans]
where_clause_trans = ' OR '.join(where_clause_trans)

arcpy.MakeFeatureLayer_management(fp_selected, 'road_lyr', where_clause_in_layer)
df_roads1 = custom_select(fp_selected, 'name', roads_consolidated_name)
df_roads2 = custom_select(fp_selected, 'OBJECTID', roads_consolidated_OBJECTID)

arcpy.MakeFeatureLayer_management(fp_location, 'location_lyr', where_clause_trans)
arcpy.MakeFeatureLayer_management(fp_selected, 'road_lyr2')
arcpy.SelectLayerByLocation_management('road_lyr2', 'intersect', 'location_lyr')

with arcpy.da.SearchCursor('road_lyr2', ['OBJECTID', 'name']) as cursor:
    # This row[0] will access teh object to grab the field.  If n fields > 1, n idx >1
    objectid, source_val = [], []
    for row in cursor:
        objectid.append(row[0])
        source_val.append(row[1])
df_loc = pd.DataFrame(np.column_stack([objectid, source_val]), columns = ['OBJECTID', 'val'],  index = objectid)
df = pd.concat([df_roads1, df_roads2, df_loc]).drop_duplicates(subset = 'OBJECTID').reset_index(drop=True)
# use this list to select features
vals_objectid = df['OBJECTID'].tolist()
where_clause_final  =  ["({field} = {val})".format(field=field2, val=vals)
                                    for vals in vals_objectid]
where_clause_final = ' OR '.join(where_clause_final)
arcpy.MakeFeatureLayer_management(fp_selected, 'road_lyr_final', where_clause_final)
arcpy.CopyFeatures_management('road_lyr_final', fp_out)

# # 2b) Select by location
# fp_KRRP_project = get_path('fp_KRRP_project')
# fp_selected = os.path.join(get_path('fp_project_working'), 'ROW\\ROW_SECDIV_Q_FRSTDIV_selected_OR_CA')
# fp_location = get_path('fp_project_clip')
# # fp_out = '{}_{}'.format(fp_KRRP_project, fp_selected.split('\\')[-1])
# fp_out = '{}_{}'.format('ROW_SECDIV_Q_FRSTDIV', 'intersect_projectArea')
# fp_out = os.path.join(fp_KRRP_project, fp_out)
# select_by_location(fp_selected, fp_location, 'intersect', fp_out)

# # At some point, figure this out and add to arcpy
# https://gis.stackexchange.com/questions/27457/including-variable-in-where-clause-of-arcpy-select-analysis
# def buildWhereClause(table, field, value):
#     """Constructs a SQL WHERE clause to select rows having the specified value
#     within a given field and table."""
#
#     # Add DBMS-specific field delimiters
#     fieldDelimited = arcpy.AddFieldDelimiters(table, field)
#
#     # Determine field type
#     fieldType = arcpy.ListFields(table, field)[0].type
#
#     # Add single-quotes for string field values
#     if str(fieldType) == 'String':
#         value = "'%s'" % value
#
#     # Format WHERE clause
#     whereClause = "%s = %s" % (fieldDelimited, value)
#     return whereClause
#
# if __name__ == "__main__":
#     inputfc = r"C:/input.shp"
#     outputfc = r"C:/output.shp"
#     fieldname = "StudyID"
#     fieldvalue = 101
#     whereclause = buildWhereClause(inputfc, fieldname, fieldvalue)
#     arcpy.Select_analysis(inputfc, outputfc, whereclause)
#
#
