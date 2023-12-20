import geopandas as gpd
from collections import OrderedDict

# Merging 3 shapefiles but retaining only one column from each
# num redds 20231213

dir_in = r'E:\box_offline\temp\tolt\McMillen_ReachBreaks_20231103'
fnames = [r'reach_boxes_summer_steelhead_counts','reach_boxes_winter_steelhead_counts',
            'reach_boxes_chinook_counts']
feats = [os.path.join(dir_in, r'{0}.shp'.format(fn)) for fn in fnames]
cols_keep = ['Reach','Label']
cols = ['NumRedSumSteelhead','NumRedWinSteelhead','NumRedChinook']

# rename columns since they are duplicates
gdf_tgt = gpd.read_file(feats[0])
gdf_tgt = gdf_tgt.rename(columns={'num_redds':cols[0]})
gdf_src = gpd.read_file(feats[1])
gdf_src = gdf_src.rename(columns={'num_redds':cols[1]})
gdf_src2 = gpd.read_file(feats[2])
gdf_src2 = gdf_src2.rename(columns={'num_redds':cols[2]})

# merge twice
gdf_merged = gdf_tgt.merge(gdf_src, on = 'Label')
gdf_merged = gdf_merged.merge(gdf_src2, on='Label')
cols_all = cols_keep+cols
cols_all2 = cols_all + ['Shape_Leng','Shape_Area']
schema_prop_dict = {v:t for v,t in zip(cols_all2, ['str:50']*len(cols_all2))}
schema_updated = {'properties':OrderedDict(schema_prop_dict),'geometry':'Polygon'}

# Add geometry as gdf.merge() returns a pandas dataframe NOT a geopandas dataframe with geom
geom = copy.copy(gdf_tgt.geometry)
gdf_merged = gdf_merged[cols_all2]
# NOTe - had to rewrite this as script was partially deleted.  File name no longer exists (deleted)
fp_out = os.path.join(dir_in, 'geomorph_boxes_test99.shp')
gdf_merged = gpd.GeoDataFrame(gdf_merged, geometry = geom, crs = r'EPSG:2926')
gdf_merged.to_file(fp_out, schema=schema_updated)



