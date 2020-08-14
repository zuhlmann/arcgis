# ZRU 7/13/20
# To run this we need to be in arcgispro-py3 environment w/ GIS package:
# go to C:\\Program Files\\ArcGIS\\Pro\\bin\\Python\\Scripts and do: Start proenv.bat
# python2 to python3 compatability: https://pro.arcgis.com/en/pro-app/arcpy/get-started/python-migration-for-arcgis-pro.htm
# coding: utf-8
from __future__ import print_function, unicode_literals, absolute_import
from arcgis.gis import GIS
from arcgis.gis import Group
import os, sys
import glob
import copy
# import pandas as pd
import utilities
# import compare_data

# # since i don't have system admin rights I cannot remove python 2.7 arcpy path (Program Files 86)
# sys.path = [p for p in sys.path if '86' not in p]
# use my modules
# sys.path.append('C:\\Users\\uhlmann\\code')
# for item in sys.path:
#     print(item)
# import arcpy

# get file paths to upload
fp_table = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Data\\compare_vers\\comparison_tables\\Wetlands\\Wetlands_20191004_Vs_20190930.csv'
fp_gdb = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath\\DataReceived\\AECOM\\100719\\WetlandAndBio_GISData_20191004\\Klamath_CDM_Wetlands_20191004.gdb'
fp_out_wetlands = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Data\\AGOL_DataUploads\\2020_08_10\\2020_08_10'
fp_new_data = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Data\\new_data_downloads'

# 1) fc to folder
# compare_data.parse_gdb_dsets(fp_gdb, fp_out = fp_out_wetlands)


# 3) ADD ITEMS TO AGOL
class AgolAccess:
    '''
    Basic init for AGOL access
    '''

    def __init__(self, credentials):
        u_name = 'uhlmann@mcmjac.com'
        p_word = 'Gebretekle24!'
        setattr(self, 'mcmjac_gis',  GIS(username = u_name, password = p_word))
        print('Connected to {} as {}'.format(self.mcmjac_gis.properties.portalHostname, mcmjac_gis.users.me.username))
        self.item_type_dict = {'shp': 'shapefile', 'feature': 'Feature Layer Collection'}
    def get_group(self, group_key):
        group_dict = {'krrp_geospatial': 'a6384c0909384a43bfd91f5d9723912b',
                        'klamath_river_test': '01b12361c9e54386a955ba6e3279b09'}
        group_id = group_dict[group_Key]
        krrp_geospatial = Group(getattr(self, 'mcmjac_gis'), group_id)
        setattr(self, group_key, krrp_geospatial)

    def identify_items_online(self, itemType, **kwargs):
        # item_type_dict created in __init__
        itemType = self.item_type_dict[itemType]
        items = self.mcmjac_gis.content.search('owner: uhlmann@mcmjac.com',
                                        item_type = itemType, max_items = 300)
        setattr(self, 'user_content_{}'.format(itemType))
        # filtered tags attribute
        try:
            tags = kwargs['tags']
            items_filtered = [item for item in items if tags in item.tags]
            setattr(self, 'user_content_{}_{}'.format(tags, itemType))
        except KeyError:
            pass

    def zip_agol_upload(inDir):
        # 1) ZIP SHAPEFILES

        inDir = copy.copy(inDir)
        outDir = '{}_zip'.format(inDir)
        if os.path.exists(outDir):
            pass
        else:
            os.mkdir(outDir)
        utilities.zipShapefilesInDir(inDir, outDir)
        setattr(self, 'outDir', outDir)
    def selection_idx(self, **kwargs):
        # SELECT BY TAGS
        try:
            target_tag = kwargs['target_tag']
            # pull tags column from df (list)
            tags_from_df = self.parse_tags()
            # find index if tags are present in col (list) and if tag matches target
            iloc_tag = [idx for idx, tags in enumerate(tags_from_df) if z(isinstance(tags, list) and (target_tag in tags)]
            self.indices = iloc_tag
        except KeyError:
            # if not tags selection then indices will be     passed
            pass

        # SELECT BY ROW INDICES
        try:
            indices = kwargs['indices']
            # cast to list if not already (i.e. an int)
            # so dataframe NOT series is returned with .iloc
            if isinstance(indices, list):
                pass
            else:
                indices = [indices]
            # determine if indices were index_column vals or indices (integers)
            try:
                indices = int(indices[0])
                self.indices = df.iloc[indices].index.tolist()
            except ValueError:
                # this basically just CHECKS that the index_col vals passes EXIST
                try:
                    self.indices = df.loc[indices].index.tolist()
                except KeyError:
                    print('index_col indices are not in index.  For examples\n'
                            'check spelling of item names')
        except KeyError:
            # there should be a a key either tags or indices so delete or resoovle code somehow
            pass

    def parse_tags(self):
        # this should parse tags from csv
            # turns tags column into list.  each column is a string with commas
            tags_column = self.df.TAGS.values.tolist()
            tags_temp = []
            for tags in tags_column:
                try:
                    # i.e. tags = 'wetlands, krrc'
                    # tags.split(',') == ['wetlands', 'krrc']
                    # hence string to list
                    tags_temp.append(tags.split(','))
                except AttributeError:
                    # nans from pd.read_csv(...) are saved as floats which have
                    # no .split attribute
                    tags_temp.append(tags)
            self.tags

    def add_agol_upload(item_description_csv, select_idx, **kwargs):
        # try:
        #     title = kwargs['rename_files']
        # except KeyError:
        #     title = [dir[:-4] for dir in os.listdir(self.outDir)]
        df = pd.read_csv(item_description_csv, index_col = 'ITEM')
        # base_paths = df.loc[self.indices]['DATA_LOCATION_MCMILLEN_JACOBS'].values.tolist()
        # file_names = self.indices
        # fp_items = [os.path.join(base_path, file_name) for base_path, file_name in zip(base_paths, file_names)]

        # GET ROW INDICES OF DF TO SELECT
        # grab rows
        titles = self.indices
        # consider adding snippets to item_description.csv
        try:
            snippets = kwargs['snippets']
            # we want a list
            if isinstance(snippets, list):
                pass
            # cast as list if string
            elif isinstance(snippets, str):
                snippets = [snippets]
            # DETERMINE snippet creation based on what was pased
            # same snippet for all
            if len(indices) == 1:
                snippets = snippets * len(title)
            # custom snippets
            elif len(snippets) == len(title):
                pass
            else:
                sys.exit('len(snippet) != len(indices)')
        except:
            snippets =[None] * len(title)

        zipped_dirs = df.loc[self.indices]['DATA_LOCATION_MCMILLEN_JACOBS'].values.tolist()
        zipped_dirs = '{}_zip'.format(zipped_dirs)
        # check if they exist:
        for zip_dir in zipped_dirs:
            if os.path.exists(zip_dir):
                pass
            else:
                sys.exit('paths dont exist')
         # zipped_dir will be index title
        for idx, shp in enumerate(zipped_dirs):
            properties_dict = {'title':titles[idx],
                                'tags':tags[idx],
                                'snippet':snippets[idx]}
            fc_item = mcmjac_gis.content.add(properties_dict, data = shp)
            # fc_item.share(groups = 'a6384c0909384a43bfd91f5d9723912b')
            print('ct = {} \\n fc_item {} '.format(idx, fc_item))


# # 4) share items
# feat_layer_list = mcmjac_gis.content.search(query = 'owner: uhlmann@mcmjac.com', item_type = 'Feature Layer Collection', max_items = 50)
# target_tag = 'wetlands'
# # find features which are wetlands
# feats = [feat for feat in feat_layer_list if target_tag in feat.tags]
#
# # publishing is EASY:
# for feat in feats:
#     feat.publish()
# # sharing is EASY
# for feat in feats:
#     feat.share(groups = [krrp_geospatial])
# # for feat in feats:
# #     print(feat)


# # 4) One off eagle data
# eagle_gdb = 'eagle_features\\KlamathEagleImpactAnalysis_20200714_gdb\\KlamathEagleImpactAnalysis_20200714.gdb'
# fp_gdb = os.path.join(fp_new_data, eagle_gdb)
# fcs = ['BaldEagleTerritoryZones_20200424', 'EagleTerritoryPoints_20200415_Proj',
#     'EagleViewingLocations_20200312', 'GoldenEagleTerritoryZones_20200424',
#     'GoldenEagleViewsheds_20200114']
# fp_fcs = [os.path.join(fp_gdb, fc) for fc in fcs]
# [arcpy.FeatureClassToGeodatabase_conversion(fc, fp_out) for fc in fp_fcs]

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


# # dir(feat) from features mcmjac_gis.content.search()
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
