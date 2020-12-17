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

# # b) Select data layers
# # agol_obj.selection_idx(alternative_select_col = {'MANAGEMENT_PLAN':'a_team'})

idx_to_stage = [290]
# idx_to_stage = [birds.append(id) for id in special_status_plants]

# indices for camas review KEEP until review over 12072020
# idx_to_stage = list(range(187,199))
# index_remove = [188,190,196,198]
# idx_to_stage = list(range(215,226))
# index_remove = [220,223, 216]
# for idx in index_remove:
    # idx_to_stage.remove(idx)

agol_obj.selection_idx(indices = idx_to_stage)

# # # consider removing NHD, contour, Parcels **all, Protected AReas, PublicLand
# # # # c) Copy feature class from Original Location to AGOL_DataUpload folder
# fp_out = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Data\\AGOL_DataUploads\\2020_12_03\\2020_12_03'
# #
for indice in agol_obj.indices:
    # NOTE - grabbing SERIES (single []) then a string is produced (.DATA_LOC...)
    fp_original = agol_obj.df.loc[indice].DATA_LOCATION_MCM_ORIGINAL
    # print('count: {} \n{}'.format(indice, fp_original))
    # since this is a pd.Series, name is equivalent to index but returns a string
    print('indice ', indice)
    feat_name = copy.copy(indice)

    # fp_agol_staging = fp_out
    fp_staging = agol_obj.df.loc[indice].DATA_LOCATION_MCM_STAGING
    fp_agol_upload = agol_obj.df.loc[indice].DATA_LOCATION_MCMILLEN_JACOBS
    feat_to_copy = os.path.join(fp_original, feat_name)
    print('beginning FeatureClassToFeatureClass_conversion on: {}'.format(indice))
    start = time.time()
    # arcpy.FeatureClassToFeatureClass_conversion(fp_original + '.shp', fp_agol_staging, feat_name)
    arcpy.FeatureClassToFeatureClass_conversion(feat_to_copy, fp_staging, feat_name)
    end = time.time()
    print('{0} took {1}'.format(indice, end-start))

# # ONCE IS ENOUGH!  Appending to Item D cannot be undone!
# agol_obj.write_xml()
# agol_obj.quickie_inventory()


# # e) After checking the metadata, ZIP
# utilities.zipShapefilesInDir(fp_out, '{}_zip'.format(fp_out))
# # example of excluding problematic files
# utilities.zipShapefilesInDir(fp_out, '{}_zip'.format(fp_out), exclude_files = 'Streets_StateOR')

#f) ADD SHP TO CONTENT AGOL
# ADD same protocol for checking if already published as in g1)
# NOTE: this will only add those in indice, therefore run selection_idx()
# snips = ['Select Invasive Species data provided by BLM July 2020']
# snip1 = ['Project Features from 100 Design Package CAD'] * 2
# snip2 = ['River Alignments for post-dam Klamath, current as of Aug 2020'] * 3
# snips.extend(snip1)
# agol_obj.add_agol_upload(snippets = snips)
# #
# # #g) PUBLISH
# # g1)
# # creates list of items adds as attribute --> user_content_<tag name>_<file type>
# tag = 'Biology'
# itemType_shp = 'shapefile'
# agol_obj.identify_items_online(itemType_shp, tags = tag)
# # note feature2 works for identifying feature layers.  Not sure what Feature Layer Collection =
# itemType_feat = 'feature2'
# agol_obj.identify_items_online(itemType_feat, tags = tag)
# itemType_feat = 'feature'
# agol_obj.identify_items_online(itemType_feat, tags = tag)
# # REMOVE DICTIONARY IN FUTURE! so not to hardcode item type --> .format(tag, 'shapefile')
# shapefiles_filtered = getattr(agol_obj, 'user_content_{}_{}'.format(tag, 'shapefile'))
# features_filtered = getattr(agol_obj, 'user_content_{}_{}'.format(tag, 'Feature_Layer'))
# features_services_filtered = getattr(agol_obj, 'user_content_{}_{}'.format(tag, 'Feature_Layer_Collection'))

# # g2)
# # FIND content already published. ADD same protocol for adding shapefiles
# # get index of shapefiles already uploaded to feat
# shp_content_name = [item.title for item in shapefiles_filtered]
# feat_content_name = [item.title for item in features_filtered]
# feat_service_name = [item.title for item in features_services_filtered]
# idx_remove = []
# shp_content_lower = [item.lower() for item in shp_content_name]
# feat_content_lower = [item.lower() for item in feat_content_name]
# for idx, shp in enumerate(shp_content_lower):
#     if shp in feat_content_lower:
#         idx_remove.append(idx)
#     print('{} shapefile {}'.format(idx, shp))
#
# # idx_find = list(set(range(idx)) - set(idx_remove))
#
# shapefiles_filtered = [i for j, i in enumerate(shapefiles_filtered) if j not in idx_remove]
#
# g3)
# # finally publish
# for content_item in shapefiles_filtered:
#     print(content_item.name)
#     content_item.publish(output_type = 'Feature Layer')

# h)
# remove data
# #
# agol_obj.selection_idx(target_action = 'remove')
# # This will find all Feature Layer Collections
# agol_obj.identify_items_online('feature')
# # list of feature items from online
# feat_layers = agol_obj.user_content_Feature_Layer_Collection
# for feat_layer in feat_layers:
#     for feat_to_remove in agol_obj.indices:
#         if feat_to_remove == feat_layer.title:
#             feat_layer.delete()
#
#
#
#     agol_obj[idx].delete
