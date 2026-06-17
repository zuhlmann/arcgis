# Check https://www.spatialised.net/lidar-qa-with-pdal-part-1/
import json
import pdal
import os
import pandas as pd
import copy
import logging

# NOTE - if proj error occurs, need to set these env-variables in GUI on windows (below does not work)
# https://gis.stackexchange.com/questions/326968/ogr2ogr-error-1-proj-pj-obj-create-cannot-find-proj-db
# occuring because postres changed those variables
# os.environ['PROJ_LIB']=r"C:\Users\ZacharyUhlmann\anaconda3\envs\pdal_env\Library\share\proj"
# os.environ['GDAL_DATA']=r"C:\Users\ZacharyUhlmann\anaconda3\envs\pdal_env\Library\share\gdal"

# # 20250805
# #   METADATA into dataframe per tile"
# year = 2015
# las_dir = r"E:\projects\temp\wallowa_viewshed"
# fp_logfile = r"{}\{}_LOG.log".format(las_dir,year)
# logging.basicConfig(filename=fp_logfile, level=logging.DEBUG)
# las_file = [fp for fp in os.listdir(las_dir) if os.path.splitext(fp)[-1]=='.laz']
# for l in las_file:
#     pipeline = [
#         {
#             "type":"readers.las",
#             "filename": os.path.join(las_dir, l)
#         },
#         { "type": "filters.stats",
#           "dimensions": "Classification",
#           "count": "Classification"}
#         ]
#     pipeline = pdal.Pipeline(json.dumps(pipeline))
#     try:
#         pipeline.execute()
#         stats = pipeline.metadata["metadata"]["filters.stats"]["statistic"]
#         cls=[s for s in stats if s["name"]=="Classification"]
#         classes = [int(float(k)) for k in list(cls[0]['bins'].keys())]
#         cols = [True]* len(classes)
#         classes.append('las_name')
#         classes.append('exception')
#         cols.append(l)
#         cols.append('None')
#         # readers.las values
#         bounds_etc = ["minx", "maxx", "miny", "maxy", "minz", "maxz"]
#         classes.extend(bounds_etc)
#         for k in bounds_etc:
#             cols.append(pipeline.metadata["metadata"]["readers.las"][k])
#         d = {k:[v] for k,v in zip(classes, cols)}
#         df_temp = pd.DataFrame(d)
#         if 'df' in locals():
#             df=pd.concat([df, df_temp])
#         else:
#             df=copy.copy(df_temp)
#     except RuntimeError:
#         d = {'las_name':[l], 'exception': ['RuntimeError']}
#         df_temp = pd.DataFrame(d)
#         if 'df' in locals():
#             df=pd.concat([df, df_temp])
#         else:
#             df=copy.copy(df_temp)
#         msg_str = f"TILE: {l}\nRunTimeError"
#         logging.info(msg_str)
#     except TypeError:
#         d = {'las_name':[l], 'exception': ['NoneType']}
#         df_temp = pd.DataFrame(d)
#         if 'df' in locals():
#             df=pd.concat([df, df_temp])
#         else:
#             df=copy.copy(df_temp)
#         msg_str = f"TILE: {l}\nTypeError"
#         logging.info(msg_str)
# srs = pipeline.metadata["metadata"]["readers.las"]["spatialreference"]
# srs_out = r'{}\{}_las_srs.txt'.format(las_dir, year)
# with open(srs_out, 'w') as txt:
#     txt.write(srs)
# df.to_csv(r"{}\{}_las_inv.csv".format(las_dir,year))

# # HAG w/ LWD
# # Output individual tiles from above inventory, then list, tile, buildVRT, merge
# las_dir = r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\raster\lidar\2024 NV5 SF Tolt LiDAR\2024_LAS\2024_LAS\Full_Classification\Full_Classification"
# tiff_dir = r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\raster\lidar\2024 NV5 SF Tolt LiDAR\2024_LWD_McM\method_devel"
# df=pd.read_csv(r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\raster\lidar\2024 NV5 SF Tolt LiDAR\2024_LAS\2024_full_las_classes.csv")
# df=df[getattr(df, '73')]
# for idx in df.index:
#     las_name = df.loc[idx, 'las_name']
#     print(las_name)
#     tiff_name = las_name[:-4]
#     tiff_name = f"{tiff_name}_AboveGdHt.tif"
#     fp_tiff = os.path.join(tiff_dir, tiff_name)
#     pipeline = [
#         {
#             "type":"readers.las",
#             # "filename": r"C:\Users\ZacharyUhlmann\Documents\staging\pdal_test\stats_test\*.las"
#             "filename": os.path.join(las_dir, las_name)
#         },
#         {
#             "type": "filters.range",
#             "limits": "Classification[2:2], Classification[73:73]"
#         },
#         {
#             "type": "filters.hag_delaunay"
#         },
#         {
#
#             "type": "filters.ferry",
#             "dimensions": "HeightAboveGround=Z"
#         },
#         {
#             "type": "filters.expression",
#             "expression": "Classification==73"
#         },
#         {
#             "type": "writers.gdal",
#             "filename": fp_tiff,
#             "output_type": "max",
#             "gdaldriver": "GTiff",
#             "nodata": -9999,
#             "resolution": 1
#         }
#         ]
#     pipeline = pdal.Pipeline(json.dumps(pipeline))
#     pipeline.execute()


# # # BE w/ 2023 Bathy (See Commented Out blocks to )
# # # NOTE!!! Ended up using next code bloc methodology to ensure matching extents
# # Output individual tiles from above inventory, then list, tile, buildVRT, merge
# # # MANUAL
# # output_dir = r"C:\Users\ZacharyUhlmann\Documents\staging\tolt\AQ07\gcd\2024\2024_las_test_large"
# # input_dir = r'C:\Users\ZacharyUhlmann\Documents\staging\tolt\2024_LiDAR\2024_LAS\2024_LAS\Full_Classification\Full_Classification'
# # df = pd.read_csv(r"D:\tolt\2020_las\2020_full_las_classes.csv")
# # FROM INVENTORY
# year=2025
# csv_m3c2 = r"C:\Users\ZacharyUhlmann\Documents\staging\tolt\AQ07\gcd\tolt_m3c2_inv.csv"
# df_m3c2 = pd.read_csv(csv_m3c2)
# df_m3c2 = df_m3c2.set_index('YEAR')
# output_dir = df_m3c2.loc[year, 'TARGET_DIR']
# input_dir = df_m3c2.loc[year, 'SOURCE_DIR']
# csv = df_m3c2.loc[year, 'LAS_INV']
# df = pd.read_csv(csv)
# df = df.set_index('las_name')
# df = df[df["9_NIR_Water_Surface"]]
# for idx in df.index:
#     fname = os.path.split(idx)[-1]
#     las_name, ext = os.path.splitext(fname)
#     if ext=='.laz':
#         pass
#     else:
#         ext='.las'
#     fname_in = f"{las_name}{ext}"
#     tile_ID = las_name[-3:]
#     if year==2025:
#         tile_ID= copy.copy(las_name)
#     fname_out = f"Tolt_{str(year)}_Class9_NIR_WaterSurface_{tile_ID}.las"
#     fp_out = os.path.join(output_dir, fname_out)
#     pipeline = [
#         {
#             "type": "readers.las",
#             # "filename": r"C:\Users\ZacharyUhlmann\Documents\staging\pdal_test\stats_test\*.las"
#             "filename": os.path.join(input_dir, fname_in)
#         },
#         {
#             "type": "filters.range",
#             "limits": "Classification[9:9]"
#         },
#         # {
#         #     "type": "filters.expression",
#         #     "expression": "Classification==2"
#         # },
#         {
#             "type":"writers.las",
#             "filename":fp_out
#         }
#         ]
#     pipeline = pdal.Pipeline(json.dumps(pipeline))
#     pipeline.execute()

# # # Merge w/ 2023 Bathy
# # MATCHING EXTENTS - used tindex merging adapted from pdal tutorial
# index_file = r"C:\Users\ZacharyUhlmann\Documents\staging\tolt\bathymetry\2023\Tolt_2023_las_index_WA_N_ft_joined.shp"
# fp_tiff = r"C:\Users\ZacharyUhlmann\Documents\staging\tolt\bathymetry\2023\Tolt_2023_Bathy_Class2_ExtentMatched_mean.tif"
# pipeline = [
#     {
#         "type":"readers.tindex",
#         "filename":index_file,
#         "lyr_name":"Tolt_2023_las_index_WA_N_ft_joined",
#         # "srs_column":"srs"
#         "t_srs":"EPSG:6597",
#         # "where":"test=99"
#         "where":"class2=1"
#     },
#     {
#         "type": "filters.range",
#         "limits": "Classification[2:2]"
#     },
#     {
#         "type": "writers.gdal",
#         "filename": fp_tiff,
#         "output_type": "mean",
#         "gdaldriver": "GTiff",
#         "nodata": -9999,
#         "resolution": 1.5,
#         # "bounds": [(1426500, 250500, 1452000, 264000)],
#         "origin_x": 1426500,
#         "origin_y": 250500,
#         "width":17000,
#         "height":9000
#     }
#     ]
# pipeline = pdal.Pipeline(json.dumps(pipeline))
# pipeline.execute()

# # # Merge las 20251022
# # MATCHING EXTENTS - used tindex merging adapted from pdal tutorial
# index_file = r"E:\tolt\add_2026\SUBSTRATE\Tolt_River_2024_Lidar_Index_Reach1.shp"
# fp_out = r"E:\tolt\add_2026\SUBSTRATE\Tolt_River_2024_Lidar_Index_Reach1.shp\2024_las_merged_reach1.las"
# pipeline = [
#     {
#         "type":"readers.tindex",
#         "filename":index_file,
#         "lyr_name":"Tolt_River_2024_Lidar_Index_Reach1",
#         # "srs_column":"srs"
#         "t_srs":"EPSG:6597"
#     },
#     {
#         "type": "writers.las",
#         "filename": fp_out
#     }
#     ]
# pipeline = pdal.Pipeline(json.dumps(pipeline))
# pipeline.execute()

# # SPLIT merged into giles for processing
# pipeline = [
#     {
#         "type": "readers.las",
#         # "filename": r"E:\tolt\2014_nv5\2014_rev2025_BE_merged.las"
#         "filename": r"E:\tolt\2025_Final\2025_BE_merged.las"
#     },
#     {
#         "type":"filters.splitter",
#         "length":"7500",
#         "origin_x":"1394000",
#         "origin_y":"251000",
#         "buffer":"100"
#     },
#     {
#         "type": "writers.las",
#         # "filename":r"E:\tolt\2014_nv5\2014_Rev_2025_LAS_BE_split\2014_rev2025_BE_split_10000ft_offset_#.las"
#         "filename":r"E:\tolt\2025_Final\2025_tile_split_7500ft\\2025_all_split_7500ft_offset_#.las"
#     }
#     ]
# pipeline = pdal.Pipeline(json.dumps(pipeline))
# pipeline.execute()
#
# # # Determine bounding extents
# # # DELETE 2025 Dec 1 - one off calculation
# # csv_split = r"C:\Users\ZacharyUhlmann\Documents\staging\tolt\AQ07\gcd\las_BE_inv_all.csv"
# # df = pd.read_csv(csv_split, index_col='YEAR')
# # idx = [2020,2022,2023,2024]
# # df_subset = df.loc[idx]
# # l = df_subset['minx'].min(), df_subset['miny'].min(),df_subset['maxx'].max(),df_subset['maxy'].max()
# # l = [int(i) for i in l]
# # l
# #
# # # M3C2
# # 20260409
# year_r_list = [2024]
# year_t_list = [2014]
# xslx = r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\field_planning\study_data\gcd\Table_2_5_GCD_Comparison.xlsx"
# csv = r"E:\tolt\add_2026\tiles_m3c2.csv"
# df_m3c2 = pd.read_excel(xslx,index_col='tile', sheet_name='tiles_m3c2')
# csv_nva = r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\field_planning\study_data\gcd\lidar_vert_accuracy.csv"
# df_accuracy = pd.read_excel(xslx, index_col = 'year', sheet_name='Lidar_Vert_Accuracy')
# ct = 0
# for year_r, year_t in zip(year_r_list, year_t_list):
#     if (year_r==2023) and (year_t==2024):
#         tile = [3,4]
#     else:
#         tile=[1,2,3,4]
#     las_dir_out = r'E:\tolt\add_2026\2024_2014'
#     fp_logfile = r"{}\{}_to_{}_LOG.log".format(las_dir_out,year_r, year_t)
#     logging.basicConfig(filename=fp_logfile, level=logging.DEBUG)
#     # list of las files in comparison year
#     l_target = [df_m3c2.loc[t, year_t] for t in tile]
#     l_ref = [df_m3c2.loc[t, year_r] for t in tile]
#     # params
#     reg_error = max(df_accuracy.loc[year_r,'nva_ft'], df_accuracy.loc[year_t, 'nva_ft'])
#     norm_diam = 30
#     proj_diam = 6
#     for lr, lt, t in zip(l_ref, l_target, tile):
#         today = pd.Timestamp.today().round('h')
#         fname_out = f"{year_r}_{year_t}_M3C2_{norm_diam}norm_{proj_diam}rad_Tile{t}.las"
#         params = f"TIME: ---{today}---\nFILENAME   {fname_out} \nREF LAS:   {lr}\nTARGET LAS {lt}\nREG ERROR: {reg_error}\n"
#         logging.info(params)
#         pipeline = [
#             {
#                 "filename": lr,
#                 "tag": "A"
#             },
#             {
#                 "filename": lt,
#                 "tag": "B"
#             },
#             {
#                 "type": "filters.m3c2",
#                 "normal_radius": norm_diam/2,
#                 "cyl_radius": proj_diam/2,
#                 "cyl_halflen": 25,
#                 "reg_error": reg_error,
#                 "inputs": [
#                     "A",
#                     "B",
#                     "A"
#                 ]
#             },
#             {
#                 "type": "writers.las",
#                 "filename": os.path.join(las_dir_out, fname_out),
#                 "extra_dims": "all",
#                 "minor_version": "4"
#             }
#         ]
#
#         pipeline = pdal.Pipeline(json.dumps(pipeline))
#         try:
#             pipeline.execute()
#         except RuntimeError:
#             msg_str = f"TILE: {l}\nRunTimeError"
#             logging.info(msg_str)
