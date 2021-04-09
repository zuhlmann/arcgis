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
agol_obj = agolZ.AgolAccess('something')
tags = ['Hydrology','Land_use', 'Geology', 'Vegetation']
# # b) Select data layers
# agol_obj.selection_idx(alternative_select_col = {'MANAGEMENT_PLAN':'a_team'})
# agol_obj.selection_idx(target_tag = tags)
# using target_action ACTION col from item_desc.csv
# agol_obj.selection_idx(target_action = 'remove')

# idx_to_stage = list(range(23,37))
# idx_to_stage.extend(range(147,187))
# idx_to_stage = [birds.append(id) for id in special_status_plants]

# indices for camas review KEEP until review over 12072020
# idx_to_stage = list(range(187,199))
# index_remove = [188,190,196,198]
# index_remove = [220,223, 216]
# for idx in index_remove:
    # idx_to_stage.remove(idx)

idx_to_stage = [311,312,313]
agol_obj.selection_idx('df',indices = idx_to_stage)

# used to output csv with data items and metadata from item desc
# agol_obj.quickie_inventory()

# # # consider removing NHD, contour, Parcels **all, Protected AReas, PublicLand
# # # # c) Copy feature class from Original Location to AGOL_DataUpload folder
fp_out = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Data\\AGOL_DataUploads\\2021_03_31\\2021_03_31'
#
# for indice in agol_obj.indices:
#     # NOTE - grabbing SERIES (single []) then a string is produced (.DATA_LOC...)
#     fp_original = agol_obj.df.loc[indice].DATA_LOCATION_MCM_ORIGINAL
#     # print('count: {} \n{}'.format(indice, fp_original))
#     # since this is a pd.Series, name is equivalent to index but returns a string
#     print('indice ', indice)
#     print('fp_original', fp_original)
#     feat_name = copy.copy(indice)
#
#     # fp_agol_staging = fp_out
#     fp_staging = agol_obj.df.loc[indice].DATA_LOCATION_MCM_STAGING
#     fp_agol_upload = agol_obj.df.loc[indice].DATA_LOCATION_MCMILLEN_JACOBS
#     feat_to_copy = os.path.join(fp_original, feat_name)
#     print('beginning FeatureClassToFeatureClass_conversion on: {}'.format(indice))
#     start = time.time()
#     # arcpy.FeatureClassToFeatureClass_conversion(fp_original + '.shp', fp_agol_staging, feat_name)
#     arcpy.FeatureClassToFeatureClass_conversion(feat_to_copy, fp_agol_upload, feat_name)
#     end = time.time()
#     print('{0} took {1}'.format(indice, end-start))

# # ONCE IS ENOUGH!  Appending to Item D cannot be undone!
# agol_obj.write_xml('df')
#
# e) After checking the metadata, ZIP
utilities.zipShapefilesInDir(fp_out, '{}_zip'.format(fp_out))
# # example of excluding problematic files
# utilities.zipShapefilesInDir(fp_out, '{}_zip'.format(fp_out), exclude_files = 'Streets_StateOR')

# Protocol for new agol update ZU 20210205
# 1) get index using indices = range() or target_action = remove
# 2) identify_items_online
# 3) take_action
# agol_obj.identify_items_online()
# agol_obj.take_action('remove')

# f) ADD SHP TO CONTENT AGOL
# ADD same protocol for checking if already published as in g1)
# NOTE: this will only add those in indice, therefore run selection_idx()
snips = ['Limits of Work 100 Design Lower Klamath Project UPDATED from previous 100 Design with medium area cut out above IG dam']
snip1 = ['Disposal Sites 100 Design plus Open Water Site at Copco']
snip2 = ['Staging converted directly from 100 Design CAD']
snips.extend(snip1)
snips.extend(snip2)
# agol_obj.AgolAccess('something')
agol_obj.add_agol_upload('df', snippets = snips)
# #
# #g) PUBLISH
# g1)
# creates list of items adds as attribute --> user_content_<tag name>_<file type>
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
#
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
# # deleting features from AGOL
# matching_features = [feat_layer for feat_layer in agol_obj.user_content_Feature_Layer if feat_layer.title in agol_obj.indices]
# feature_layer.update(item_properties = {'title' = '<new_title'})
#
# # to update columns in dataframe
# df.at[<int; row idx>, <str; col name>] = 'action'
# df.at[0, 'ACTION'] = ''
#
# 1. ContentManager Module (accessed via GIS Module in my code i.e.
# mcm_gis = GIS(username, pword))
# mcm_gis.content.search('owner: uhlmann@mcmjac.com', item_type = itemType, max_items = 900))
#
# 1a. Useful properties/methods within ContentManager:
# bulk_update(itemids, properties)
# itemsids = mcmjac_gis.content.search("owner: uhlmann@mcmjac.com")
# properties = {'categories': ["limits_of_work", "project_data"]}
# mcmjac_gis.content._bulk_update(itemids, properties)
#
# 1b. check create_service for PUBLISHING!! ZU 20210205
#
# 1c. delete_items
# delete collection of items by passing list of item or itemid
#
# 1d. generate
# generate csv, shapefile or GeoJSon
#
# 1e. get(itemid)
# provide item id and return boolean if exists
#
# 1f. import_data
# import pandas df INTO ArcGIS Online
#
# 1g. share_items
# share batch of items with specified group, members, everyone, etc.


#     agol_obj[idx].delete

# # 4) GIS Random tidbits
# # print content
# krrp_content = krrp_geospatial.content()
# # string search from parse_dir
# target_content = krrp_content[5]
# print(target_content)
# target_id = target_content.id
# feature_collection = mcmjac_gis.content.get(target_id)
# fp_download = 'C:\\Users\\uhlmann\\box_offline\\test_download'
# gdb_name = 'eagle.gdb'
# result = feature_collection.export(gdb_name, 'File Geodatabase')
# result.download(fp_download)


# dir(feat) from features mcmjac_gis.content.search()
# '_ux_item_type', '_workdir', 'access', 'accessInformation', 'add_comment', 'add_relationship',
#  'appCategories', 'app_info', 'avgRating', 'banner', 'categories', 'clear', 'comments', 'content_status',
#  'copy', 'copy_feature_layer_collection', 'create_thumbnail', 'create_tile_service', 'created', 'culture',
#   'delete', 'delete_rating', 'delete_relationship', 'dependencies', 'dependent_to', 'dependent_upon',
#   'description', 'documentation', 'download', 'download_metadata', 'download_thumbnail', 'export', 'extent',
#    'fromkeys', 'get', 'get_data', 'get_thumbnail', 'get_thumbnail_link', 'groupDesignations', 'guid',
#    'homepage', 'id', 'industries', 'isOrgItem', 'itemid', 'items', 'keys', 'languages', 'largeThumbnail',
#    'layers', 'licenseInfo', 'listed', 'metadata', 'modified', 'move', 'name', 'numComments', 'numRatings',
#    'numViews', 'owner', 'ownerFolder', 'pop', 'popitem', 'properties', 'protect', 'protected', 'proxies',
#    'proxyFilter', 'publish', 'rating', 'reassign_to', 'register', 'related_items', 'resources', 'scoreCompleteness',
#    'screenshots', 'setdefault', 'share', 'shared_with', 'snippet', 'spatialReference', 'status', 'tables', 'tags',
#     'thumbnail', 'title', 'type', 'typeKeywords', 'unregister', 'unshare', 'update', 'url', 'usage', 'values']
