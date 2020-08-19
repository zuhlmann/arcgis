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
import pandas as pd
import utilities


class AgolAccess:
    '''
    Basic init for AGOL access
    '''

    def __init__(self, credentials):
        '''
        need to add credentials like a key thing.  hardcoded currently
        '''
        u_name = 'uhlmann@mcmjac.com'
        u_name2 = 'zuhlmann@mcmjac.com'
        p_word = 'Gebretekle24!'
        p_word2 = 'Mcmjac081'
        setattr(self, 'mcmjac_gis',  GIS(username = u_name2, password = p_word2))
        print('Connected to {} as {}'.format(self.mcmjac_gis.properties.portalHostname, self.mcmjac_gis.users.me.username))
        # dictionary that can be expanded upon
        self.item_type_dict = {'shapefile': 'shapefile', 'feature': 'Feature Layer Collection'}
        # move this eventually
        self.df = pd.read_csv('C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Data\\item_descriptions.csv',  index_col = 'ITEM')
    def get_group(self, group_key):
        '''
        hardcoded. update if more groups become necessary.
        '''
        group_dict = {'krrp_geospatial': 'a6384c0909384a43bfd91f5d9723912b',
                        'klamath_river_test': '01b12361c9e54386a955ba6e3279b09'}
        group_id = group_dict[group_key]
        krrp_geospatial = Group(getattr(self, 'mcmjac_gis'), group_id)
        setattr(self, group_key, krrp_geospatial)

    def identify_items_online(self, itemType, **kwargs):
        '''
        find items already online
        '''
        # item_type_dict created in __init__
        itemType = self.item_type_dict[itemType]
        items = self.mcmjac_gis.content.search('owner: uhlmann@mcmjac.com',
                                        item_type = itemType, max_items = 300)
        setattr(self, 'user_content_{}'.format(itemType), items)
        # filtered tags attribute
        try:
            tags = kwargs['tags']
            items_filtered = [item for item in items if tags in item.tags]
            setattr(self, 'user_content_{}_{}'.format(tags, itemType), items_filtered)
        except KeyError:
            pass

    def zip_agol_upload(self, inDir):
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
        '''
        use item_descriptions.csv tags to find indices OR pass integer
        indices.  Use kwargs to indicate type
        '''
        # SELECT BY TAGS
        try:
            target_tag = kwargs['target_tag']
            # list will be passed for multiple target tags
            if not isinstance(target_tag, list):
                target_tag = [target_tag]
            # pull tags column from df (list)
            self.parse_tags()
            # find index if tags are present in col (list) and if tag matches target
            # iloc_tag = [idx for idx, tags in enumerate(tags_from_df) for val_targ in target_tag if (isinstance(tags, list)) and (val_targ in tags)]
            iloc_temp = []
            for target in target_tag:
                ct = 0
                try:
                    for tags in self.tags_from_df:
                        print('if {}(type = {}) in {}'.format(target, type(target), tags))
                        if target in tags:
                            iloc_temp.append(ct)
                        ct += 1
                except TypeError:
                    ct += 1
            print(iloc_temp)
            iloc_tag = list(set(iloc_temp))
            # get index names from iloc vals
            self.indices = self.df.iloc[iloc_tag].index.tolist()
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
            # If indices passed were integers
            try:
                int(indices[0])
                print('indices {}'.format(indices))
                self.indices = self.df.iloc[indices].index.tolist()
            # If indices were index_column vals (stirng)
            except ValueError:
                try:
                    self.indices = self.df.loc[indices].index.tolist()
                #Check that the index_col vals passes EXIST
                except KeyError:
                    print('index_col indices are not in index.  For examples\n'
                            'check spelling of item names')
        except KeyError:
            # there should be a a key either tags or indices so delete or resoovle code somehow
            pass

    def parse_tags(self):
        '''
        takes string from tags column and parse into list of strings
        '''
        tags_column = self.df.TAGS.values.tolist()
        tags_temp = []
        for tags in tags_column:
            try:
                # i.e. tags = 'wetlands, krrc'
                # tags.split(',') == ['wetlands', ' krrc']
                # tag.strip(' ') removes leading space for tags after position 1 (idx 0)
                # hence string to list
                tags_temp.append([tag.strip(' ') for tag in tags.split(',')])
            except AttributeError:
                # nans from pd.read_csv(...) are saved as floats which have
                # no .split attribute
                tags_temp.append(tags)
        self.tags_from_df = tags_temp

    def add_agol_upload(self, **kwargs):
        '''
        currently passing snippets as kwarg but could be drawn from column in
        csv in future.  shapefiles need to be zipped and in file structure
        before using this.
        '''
        # try:
        #     title = kwargs['rename_files']
        # except KeyError:
        #     title = [dir[:-4] for dir in os.listdir(self.outDir)]
        # base_paths = df.loc[self.indices]['DATA_LOCATION_MCMILLEN_JACOBS'].values.tolist()
        # file_names = self.indices
        # fp_items = [os.path.join(base_path, file_name) for base_path, file_name in zip(base_paths, file_names)]
        titles = self.indices

        # tags
        try:
            tags = self.tags_parsed
        except AttributeError:
            self.parse_tags()
            tags= self.tags_from_df

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
            snippets =[None] * len(titles)

        # need indices from self.selection_idx
        upload_folders = self.df.loc[self.indices]['DATA_LOCATION_MCMILLEN_JACOBS'].values.tolist()
        parent_zip_folder = ['{}_zip'.format(upload_folder) for upload_folder in upload_folders]
        zipped_folders = [os.path.join(zip_folder, title) for zip_folder, title in zip(parent_zip_folder, titles)]
        zipped_folders = ['{}.zip'.format(zip_folder) for zip_folder in zipped_folders]
        # check if they exist:
        for zip_dir in zipped_folders:
            print(zip_dir)
            if os.path.exists(zip_dir):
                pass
            else:
                sys.exit('paths dont exist')

         # zipped_dir will be index title
        for idx, shp in enumerate(zipped_folders):
            properties_dict = {'title':titles[idx],
                                'tags':tags[idx],
                                'snippet':snippets[idx]}
            fc_item = self. mcmjac_gis.content.add(properties_dict, data = shp)
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
