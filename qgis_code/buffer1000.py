import os 
import geopandas as gpd

# take intersection of parcels with buffered reservoir.
# Generally use with any intersection, etc.
# ZU 20232010

scratch_dir = r'D:\box_offline\temp\gpd_practice_20230118'
master_gdb = os.path.join(scratch_dir, 'master.gdb')
d_drive_gdb = os.path.join(scratch_dir, 'klamath_d_drive2.gdb')
gdf_buff = gpd.read_file(d_drive_gdb, layer = 'IG_1000ft_buff')
gdf_buff_select = gdf_copco.iloc[0]
gdf_parcels = gpd.read_file(d_drive_gdb, layer='gdf_joined_20230206')

ex = [6428965,2584755,6469115,2607455]
gdf_parcels_clip = gdf_parcels.cx[ex[0]:ex[2],ex[1]:ex[3]]
#
ls = []
for idx, row in gdf_parcels_clip.iterrows():
    # intersect the parcels | cast to list
    temp = gdf_buff['geometry'].intersects(row['geometry']).to_list()[0]
    ls.append(temp)
df_buff = gpd.GeoSeries(ls)

gdf_parcels_selected = gdf_parcels_clip[df_buff.values]
gdf_parcels_selected.to_file(d_drive_gdb, layer='gdf_joined_1000ftbuff_IG')

#"apn" ='004-393-521-000'