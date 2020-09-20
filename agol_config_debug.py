import spyder_arcgis_oop as agolZ
import utilities
import os
import sys
sys.path = [p for p in sys.path if '86' not in p]
import arcpy
import glob

#debugging the purpose in Item Description - DATA_LOCATION_MC...: []

# a) basic stuff
fp_candidates = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Request_Tracking\\GIS_Requests_Management_Plans\\data_candidates_management_plans.csv'
fp_item_descriptions = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Data\\item_descriptions.csv'
fp_csv = fp_item_descriptions
agol_obj = agolZ.AgolAccess('something', fp_csv)

# b) Select data layers
# agol_obj.selection_idx(alternative_select_col = {'MANAGEMENT_PLAN':'a_team'})
agol_obj.selection_idx(indices = [23, 24])

# c) Copy feature class from Original Location to AGOL_DataUpload folder
fp_out = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Data\\AGOL_DataUploads\\2020_09_18\\2020_09_18'
for indice in agol_obj.indices:
    # NOTE - grabbing SERIES (single []) then a string is produced (.DATA_LOC...)
    fp_original = agol_obj.df.loc[indice].DATA_LOCATION_MCM_ORIGINAL
    # print('count: {} \n{}'.format(indice, fp_original))
    # since this is a pd.Series, name is equivalent to index but returns a string
    feat_name = indice
    fp_original = os.path.join(fp_original, feat_name)
    arcpy.FeatureClassToFeatureClass_conversion(fp_original, fp_out, feat_name)


# e) After checking the metadata, ZIP
utilities.zipShapefilesInDir(fp_out, '{}_zip'.format(fp_out))

# #f) ADD SHP TO CONTENT AGOL
# # NOTE: this will only add those in indice, therefore run selection_idx()
# snips = ['Right of Ways uploaded for Camas']
# agol_obj.add_agol_upload(snippets = snips)
#
# # #g) PUBLISH
# # creates list of items adds as attribute --> user_content_<tag name>_<file type>
# tag = 'row'
# itemType = 'shapefile'
# agol_obj.identify_items_online(itemType, tags = tag)
# items_filtered = getattr(agol_obj, 'user_content_{}_{}'.format(tag, itemType))
# for content_item in items_filtered:
#     print(content_item.name)
#     content_item.publish(output_type = 'Feature Layer')
