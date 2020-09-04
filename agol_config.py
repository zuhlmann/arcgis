import spyder_arcgis_oop as agolZ
import utilities
import os
import sys
sys.path = [p for p in sys.path if '86' not in p]
# import arcpy
import glob


# 1) Basic upload
# # INITIATE
# fp_item_descriptions = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Data\\item_descriptions.csv'
# fp_candidates = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Request_Tracking\\GIS_Requests_Management_Plans\\data_candidates_management_plans.csv'
# fp_csv = fp_candidates
# agol_obj = agolZ.AgolAccess('something', fp_csv)
#
# # GROUP
# agol_obj.get_group('krrp_geospatial')
#
# # # # SEARCH FILES ONLINE
# # # itemType = 'shapefile'
# # # agol_obj.identify_items_online(itemType, tags = 'eagles')
# # # print(agol_obj.user_content_eagles_shapefile)
# #
# zip_test = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Data\\AGOL_DataUploads\\2020_08_13\\2020_08_13'
# agol_obj.zip_agol_upload(zip_test)
#
# # select by tags
# agol_obj.selection_idx(target_tag = ['eagles', 'test'])
# print(agol_obj.indices)
#
# # # select by indices
# # agol_obj.selection_idx(indices = [1,2,3,5,9,21])
# # print(agol_obj.indices)

# # publish
# snip = 'testing if my class works'
# agol_obj.add_agol_upload(snippets = snip)

# 2) Example of adding new metadata
# agol_obj = agolZ.metaData()
# agol_obj = agolZ.AgolAccess('something')
# agol_obj.selection_idx(indices = [21,22])
# # agol_obj.zip_agol_upload()
# snips = ['FERC boundaries from 2017.  Still valid as of Aug 2020. However will' +
#         'be edited soon', 'Limit of Work 60Design for KRRP']
# agol_obj.add_agol_upload(snippets = snips)


# # 3) testing oop
# import testClass as oop
# object1 = oop.inheritanceClass()
# print('my name is {} my bday is {}'.format(object1.name, object1.bday))
# print(object1.square(5))

# # COPY FEATURES TO NEW PATH AS SHP
# # gdb feature to shapefils --> zip
# shp_name = 'Public_Lands'

# REAL EXAMPLE) Protocol for preparing data for managment plans start to finish
# a) basic stuff
fp_candidates = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Request_Tracking\\GIS_Requests_Management_Plans\\data_candidates_management_plans.csv'
fp_csv = fp_candidates
agol_obj = agolZ.AgolAccess('something', fp_csv)

# b) Select data layers
# agol_obj.selection_idx(alternative_select_col = {'MANAGEMENT_PLAN':'a_team'})
# agol_obj.selection_idx(indices = list(range(3,35)))

# # c) Copy feature class from Original Location to AGOL_DataUpload folder
# fp_out = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Data\\AGOL_DataUploads\\2020_08_31\\2020_08_31'
#
# for indice in agol_obj.indices:
#     # NOTE - grabbing SERIES (single []) then a string is produced (.DATA_LOC...)
#     fp_original = agol_obj.df.loc[indice].DATA_LOCATION_ORIGINAL
#     # print('count: {} \n{}'.format(indice, fp_original))
#     # since this is a pd.Series, name is equivalent to index but returns a string
#     feat_name = indice
#     fp_original = os.path.join(fp_original, feat_name)
#     arcpy.FeatureClassToFeatureClass_conversion(fp_original, fp_out, feat_name)

# # d) assemble purpose OR in this case add to existing
# purp_dict = {'DATA_LOCATION_MCMILLEN_JACOBS':fp_out}
# agol_obj.write_xml(add_lines_purp = purp_dict)

# # e) After checking the metadata, ZIP
# utilities.zipShapefilesInDir(fp_out, '{}_zip'.format(fp_out))

# #f) ADD SHP TO CONTENT AGOL
# # NOTE: this will only add those in indice, therefore run selection_idx()
# snips = ['Data item to be evaluated for use in Management Plan figures']
# agol_obj.add_agol_upload(snippets = snips)

# #g) PUBLISH
# creates list of items adds as attribute --> user_content_<tag name>_<file type>
agol_obj.identify_items_online('shapefile', tags = 'management_plan')
items_filtered = agol_obj.user_content_management_plan_shapefile
for content_item in items_filtered:
    print(content_item.name)
    content_item.publish(output_type = 'Feature Layer')


# # ADD GROUP
# users_list = ['Jeremy.DelPrete@stantec.com_stantec',
#                 'jeff.comstock@stantec.com_stantec',
#                 'jonathan.ricketts@stantec.com_stantec',
#                 'bernadette.bezy@stantec.com_stantec']
# agol_obj.krrp_geospatial.invite_users(users_list)
