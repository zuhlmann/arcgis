import arcpy
import utilities
import copy
import os

fp_copy_to_scratch = os.path.join(utilities.get_path(6), 'Project_Data/Cut_Fill_Areas_60_Design')
fp_scratch =  utilities.get_path(19)

low_feat = 'LoW_60_v2_scratch'
cut_fill = 'Cut_Fill_Areas_60_Design_scratch'
access_route = 'Access_Routes_scratch'
access_route_buffer = 'Access_Routes_Buffer'
# copy working feats to scratch gdb
# arcpy.FeatureClassToFeatureClass_conversion(fp_copy_to_scratch, fp_scratch, cut_fill)
merge_feat = access_route

fp_access_route = os.path.join(fp_scratch, access_route)
fp_access_route_buffer = os.path.join(fp_scratch, access_route_buffer)
utilities.buffer_and_create_feat(fp_access_route, fp_access_route_buffer, "15 feet", dissolve_option = 'ALL')
# arcpy.FeatureClassToFeatureClass_conversion(fp_copy_to_scratch, fp_scratch, merge_feat)
# arcpy.env.workspace = copy.copy(fp_scratch)
#
# fieldMappings = arcpy.FieldMappings()
#
# fieldMappings.addTable(low_feat)
# fieldMappings.addTable(merge_feat)
#
# fldMap_merge_feat = arcpy.FieldMap()
# att_list_access = ['label', 'descriptio', 'road_type']
# for att in att_list_access:
#     fldMap_merge_feat.addInputField(merge_feat, att)
#
# att_rename_list = copy.copy(att_list_access)
# merge_feat_info = fldMap_merge_feat.outputField
# for att_name in att_rename_list:
#     merge_feat_info.name = att_name
# fldMap_merge_feat.outputField = merge_feat_info
# fieldMappings.addFieldMap(fldMap_merge_feat)
#
# for field in fieldMappings.fields:
#     if field.name not in att_rename_list + ['Shape_Len', 'Shape_Area']:
#         fieldMappings.removeFieldMap(fieldMappings.findFieldMapIndex(field.name))
#
# new_feat = 'LoW_Access_Routes.shp'
# arcpy.Merge_management([low_feat, merge_feat], new_feat, fieldMappings)
#
# #new feature in scratch location
# fp_new = os.path.join(fp_scratch, new_feat)
# # fp to final project gdb locatoin
# fp_working_LoW = os.path.join(utilities.get_path('fp_working'), 'LoW')
# new_feat_name = 'LoW_CutFill_Draft90Design_20200623'
# arcpy.FeatureClassToFeatureClass_conversion(fp_new, fp_working_LoW, new_feat_name)
