# import processing
shp = r'C:\Box\MCM Projects\MCWRA (Monterey County)\25-001_San Antonio Spillway Design\6.0 Plans and Specs\6.4 Design\6.4.4 Hydraulics\2025 PMF update\NLCD_2025\zonal_hist_BASIN.shp'

params = {'INPUT_RASTER':'Annual_NLCD_LndCov_2023',
            'RASTER_BAND':1,
            'INPUT_VECTOR':'San_Antonio_Watershed_Area',
            'COLUMN_PREFIX':'HISTO_',
            'OUTPUT':shp
            }
processing.run("native:zonalhistogram", params)

import geopandas as gpd
import pandas as pd
csv_legend = r"C:\Box\MCM Projects\MCWRA (Monterey County)\25-001_San Antonio Spillway Design\6.0 Plans and Specs\6.4 Design\6.4.4 Hydraulics\2025 PMF update\NLCD_2025\NLCD_tJfNHo902Le2GMhaVeYs\NLCD_landcover_legend_2018_12_17_tJfNHo902Le2GMhaVeYs.csv"
df_legend =  pd.read_csv(csv_legend, index_col='Value')
gdf_zonal = gpd.read_file(shp)
columns_shp = [c for c in gdf_zonal.columns if 'HISTO_' in c]
columns_shp_fmt = [int(c[6:]) for c in gdf_zonal.columns if 'HISTO_' in c]
df_legend_key = df_legend.loc[columns_shp_fmt]
df_legend_key.loc[columns_shp_fmt, 'shp_cols']=columns_shp
nlcd_dict_fmt = {df_legend_key.loc[idx, 'shp_cols']: df_legend_key.loc[idx, 'Legend'] for idx in df_legend_key.index}
gdf_zonal.rename(columns=nlcd_dict_fmt, inplace=True)
shp_out = r'C:\Box\MCM Projects\MCWRA (Monterey County)\25-001_San Antonio Spillway Design\6.0 Plans and Specs\6.4 Design\6.4.4 Hydraulics\2025 PMF update\NLCD_2025\zonal_hist_fmt_BASIN.shp'
gdf_zonal.to_file(shp_out)

# RIVER MILES
# A) Reverse Line Dir (if necessary)
# Reverse Line Direction tool
# B) Generate points
# Points Along Geometry tool to get points

# # C) Format att table
# layer_name = 'RMs'
# layer = QgsProject.instance().mapLayersByName(layer_name)[0]
# layer.startEditing()
# features = layer.getFeatures()
# total_len=0
# for ct, feature in enumerate(features):
#     incr=528
#     tenth_mi = (total_len / incr) % 10
#     whole_mi = total_len // 5280
#     total_len += incr
#     feature['tenth_mi']= tenth_mi
#     feature['whole_mi']= whole_mi
#     layer.updateFeature(feature)
# layer.commitChanges()