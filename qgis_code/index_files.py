from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import MultiPolygon
from shapely.geometry import LineString
import geopandas as gpd
import numpy as np
#
# 20230823
# Creating indices with ll beginning tile coordinates, num rows, num cols and overlap.  Set overlap to 0
# if none desired

# x0 = 9043750
# y0 = 625850
# # total overlap for two adjacent indices
# overlap = 0.05
# # split between the two tiles
# o_factor = (1-overlap)
# layout_width = 12
# layout_ht = 8
# ft_to_in_scale = 1000
# # multiply by 0.5 because we are starting at centroid.  dx + dx = full indice width
# dx = (ft_to_in_scale * layout_width) *0.5
# dy = (ft_to_in_scale * layout_ht) * 0.5
# rows = 12
# cols = 1
# polys = []
# for c in range(cols):
#     for r in range(rows):
#         x = x0 + 2*dx*c*o_factor
#         y = y0 + 2*dy*r*o_factor
#         ul = (x-dx, y+dy)
#         ur = (x+dx, y+dy)
#         lr = (x+dx, y-dy)
#         ll = (x-dx, y-dy)
#         polys.append(Polygon([ul,ur,lr,ll]))
# features = [i for i in range(len(polys))]
# crs = "EPSG:6559"
# gdr = gpd.GeoDataFrame({'feature': features, 'geometry':polys}, crs=crs)
# fp_out = r'C:\Box\MCMGIS\Project_Based\Wallowa_Dam\gis_data\data_received\indices\wallowa_indices_v2.shp'
# gdr.to_file(fp_out)

# load df
fp_shp = r"C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\DLA\staging\indices\greengen_1in_to_300ft_24x32.shp"
df = gpd.read_file(fp_shp)
crs = "ESRI:103004"
df.to_crs(crs,inplace=True)

poly = False
# Part 2
# Generate 3 points from edited and finalized tiles
triangles = []
triangle_num = []
fld1_list = []
tb = ['t1']*3 + ['t2']*3
pct = 0.2
# From here https://gis.stackexchange.com/questions/287306/listing-all-polygon-vertices-coordinates-using-geopandas
# get coords into gpd df
#
for idx, g in enumerate(df.geometry):
    x,y = g.exterior.coords.xy
    pts = [Point([xp,yp]) for xp,yp in zip(x,y)]
    line1 = LineString([pts[0],pts[1]])
    line2 = LineString([pts[1], pts[2]])
    if line1.length>line2.length:
        start_idx = 0
    else:
        start_idx = 1
    # create line3
    diag1 = LineString([pts[start_idx], pts[start_idx + 2]])
    diag2 = LineString([pts[start_idx + 1], pts[start_idx + 3]])
    p1 = diag1.interpolate(diag1.length * pct)
    p4 = diag1.interpolate(diag1.length * (-pct))
    p2 = diag2.interpolate(diag2.length * pct)
    p5 = diag2.interpolate(diag2.length * (-pct))
    longline1 = LineString([pts[start_idx], pts[start_idx+1]])
    longline2 = LineString([pts[start_idx+2], pts[start_idx + 3]])
    center1 = longline1.interpolate(longline1.length / 2)
    center2 = longline2.interpolate(longline2.length / 2)
    cross_axis = LineString([center1, center2])
    p6 = cross_axis.interpolate(cross_axis.length * pct)
    p3 = cross_axis.interpolate(cross_axis.length * (-pct))
    final_coords = [Point(p) for p in [p1,p2,p3,p4,p5,p6]]
    triangles.extend(final_coords)
    triangle_num.extend(tb)
    fld1 = [df.loc[idx,'sheet_num']]*6
    fld1_list.extend(fld1)

features = [i for i in range(len(triangles))]
gdr = gpd.GeoDataFrame({'feature': features, 'triangle_num': triangle_num, 'sheet_num':fld1_list, 'geometry':triangles},crs = df.crs)
gdr.to_file(r"C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\DLA\staging\indices\greengen_1in_to_300ft_24x32_3pts.shp")



