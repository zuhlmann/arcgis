from sklearn.neighbors import KDTree
import numpy as np
import geopandas as gpd
import pandas as pd
import copy

# ZU 20240221 magic valley inundation

gdb_pro = r"C:\Box\MCM Projects\Magic Dam Wood Hydro - Part 12 and other work\24-009 Magic Dam Inundation Mapping\6.0 Plans and Specs\6.6_GIS\Project_mxds\magic_valley_inundation\magic_valley_inundation.gdb"
gdb_pro =r"E:\box_offline\projects\magic_valley\magic_valley_scratch.gdb"
fp_unknown = r"E:\box_offline\projects\magic_valley\nsi_2022_digitized.shp"
fp_existing = r"E:\box_offline\projects\magic_valley\nsi_2022_16_aoi_wgs84.shp"
fp_out = r"E:\box_offline\projects\magic_valley\nsi_2022_digitized_matched.shp"
gdf_unknown = gpd.read_file(fp_unknown)
gdf_existing = gpd.read_file(fp_existing)

# Get indices for nearest 5 points using KD Tree (or other method linked below)
# https://towardsdatascience.com/tree-algorithms-explained-ball-tree-algorithm-vs-kd-tree-vs-brute-force-9746debcd940
# gdf_existing['KDTree_idx'] = list(range(len(gdf_existing)))
# gdf_existing = gdf_existing.set_index(['KDTree_idx'])
lon = gdf_existing['lon_mcm']
lat = gdf_existing['lat_mcm']

# iterate over unknown points
lon2, lat2 = gdf_unknown['lon_mcm'], gdf_unknown['lat_mcm']
coords_unknown = np.column_stack((np.array(lon2), np.array(lat2)))

# Empty dataframe to populate with tree indices per damage category
dam_cat = [r'COM',r'IND',r'PUB',r'RES']
arr_empty = np.zeros([len(gdf_unknown), 4])
arr_empty = np.full_like(arr_empty,-9999)
df_tree = pd.DataFrame(arr_empty, columns = dam_cat)

for dc in dam_cat:
    gdf_subset = gdf_existing[gdf_existing['st_damcat']==dc]
    idx_existing = gdf_subset.index.to_list()
    lon = gdf_subset['lon_mcm']
    lat = gdf_subset['lat_mcm']
    coords_existing = np.column_stack((np.array(lon), np.array(lat)))
    tree = KDTree(coords_existing, leaf_size=2)
    dist, tree_idx = tree.query(coords_unknown, k=1)
    # [0] below because array structure
    idx_existing = [idx_existing[ti[0]] for ti in tree_idx]
    df_tree[dc] = idx_existing

for idx_unknown, row in gdf_unknown.iterrows():
    # Substitute entire row
    dc = row['st_damcat']
    idx_existing = df_tree.loc[idx_unknown,dc]
    # gdf_unknown.iloc[1, :] = gdf_existing.loc[3641, :]  #WORKED now try slicing to begin at non-fid
    # The column idx 3: will skip FIDs from QGIS
    gdf_unknown.iloc[idx_unknown,3:-3] = gdf_existing.iloc[idx_existing, 3:-3]  #WORKED now try slicing to begin at non-fid
    # gdf_unknown.iloc[id,:] = gdf_existing.loc[tree_idx[id],:].values()[0]
    # # Add defaults
    gdf_unknown.loc[idx_unknown, 'bid']=r'McMillen_ID{}'.format(idx_unknown)
    gdf_unknown.loc[idx_unknown, 'students']=0
dtype_dict_csv = r"C:\Box\MCM Projects\Magic Dam Wood Hydro - Part 12 and other work\24-009 Magic Dam Inundation Mapping\6.0 Plans and Specs\6.6_GIS\LifeSim\dtype_dict.csv"
df_dtype = pd.read_csv(dtype_dict_csv)
subset = df_dtype[~pd.isnull(df_dtype.dtype_map)]
vals = subset['dtype_map']
keys = subset['field']
d = dict(zip(keys, vals))
d2 = dict(zip(keys,['int32']*len(vals)))
# schema_fixed = gpd.io.file.infer_schema(gdf_unknown)
schema_existing = gpd.io.file.infer_schema(gdf_existing)
# schema_fixed['properties']=copy.copy(schema_existing['properties'])
for k,v in zip(keys, vals):
    schema_existing['properties'][k]=v
gdf_unknown = gdf_unknown.astype(d2)
gdf_unknown.to_file(fp_out, schema = schema_existing)


