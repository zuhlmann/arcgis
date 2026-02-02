import geopandas as gpd
# 20251208
# used for columbia basin 1) multipart NHD Formatted 3) Only retained larged multipart

shp_in = r"C:\Box\MCMGIS\Project_Based\CBHP\data\staging\NHD\WA_State_NHD_fmt_multi.shp"
df = gpd.read_file(shp_in)

idx = df.groupby(['FIRST_GNIS'])['length_ft'].transform(max) == df['length_ft']
df_subset = df[idx]

shp_out = r"C:\Box\MCMGIS\Project_Based\CBHP\data\staging\NHD\WA_State_NHD_fmt_CBHP.shp"
df_subset.to_file(shp_out)