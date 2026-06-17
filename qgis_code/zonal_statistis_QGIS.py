# # import processing
# shp = r'C:\Box\MCM Projects\MCWRA (Monterey County)\25-001_San Antonio Spillway Design\6.0 Plans and Specs\6.4 Design\6.4.4 Hydraulics\2025 PMF update\NLCD_2025\zonal_hist_BASIN.shp'
#
# params = {'INPUT_RASTER':'Annual_NLCD_LndCov_2023',
#             'RASTER_BAND':1,
#             'INPUT_VECTOR':'San_Antonio_Watershed_Area',
#             'COLUMN_PREFIX':'HISTO_',
#             'OUTPUT':shp
#             }
# processing.run("native:zonalhistogram", params)
#
# import geopandas as gpd
# import pandas as pd
# csv_legend = r"C:\Box\MCM Projects\MCWRA (Monterey County)\25-001_San Antonio Spillway Design\6.0 Plans and Specs\6.4 Design\6.4.4 Hydraulics\2025 PMF update\NLCD_2025\NLCD_tJfNHo902Le2GMhaVeYs\NLCD_landcover_legend_2018_12_17_tJfNHo902Le2GMhaVeYs.csv"
# df_legend =  pd.read_csv(csv_legend, index_col='Value')
# gdf_zonal = gpd.read_file(shp)
# columns_shp = [c for c in gdf_zonal.columns if 'HISTO_' in c]
# columns_shp_fmt = [int(c[6:]) for c in gdf_zonal.columns if 'HISTO_' in c]
# df_legend_key = df_legend.loc[columns_shp_fmt]
# df_legend_key.loc[columns_shp_fmt, 'shp_cols']=columns_shp
# nlcd_dict_fmt = {df_legend_key.loc[idx, 'shp_cols']: df_legend_key.loc[idx, 'Legend'] for idx in df_legend_key.index}
# gdf_zonal.rename(columns=nlcd_dict_fmt, inplace=True)
# shp_out = r'C:\Box\MCM Projects\MCWRA (Monterey County)\25-001_San Antonio Spillway Design\6.0 Plans and Specs\6.4 Design\6.4.4 Hydraulics\2025 PMF update\NLCD_2025\zonal_hist_fmt_BASIN.shp'
# gdf_zonal.to_file(shp_out)


# Vector Products
import geopandas as gpd
import pandas as pd
import copy
xslx = r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\field_planning\AQ09\Slide_Examples\data\NHC_Hydr_Models_202604_inv.xlsx"
df = pd.read_excel(xslx)
df = df[df.Model_Type=='cfs_Depth']
fp_box = r'C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\field_planning\study_data\hydraulic_model\AQ06_Lower_SFT_Hydr_Model_NHC\202604\Depth'
fp_hd = r'E:\tolt\add_2026\AQ06_Lower_SFT_Hydraulic_Model_Production_Runs\Cleaned_Results\Depth'
df['DATA_LOCATION_MCM_LOCAL']=[p.replace(fp_box, fp_hd) for p in df.DATA_LOCATION_MCMILLEN]
shp_in = r'C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\field_planning\AQ09\Slide_Examples\data\shp\AQ09_Channel_Bdry_Slides_1.shp'
shp_out =  r'C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\field_planning\AQ09\Slide_Examples\data\shp\AQ09_Channel_Bdry_Slides_ZonalStats_Both.shp'
geodf = gpd.GeoDataFrame.from_file(shp_in)
# geodf = geodf[geodf.name=='ex_off_channel']
for idx in df.index:
    import rasterio
    model_run = df.loc[idx, 'DATA_LOCATION_MCM_LOCAL']
    with rasterio.open(model_run) as src:
        transform = src.meta['transform']
        array = src.read(1)
    # transform=(87630, 154.54,0,4025300,0,-156)
    from rasterstats import zonal_stats
    tgt_stats = ['mean','min','max','count']
    all_cols = ['name','geometry']
    all_cols.extend(tgt_stats)
    d = {'mean':'avg','min':'min','max':'max','count':'ct'}
    stats_str = ' '.join(tgt_stats)
    # stats = zonal_stats(geodf, array, transform=transform, stats=stats_str)
    stats = zonal_stats(geodf, model_run, stats=stats_str)
    new_geodf = geodf.join(pd.DataFrame(stats))
    gdf_format=new_geodf[all_cols]
    for s in tgt_stats:
        v = df.loc[idx, 'Value']
        new_col_name = f"{v}cfs_{d[s]}"
        gdf_format[s] = round(gdf_format[s], 2)
        gdf_format.rename(columns={s: new_col_name}, inplace=True)
    if not 'gdf_joined' in locals():
        gdf_joined = copy.copy(gdf_format)
    else:
        t = gdf_format[[c for c in gdf_format.columns if c not in 'geometry']]
        gdf_joined = pd.merge(gdf_joined, t, left_on='name', right_on='name')
gdf_joined.to_file(shp_out, driver="ESRI Shapefile")


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

