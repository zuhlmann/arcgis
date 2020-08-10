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

# # since i don't have system admin rights I cannot remove python 2.7 arcpy path (Program Files 86)
sys.path = [p for p in sys.path if '86' not in p]
# use my modules
sys.path.append('C:\\Users\\uhlmann\\code')
for item in sys.path:
    print(item)
import arcpy
import compare_data

# get file paths to upload
fp_table = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Data\\compare_vers\\comparison_tables\\Wetlands\\Wetlands_20191004_Vs_20190930.csv'
fp_gdb = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath\\DataReceived\\AECOM\\100719\\WetlandAndBio_GISData_20191004\\Klamath_CDM_Wetlands_20191004.gdb'
fp_out = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Data\\AGOL_DataUploads\\2020_08_05\\2020_08_05'
fp_new_data = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Data\\new_data_downloads'

# 1) ZIP SHAPEFILES
# only need to do this ONCE!
# NOTE: these files were created with compare_data.parse_gdb_datasets function used earlier
inDir = copy.copy(fp_out)
outDir = '{}zip2'.format(inDir)
utilities.zipShapefilesInDir(inDir, outDir)

# 2)  Tag, Zip and Upload
# 2a) general
title = [dir[:-4] for dir in os.listdir(outDir)]
tags = ['eagles', 'observations', 'krrp']
tags_final = []
# dumb way to make a nested list with duplicate tags for each feature
for i in range(len(title)):
    tags_final.append(tags)
snippet = ['eagle observation data current as of 7/13/2020'] * len(title)

# # 2b) wetlands.gdb
# # CREATE SHAPEFILES and get titles
# # NOTE: to create shapefils pass fp_out = 'path/to/folder' to parse_gdb_dsets()
# title = compare_data.parse_gdb_dsets(fp_gdb)
# # SORT ALPHABETICALLY!  or else mismatched item_properties to dataset BECAUSe
# # when files zipped, they are arranged alphabetically and they will be read
# # futher down
# title.sort()
#
# # wierd but quick way to pull reservoir name from variable fc naming strategy in gdb fc in comparison csv
# trans_dict = {'jc':'JC Boyle', 'co':'Copco', 'ir':'Iron Gate'}
# # ADD RESERVOIR NAMEe to tags: grab first two letters in feature class then key to full reservoir name
# tags = [trans_dict[fc[:2].lower()] for fc in title]
# # add wetland to tags
# temp_tags = []
# # appending to make nested list
# tags_final = []
# for tag in tags:
#     temp_tags = []
#     temp_tags.append(tag)
#     temp_tags.append('wetlands')
#     tags_final.append(temp_tags)
#
# # single snippet for all features
# snippet = ['Item from WETLAND delineations (current as of May 2020): boundaries and points'] * len(title)
#
# # # Print DEBUGGING
# # for idx, tags in enumerate(tags_final):
# #     print('{} tags final: {}'.format(idx + 1, tags))
# # for idx, t in enumerate(title):
# #     print('{} title: {}'.format(idx, t))


# 3) ADD ITEMS TO AGOL

# 3a) GIS stuff: login with credentials
mcmjac_gis = GIS(username = 'uhlmann@mcmjac.com', password = 'Gebretekle24!')
print('Connected to {} as {}'.format(mcmjac_gis.properties.portalHostname, mcmjac_gis.users.me.username))
# # query_str = 'owner:'.format(gis.users.me.username)
# # my_content = gis.content.search(query = query_str, item_type = 'shapefile', max_items = 15)
# to get group info use group id from html 'html?id-<HERE IS ID #>'
krrp_geospatial = Group(mcmjac_gis, 'a6384c0909384a43bfd91f5d9723912b')

# 3b) AGOL Add data to Content and Groups
# file paths to .zip in alphabetical order
zipped_dirs = [subD.path for subD in os.scandir(outDir)]

for idx, shp in enumerate(zipped_dirs):
    properties_dict = {'title':title[idx],
                        'tags':tags_final[idx],
                        'snippet':snippet[idx]}
    fc_item = mcmjac_gis.content.add(properties_dict, data = shp)
    # fc_item.share(groups = 'a6384c0909384a43bfd91f5d9723912b')
    print('ct = {} \\n fc_item {} '.format(idx, fc_item))

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
