import geopandas as gpd 
import pandas as pd

#https://gist.github.com/maptastik/dc3d3b4514546310500a13fb77663bb9

# Get points from intersecting lines, with attribute from line.
# used for intersection of river with pipeline and ferc boundary (two separate runs)
# grabbed the RTE_ID (called FERC_ID in my dataset) from the king_co_wcrcs...streams data
# ZU 20230706

gdb_pro = r'C:\Users\UhlmannZachary\Box\MCMGIS\Project_Based\South_Fork_Tolt\map_documents\fish_passage\fish_passage.gdb'
gdb_master = r'C:\Users\UhlmannZachary\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\gdb\SFT_master.gdb'
proj_bdry = r'C:\Users\UhlmannZachary\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\p2959_project_bdry.shp'
contour = r'C:\Users\UhlmannZachary\Box\MCMGIS\Project_Based\Eklutna\Data\trails_2023july\contour_2022dem_267ft.shp'
lakeside_trail = r'C:\Users\UhlmannZachary\Box\MCMGIS\Project_Based\Eklutna\Data\trails_2023july\eklutna_lakeside_trail_split.shp'

#gdf_contour = gpd.read_file(contour)
#gdf_trail = gpd.read_file(lakeside_trail)
#gdf_pipeline = gpd.read_file(gdb_master, layer = 'pipelines')
#gdf_pipeline = gdf_pipeline.iloc[[3,5],]
# gdf_proj_bdry = gpd.read_file(proj_bdry)
gdf_roads = gpd.read_file(gdb_pro, layer = 'road_base_tolt_res')
gdf_streams = gpd.read_file(gdb_pro, layer='tributaries_tolt_res')

intersections_gdf = pd.DataFrame()

# Next, we'll iterate through each row in `gdf` and find out if and where it intersects with another line.
for index, row in gdf_streams.iterrows():
    # Get GeoSeries of intersections of row with all rows
    row_intersections = gdf_roads.intersection(row['geometry'])\
    
    # Exclude any rows that aren't a Point geometry
    row_intersection_points = row_intersections[row_intersections.geom_type == 'Point']
    
    # Create a DataFrame of the the row intersection points
    row_intersections_df = pd.DataFrame(row_intersection_points)
#     Create a field for the name (or some identifying value) of the row
    row_intersections_df['FERC_ID'] = row['FERC_ID']
    # Join the input gdf to the row intersections gdf. By default, this is a left join on the index.
   
#   # ZU was unable to get this join to work.  Barely tried though.  20230707
#   # Because the row gdf is a derivative of gdf, the index of each intersecting row is the same as in gdf
#    row_intersections_df = row_intersections_df.join(gdf_streams, on='FERC_ID',lsuffix='_',rsuffix='__')
  
  # Append the row intersection gdf to results gdf
    intersections_gdf = row_intersections_df.append(intersections_gdf)
    
    print(row_intersections_df)

# Drop the geometry field. Because we joined directly to our input gdf, the geometry field is the Line for the feature at the joined row's index
# intersections_gdf = intersections_gdf.drop('geometry', axis = 1)
# Rename and set the point field as the geometry field
intersections_gdf = intersections_gdf.rename(columns={0: 'geometry'})

## There are two points for each intersection. We only want one. We'll create a new field to store an intersection name based on a sorted list of the name of the two intersecting lines
#intersections_gdf['intersection'] = intersections_gdf.apply(lambda row: '-'.join(sorted([row['name_2'], row['name']])), axis = 1)
## We'll group the intersections by their name, returning only the first result for each unique value
#intersections_gdf = intersections_gdf.groupby('intersection').first()

# The index is now the intersection field. We don't want that, so we'll reset the index
intersections_gdf = intersections_gdf.reset_index()
# Finally, we'll turn the DataFrame back into a GeoDataFrame and set the CRS
intersections_gdf = gpd.GeoDataFrame(intersections_gdf, geometry = 'geometry')
intersections_gdf.crs = {'init': 'epsg:2926'}

## will throw error but works
intersections_gdf.to_file(gdb_pro, layer='fish_passage_points_reservoir_v2')