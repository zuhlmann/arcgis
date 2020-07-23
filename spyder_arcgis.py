# ZRU 7/13/20
# To run this we need to be in arcgispro-py3 environment w/ GIS package:
# go to C:\Program Files\ArcGIS\Pro\bin\Python\Scripts and do: Start proenv.bat
# python2 to python3 compatability: https://pro.arcgis.com/en/pro-app/arcpy/get-started/python-migration-for-arcgis-pro.htm
# coding: utf-8
from __future__ import print_function, unicode_literals, absolute_import
from arcgis.gis import GIS
from arcgis.gis import Group
import os, sys
import glob
import copy
import pandas as pd
import zipfile

# # since i don't have system admin rights I cannot remove python 2.7 arcpy path (Program Files 86)
sys.path = [p for p in sys.path if '86' not in p]
# use my modules
sys.path.append('C:\\Users\\uhlmann\\code')
for item in sys.path:
    print(item)
import arcpy
import compare_data


mcmjac_gis = GIS(username = 'uhlmann@mcmjac.com', password = 'Gebretekle24!')
print('Connected to {} as {}'.format(mcmjac_gis.properties.portalHostname, mcmjac_gis.users.me.username))
# # query_str = 'owner:'.format(gis.users.me.username)
# # my_content = gis.content.search(query = query_str, item_type = 'shapefile', max_items = 15)
# to get group info use group id from html 'html?id-<HERE IS ID #>'
krrp_geospatial = Group(mcmjac_gis, 'a6384c0909384a43bfd91f5d9723912b')
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

# get file paths to upload
fp_table = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Data\\compare_vers\\comparison_tables\\Wetlands\\Wetlands_20191004_Vs_20190930.csv'
fp_gdb = 'C:\\Users\\uhlmann\\Box\GIS\\Project_Based\Klamath\\DataReceived\\AECOM\\100719\\WetlandAndBio_GISData_20191004\\Klamath_CDM_Wetlands_20191004.gdb'
fp_out = 'C:\\Users\\uhlmann\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\GIS_Data\\AGOL_DataUploads\\2020_07_21\\2020_07_21'

# version 1 when using csv to grab titles
# df = pd.read_csv(fp_table)
# title = df['feature_1']


# CREATE SHAPEFILES and get titles
title = compare_data.parse_gdb_dsets(fp_gdb)
# SORT ALPHABETICALLY!  or else mismatched item_properties to dataset
title.sort()

# wierd but quick way to pull reservoir name from variable fc naming strategy in gdb fc in comparison csv
trans_dict = {'jc':'JC Boyle', 'co':'Copco', 'ir':'Iron Gate'}
# ADD RESERVOIR NAMEe to tags: grab first two letters in feature class then key to full reservoir name
tags = [trans_dict[fc[:2].lower()] for fc in title]
# add wetland to tags
temp_tags = []
tags_final = []
for tag in tags:
    temp_tags = []
    temp_tags.append(tag)
    temp_tags.append('wetlands')
    tags_final.append(temp_tags)

# Print
for idx, tags in enumerate(tags_final):
    print('{} tags final: {}'.format(idx + 1, tags))
for idx, t in enumerate(title):
    print('{} title: {}'.format(idx, t))

# single snippet for all features
snippet = ['Item from WETLAND delineations (current as of May 2020): boundaries and points'] * len(title)

# 2) ZIP SHAPEFILES
# From here: https://community.esri.com/thread/28985

def zipShapefilesInDir(inDir, outDir):
    # Check that input directory exists
    if not os.path.exists(inDir):
        print("Input directory {} does not exist!".format(inDir))
        return False

    # Check that output directory exists
    if not os.path.exists(outDir):
        # Create it if it does not
        print('Creating output directory {}'.format(outDir))
        os.mkdir(outDir)

    print("Zipping shapefile(s)in folder {} to output folder {}".format(inDir, outDir))

    # Loop through shapefiles in input directory
    for inShp in glob.glob(os.path.join(inDir, "*.shp")):
        # Build the filename of the output zip file
        outZip = os.path.join(outDir, os.path.splitext(os.path.basename(inShp))[0] + ".zip")

        # Zip the shapefile
        zipShapefile(inShp, outZip)
    return True

def zipShapefile(inShapefile, newZipFN):
    print('Starting to Zip '+ inShapefile +' to '+ newZipFN)

    # Check that input shapefile exists
    if not (os.path.exists(inShapefile)):
        print(inShapefile + ' Does Not Exist')
        return False

    # Delete output zipfile if it already exists
    if (os.path.exists(newZipFN)):
        print('Deleting '+newZipFN)
        os.remove(newZipFN)

    # Output zipfile still exists, exit
    if (os.path.exists(newZipFN)):
        print('Unable to Delete'+newZipFN)
        return False

    # Open zip file object
    zipobj = zipfile.ZipFile(newZipFN,'w')

    # Loop through shapefile components
    for infile in glob.glob( inShapefile.lower().replace(".shp",".*")):
        # Skip .zip file extension
        if os.path.splitext(infile)[1].lower() != ".zip":
            print("Zipping {}".format(infile))
            # Zip the shapefile component
            zipobj.write(infile, os.path.basename(infile), zipfile.ZIP_DEFLATED)

    # Close the zip file object
    zipobj.close()
    return True

# NOTE: these files were created with parse_gdb_datasets function used earlier
inDir = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\Klamath_River_Renewal_MJA\\GIS_Data\\AGOL_DataUploads\\2020_07_21\\2020_07_21'
outDir = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Data\AGOL_DataUploads\\2020_07_21\\2020_07_21_zip'
# zipShapefile(testShapeFile,testZipFile)
# zipShapefilesInDir(inDir, outDir)

# Main method, used when this script is the calling module, otherwise
# you can import this module and call your functions from other modules
# if __name__=="__main__":
#
#     inDir = r"c:\temp"
#     outDir = r"c:\temp\testZipShp"
#     zipShapefilesInDir(inDir, outDir)
#     print("done!")
#
# 3) ADD ITEMS TO AGOL
zipped_dirs = [subD.path for subD in os.scandir(outDir)]
for idx, shp in enumerate(zipped_dirs[:2]):
    print('{} shp: {}'.format(idx,shp))
#
for idx, shp in enumerate(zipped_dirs[:2]):
    properties_dict = {'title':title[idx],
                        'tags':tags[idx],
                        'snippet':snippet[idx]}
    fc_item = mcmjac_gis.content.add(properties_dict, data = shp)
    print('ct = {} \n fc_item {} '.format(idx, fc_item))
fc_item.share(groups = krrp_geospatial)
