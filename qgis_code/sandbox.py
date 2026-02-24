from shapely.geometry import box, mapping
import fiona
import rasterio

# create a Polygon from the raster bounds
bbox = box(-119.0, 33.5, -117.2, 34.75)

# create a schema with no properties
schema = {'geometry': 'Polygon', 'properties': {}}

src_crs = fiona.crs.from_epsg(4326)
shp = r'C:\Box\MCMGIS\Project_Based\RsrcDistSantaMonicaMtns\SouthLACoConnectivityPlan\data\vector\dbase_devel\LA_bbox_4326.shp'

# create shapefile
with fiona.open(shp, 'w', driver='ESRI Shapefile',
                crs=src_crs, schema=schema) as c:
    c.write({'geometry': mapping(bbox), 'properties': {}})