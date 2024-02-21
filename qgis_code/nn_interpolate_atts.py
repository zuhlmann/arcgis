from sklearn.neighbors import KDTree
import numpy as np
import geopandas as gpd

gdb_pro = r"C:\Box\MCM Projects\Magic Dam Wood Hydro - Part 12 and other work\24-009 Magic Dam Inundation Mapping\6.0 Plans and Specs\6.6_GIS\Project_mxds\magic_valley_inundation\magic_valley_inundation.gdb"
gdb_pro =r"E:\box_offline\projects\magic_valley\magic_valley_scratch.gdb"
fp_unknown = r"E:\box_offline\projects\magic_valley\nsi_2022_digitized.shp"
fp_existing = r"E:\box_offline\projects\magic_valley\nsi_2022_16_aoi_wgs84.shp"
fp_out = r"E:\box_offline\projects\magic_valley\nsi_2022_digitized_populated2.shp"
gdf_unknown = gpd.read_file(fp_unknown)
gdf_existing = gpd.read_file(fp_existing)

# Get indices for nearest 5 points using KD Tree (or other method linked below)
# https://towardsdatascience.com/tree-algorithms-explained-ball-tree-algorithm-vs-kd-tree-vs-brute-force-9746debcd940
# gdf_existing['KDTree_idx'] = list(range(len(gdf_existing)))
# gdf_existing = gdf_existing.set_index(['KDTree_idx'])
lon = gdf_existing['lon_mcm']
lat = gdf_existing['lat_mcm']

coords_existing = np.column_stack((np.array(lon), np.array(lat)))
tree = KDTree(coords_existing, leaf_size=2)

# iterate over unknown points
lon2, lat2 = gdf_unknown['lon_mcm'], gdf_unknown['lat_mcm']

coords_unknown = np.column_stack((np.array(lon2), np.array(lat2)))
dist, tree_idx = tree.query(coords_unknown, k=1)

# starting point for new fid
fid_existing = gdf_existing['fid']
fid_existing = [int(f) for f in fid_existing]
fid_unknown_start = max(fid_existing)

for idx_unknown, row in gdf_unknown.iterrows():
    # Substitute entire row
    idx_existing = tree_idx[idx_unknown]
    idx_existing = idx_existing[0]
    # gdf_unknown.iloc[1, :] = gdf_existing.loc[3641, :]  #WORKED now try slicing to begin at non-fid
    # The column idx 3: will skip FIDs from QGIS
    gdf_unknown.iloc[idx_unknown,3:-3] = gdf_existing.iloc[idx_existing, 3:-3]  #WORKED now try slicing to begin at non-fid
    # gdf_unknown.iloc[id,:] = gdf_existing.loc[tree_idx[id],:].values()[0]
    # # Add defaults
    gdf_unknown.loc[idx_unknown, 'bid']=r'McMillen_ID{}'.format(idx_unknown)
    gdf_unknown.loc[idx_unknown, 'students']=0
gdf_unknown.to_file(fp_out)


