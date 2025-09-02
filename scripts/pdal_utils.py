# Check https://www.spatialised.net/lidar-qa-with-pdal-part-1/
import json
import pdal
import os
import pandas as pd
import copy

# # 20250805
# #   METADATA into dataframe per tile
# las_dir = r"D:\2025_LAS"
# las_file = [fp for fp in os.listdir(las_dir) if os.path.splitext(fp)[-1]=='.las']
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
#     pipeline.execute()
#     stats = pipeline.metadata["metadata"]["filters.stats"]["statistic"]
#     cls=[s for s in stats if s["name"]=="Classification"]
#     classes = [int(float(k)) for k in list(cls[0]['bins'].keys())]
#     cols = [True]* len(classes)
#     classes.append('las_name')
#     cols.append(l)
#     d = {k:[v] for k,v in zip(classes, cols)}
#     df_temp = pd.DataFrame(d)
#     if 'df' in locals():
#         df=pd.concat([df, df_temp])
#     else:
#         df=copy.copy(df_temp)
# df.to_csv(r"D:\2025_las_classifications.csv")

# INDIVIDUAL TILES
# Output individual tiles from above inventory, then list, tile, buildVRT, merge
las_dir = r"C:/Users/ZacharyUhlmann/Documents/staging/tolt/2024_LiDAR/2024_LAS/2024_LAS/Full_Classification/Full_Classification"
tiff_dir = r"C:\Users\ZacharyUhlmann\Documents\staging\pdal_test\2024_boulder\tiles"
df=pd.read_csv(r"C:\Users\ZacharyUhlmann\Documents\staging\pdal_test\2024_las_classifications.csv")
df=df[getattr(df, '72')]
for idx in df.index:
    las_name = df.loc[idx, 'las_name']
    print(las_name)
    tiff_name = las_name[:-4]
    tiff_name = f"{tiff_name}_AboveGdHt.tif"
    fp_tiff = os.path.join(tiff_dir, tiff_name)
    pipeline = [
        {
            "type":"readers.las",
            # "filename": r"C:\Users\ZacharyUhlmann\Documents\staging\pdal_test\stats_test\*.las"
            "filename": os.path.join(las_dir, las_name)
        },
        {
            "type": "filters.range",
            "limits": "Classification[2:2], Classification[72:72]"
        },
        {
            "type": "filters.hag_delaunay"
        },
        {

            "type": "filters.ferry",
            "dimensions": "HeightAboveGround=Z"
        },
        {
            "type": "filters.expression",
            "expression": "Classification==72"
        },
        {
            "type": "writers.gdal",
            "filename": fp_tiff,
            "output_type": "max",
            "gdaldriver": "GTiff",
            "nodata": -9999,
            "resolution": 1
        }
        ]
    pipeline = pdal.Pipeline(json.dumps(pipeline))
    pipeline.execute()
