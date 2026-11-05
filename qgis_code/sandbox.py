# from shapely.geometry import box, mapping
# import fiona
# import rasterio
import os

# # create a Polygon from the raster bounds
# bbox = box(-119.0, 33.5, -117.2, 34.75)
#
# # create a schema with no properties
# schema = {'geometry': 'Polygon', 'properties': {}}
#
# src_crs = fiona.crs.from_epsg(4326)
# shp = r'C:\Box\MCMGIS\Project_Based\RsrcDistSantaMonicaMtns\SouthLACoConnectivityPlan\data\vector\dbase_devel\LA_bbox_4326.shp'
#
# # create shapefile
# with fiona.open(shp, 'w', driver='ESRI Shapefile',
#                 crs=src_crs, schema=schema) as c:
#     c.write({'geometry': mapping(bbox), 'properties': {}})
#
#
#     elif mete_mode=='point':
#         with arcpy.da.InsertCursor(fp_feat, ["SHAPE@"]) as cursor:
#             if assembly_type == 'previous_val':
#                 x=math.cos(math.radians(bearing_dd))*segment_len + easting
#                 y=math.sin(math.radians(bearing_dd))*segment_len + northing
#                 point = arcpy.Point(x, y)
#                 cursor.insertRow([point])
#                 easting = copy.copy(x)
#                 northing = copy.copy(y)
#                 return(easting, northing)
#         del cursor
#
# # RENAMING 20260922
# # CAN DELETE
# fp_dir = r'C:\Box\MCM Projects\City of Seattle\Seattle City Light\23-024_South Fork Tolt Relicensing\11.0 Supplemental Files\Figures\USR\AQ01\Figs'
# for f in os.listdir(fp_dir):
#     try:
#         if os.path.splitext(f)[-1] == '.png':
#             comps = f.split('_AQ01_')
#             if len(comps)>2:
#                 fname_new = ''.join([comps[0], 'USR_AQ01_', comps[1],'_',comps[2]])
#                 os.rename(os.path.join(fp_dir,f), os.path.join(fp_dir,fname_new))
#                 print('NEW NAME:  ',fname_new)
#             else:
#                 print('ORIG NAME: ', f)
#     except IndexError:
#         pass

msg_str = (f"CURRENT SOURCE NOT IN DF_RESOURCE"
           "RESOURCED")
print(msg_str)