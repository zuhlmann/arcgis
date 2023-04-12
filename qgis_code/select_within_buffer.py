import geopandas as gpd
import os

scratch_dir = r'E:\box_offline\temp\gpd_practice_20230118'
master_gdb = os.path.join(scratch_dir, 'master.gdb')
gdf_klamath_river = gpd.read_file(master_gdb, layer = 'KlamathRiver')
gdf_klamath_river = gdf_klamath_river.unary_union
del_norte = r'E:\box_offline\klamath\McmJac_KRRP_GIS_data\new_data_downloads\parcels\del_norte_parcels\parcels_20230411\Parcels.shp'
humboldt = r'E:\box_offline\klamath\McmJac_KRRP_GIS_data\new_data_downloads\parcels\humboldt_parcels\apnhum108sp_202301091739192795\apnhum108sp.shp'

#Buffer river
klamath_buffer = gdf_klamath_river.buffer(500)
klamath_buffer.to_file(os.path.join(scratch_dir, 'klamath_buffer_500ft.shp'))

# ls = []
# for idx, row in gdf_parcels_clip.iterrows():
#     # intersect the parcels | cast to list
#     temp = gdf_buff['geometry'].intersects(row['geometry']).to_list()[0]
#     ls.append(temp)
# df_buff = gpd.GeoSeries(ls)

# gdf_parcels_selected = gdf_parcels_clip[df_buff.values]
# gdf_parcels_selected.to_file(d_drive_gdb, layer='gdf_joined_1000ftbuff_IG')
