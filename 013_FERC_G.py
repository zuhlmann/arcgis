from utilities import *
import arcpy
import os
import copy
# import pandas as pd

# # 1) Make project area intersection
# fp_select = os.path.join(get_path(8), 'Sections_OR\CadNSDI_PLSS_web.gdb\PLSSFirstDivision')
# fp_location = os.path.join(get_path(4), 'project_clip')
# spatial_slxn_type = 'intersect'
# fp_out = os.path.join(get_path(19), 'PLSSFirstDivision_project_intersect')
# select_by_location(fp_select, spatial_slxn_type, fp_location, fp_out)
#
#
# fp_section = os.path.join(get_path(4), 'PLSS_Sections_BLM_GCD')
# fp_township = os.path.join(get_path(3), 'PLSS_Townships')
# fp_out = os.path.join(get_path(4), 'PLSS_Sections_BLM_GCD_project_corrected')
# # atts = ['OBJECTID', 'FIPS_C']
# #
# # with arcpy.da.SearchCursor(fp_or_feat, atts) as cursor:
# #     # This row[0] will access teh object to grab the field.  If n fields > 1, n idx >1
# #     objectid, source_val = [], []
# #     for row in cursor:
# #         objectid.append(row[0])
# #         source_val.append(row[1])
# # df = pd.DataFrame(np.column_stack([objectid, source_val]), columns = ['OBJECTID', 'val'],  index = objectid)
# # # arrange by FIP
#
# with arcpy.da.SearchCursor(fp_section, ['OBJECTID', 'mtrs']) as cursor:
#     # This row[0] will access teh object to grab the field.  If n fields > 1, n idx >1
#     objectid, mtrs = [], []
#     for row in cursor:
#         objectid.append(row[0])
#         mtrs.append(row[1])
# df = pd.DataFrame(np.column_stack([objectid, mtrs]), columns = ['OBJECTID', 'mtrs'])
# df = df.sort_values(by = ['mtrs'])
# objid_list = df['OBJECTID']
# mtrs_list = df['mtrs']
# objid_select = []
# previous_val = 9999
# for objid, mtrs in zip(objid_list, mtrs_list):
#     if mtrs != previous_val:
#         objid_select.append(objid)
#     else:
#         pass
#     previous_val = mtrs
# objid_select = [int(objid.encode('utf-8')) for objid in objid_select]
# where_clause_final = '"OBJECTID" IN ' + str(tuple(objid_select))
# arcpy.MakeFeatureLayer_management(fp_section, 'sections_project_corrected', where_clause_final)
# arcpy.CopyFeatures_management('sections_project_corrected', fp_out)

# 2) Making triangulation reference points

# # But first if we need to copy
# fp_in_temp = os.path.join(get_path(4), 'water_stations_CA_StatePlane_FIPS_0401')
# arcpy.FeatureClassToFeatureClass_conversion(fp_in_temp, get_path(4), 'water_stations_CA_StatePlane_FIPS_0401')

fp_water_stations = os.path.join(get_path(4), 'water_stations_CA_StatePlane_FIPS_0401')
fp_structures_pac = os.path.join(get_path(3), 'Utilities\Structures_PacifiCorp')

# 1_1water stations not pac
sheet1_1_val = [7]
sheet1_1_att = 'OBJECTID'
fp_sheet1_1 = copy.copy(fp_water_stations)
# 1_2 structures_pacificorp
sheet1_2_val = [47, 1319, 1292, 157]
sheet1_2_att = 'objectid'
fp_sheet1_2 = copy.copy(fp_structures_pac)

# CHANGE THESE VALS:
objid_select = copy.copy(sheet1_2_val)
att_select = copy.copy(sheet1_2_att)
fp_select = copy.copy(fp_sheet1_2)
feat_lyr = 'FERC_coords_sheet1_2'

fp_out = os.path.join(get_path(19), feat_lyr)
# refer to this for formating
# https://gis.stackexchange.com/questions/29735/selecting-features-by-attribute-if-in-python-list
if len(objid_select) > 1:
    substring = '"{}" IN '.format(att_select)
    where_clause_final = substring + str(tuple(objid_select))
    # where_clause_final = '"{}" IN ' + str(tuple(objid_select)).format(att_select)
else:
    print('HERE')
    print(objid_select)
    print('attselect')
    print(att_select)
    where_clause_final = '"{}" IN '.format(att_select) + '({})'.format(objid_select[0])
arcpy.MakeFeatureLayer_management(fp_select, feat_lyr, where_clause_final)
arcpy.CopyFeatures_management(feat_lyr, fp_out)
