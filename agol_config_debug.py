import spyder_arcgis_oop as agolZ
import utilities
import os
import sys
sys.path = [p for p in sys.path if '86' not in p]
import arcpy
import glob
import copy
import time

#debugging the purpose in Item Description - DATA_LOCATION_MC...: []

# a) basic stuff
fp_candidates = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Request_Tracking\\GIS_Requests_Management_Plans\\data_candidates_management_plans.csv'
fp_item_descriptions = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Data\\item_descriptions.csv'
fp_csv = fp_item_descriptions
agol_obj = agolZ.AgolAccess('something', fp_csv)

# # # b) Select data layers
# # # agol_obj.selection_idx(alternative_select_col = {'MANAGEMENT_PLAN':'a_team'})
# idx_to_stage = list(range(29, 261))
# index_remove = list(range(126,147))
# index_remove.append(228)
# index_remove.append(50)
# for idx in index_remove:
#     idx_to_stage.remove(idx)
#
# agol_obj.selection_idx(indices = idx_to_stage)

# consider removing NHD, contour, Parcels **all, Protected AReas, PublicLand
# # c) Copy feature class from Original Location to AGOL_DataUpload folder
fp_out = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Data\\AGOL_DataUploads\\2020_09_21\\2020_09_21'

# for indice in agol_obj.indices:
#     # NOTE - grabbing SERIES (single []) then a string is produced (.DATA_LOC...)
#     fp_original = agol_obj.df.loc[indice].DATA_LOCATION_MCM_ORIGINAL
#     # print('count: {} \n{}'.format(indice, fp_original))
#     # since this is a pd.Series, name is equivalent to index but returns a string
#     print('indice ', indice)
#     feat_name = copy.copy(indice)
#     fp_original = os.path.join(fp_original, feat_name)
#     fp_agol_staging = agol_obj.df.loc[indice].DATA_LOCATION_MCMILLEN_JACOBS
#     print('beginning FeatureClassToFeatureClass_conversion on: {}'.format(indice))
#     start = time.time()
#     arcpy.FeatureClassToFeatureClass_conversion(fp_original, fp_agol_staging, feat_name)
#     end = time.time()
#     print('{0} took {1}'.format(indice, end-start))
#
# # # ONCE IS ENOUGH!  Appending to Item D cannot be undone!
# # # agol_obj.write_xml()


# e) After checking the metadata, ZIP
utilities.zipShapefilesInDir(fp_out, '{}_zip'.format(fp_out), exclude_files = 'Streets_StateOR')
# PROBS WITH Streets_StateOR

# #f) ADD SHP TO CONTENT AGOL
# # NOTE: this will only add those in indice, therefore run selection_idx()
# snips = ['from main geodatabase compiled by AECOM provided to McMillen Jacobs on 9/11/2020']
# agol_obj.add_agol_upload(snippets = snips)

# # #g) PUBLISH
# # creates list of items adds as attribute --> user_content_<tag name>_<file type>
# tag = 'aecom_vector_gdb'
# itemType = 'shapefile'
# agol_obj.identify_items_online(itemType, tags = tag)
# items_filtered = getattr(agol_obj, 'user_content_{}_{}'.format(tag, itemType))
# for content_item in items_filtered:
#     print(content_item.name)
#     content_item.publish(output_type = 'Feature Layer')
