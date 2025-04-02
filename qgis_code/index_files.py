from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import MultiPolygon
from shapely.geometry import LineString
import geopandas as gpd
import numpy as np
#

# # 20240918
# # Ran again for relative scale;  first adapted for in_to_feet for wallowa
# # Creating indices with ll beginning tile coordinates, num rows, num cols and overlap.  Set overlap to 0
# # if none desired
#
# x0 = 1408250
# y0 = 257750
# # total overlap for two adjacent indices
# overlap = 0.05
# # split between the two tiles
# o_factor = (1-overlap)
# layout_width = 16
# layout_ht = 7.8
# # Set true for relative, false for 1 inch = n feet scale convention
# relative=True
# ft_to_in_scale = 1000
# relative_scale = 24000
# # multiply by 0.5 because we are starting at centroid.  dx + dx = full indice width
# # _relative and _in2feet are for the two scale representations.  Set one above along with boolean
# dx_relative = (relative_scale * layout_width * (1/12)) * 0.5
# dy_relative = (relative_scale * layout_ht * (1/12)) * 0.5
# dx_in2feet = (ft_to_in_scale * layout_width) *0.5
# dy_in2feet = (ft_to_in_scale * layout_ht) * 0.5
# if relative:
#     dx = dx_relative
#     dy = dy_relative
# else:
#     dx = dx_in2feet
#     dy = dy_in2feet
# rows = 3
# cols = 3
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
# crs = "EPSG:2926"
# gdr = gpd.GeoDataFrame({'feature': features, 'geometry':polys}, crs=crs)
# fp_out = r'C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\staging\indices\cultural_SA_shpo.shp'
# gdr.to_file(fp_out)

# load df
fp_shp = r"C:\Box\MCM Projects\Magic Dam Wood Hydro - Part 12 and other work\24-009 Magic Dam Inundation Mapping" \
          r"\6.0 Plans and Specs\6.6_GIS\GIS_files\data_original\staging\magic_dam_index_zoomins_1to500.shp"
fp_shp =r"C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\DLA\staging\indices\ExhibitG_DDP_v2.shp"
gdb=r'C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Maps\DLA\map_docs\greengen_ferc\greengen_ferc_v2.gdb'
df = gpd.read_file(fp_shp)
# df = gpd.read_file(gdb, layer='ExhibitG_DDP_v2')
crs = "EPSG:2226"
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
    fld1 = [df.loc[idx,'page_num']]*6
    # fld1=[1]*6
    fld1_list.extend(fld1)

features = [i for i in range(len(triangles))]
gdr = gpd.GeoDataFrame({'feature': features, 'triangle_num': triangle_num, 'sheet_num':fld1_list, 'geometry':triangles},crs = df.crs)
gdr.to_file(r"C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\DLA\staging\indices\ExhibitG_DDP_v2_ref_pts.shp")





