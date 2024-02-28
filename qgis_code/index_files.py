from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import MultiPolygon
import geopandas as gpd
import numpy as np

# # 20230823
# # Creating indices with ll beginning tile coordinates, num rows, num cols and overlap.  Set overlap to 0
# # if none desired
#
# x0 = 1380000
# y0 = 439500
# # total overlap for two adjacent indices
# overlap = 0.05
# # split between the two tiles
# o_factor = (1-overlap)
# layout_width = 12.3
# layout_ht = 8.2
# ft_to_in_scale = 3000
# # multiply by 0.5 because we are starting at centroid.  dx + dx = full indice width
# dx = (ft_to_in_scale * layout_width) *0.5
# dy = (ft_to_in_scale * layout_ht) * 0.5
# rows = 3
# cols = 5
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
# gdr = gpd.GeoDataFrame({'feature': features, 'geometry':polys}, crs="EPSG:6449")
# gdr.to_file(r'E:\box_offline\projects\magic_valley\parcels\magic_valley_inundation_index_1to3000_v1.shp')

# load df
fp_shp = r"C:\Box\MCM Projects\Magic Dam Wood Hydro - Part 12 and other work\24-009 Magic Dam Inundation Mapping" \
          r"\6.0 Plans and Specs\6.6_GIS\GIS_files\data_original\staging\magic_valley_inundation_index_1to4000_SMK.shp"
df = gpd.read_file(fp_shp)
poly = False

# Part 2
# Generate 3 points from edited and finalized tiles
triangles = []
pct = 0.2
# From here https://gis.stackexchange.com/questions/287306/listing-all-polygon-vertices-coordinates-using-geopandas
# get coords into gpd df
#
for g in df.geometry:
    x,y = g.exterior.coords.xy
    # x and y are lists/tuples with n=num vertices points
    dfx = max(set(x)) - min(set(x))
    dfy = max(set(y)) - min(set(y))
    xmin, xmax = min(set(x)), max(set(x))
    ymin, ymax = min(set(y)), max(set(y))
    xmin_adj =xmin + (pct * dfx)
    xmax_adj = xmin + ((1-pct) * dfx)
    ymin_adj = ymin + (pct * dfy)
    ymax_adj = ymin + ((1-pct) *dfy)
    xmid = xmin + dfx/2
    ymid = ymin + dfy/2
    ul,ur = (xmin_adj, ymax_adj), (xmax_adj,ymax_adj)
    ll,lr = (xmin_adj,ymin_adj),(xmax_adj,ymin_adj)
    u_cent = (xmid,ymax_adj)
    rt_cent = (xmax_adj,ymid)
    l_cent = (xmid,ymin_adj)
    lt_cent = (xmin_adj,ymid)

    # create three reference points per tile
    # triangle_types = ['upper','right','lower','left']
    # d = dict(zip(list(range(4))),triangle_types)
    if poly:
        upper_coords = Polygon([u_cent,lr,ll])
        right_coords = Polygon([rt_cent,ll,ul])
        lower_coords = Polygon([l_cent,ul,ur])
        left_coords = Polygon([lt_cent, ur,lr])
        triangles.append(upper_coords)
    else:
        upper_coords = [Point(p) for p in [u_cent, lr, ll]]
        right_coords = Polygon([rt_cent, ll, ul])
        lower_coords = Polygon([l_cent, ul, ur])
        left_coords = Polygon([lt_cent, ur, lr])
        triangles.extend(upper_coords)
features = [i for i in range(len(triangles))]
gdr = gpd.GeoDataFrame({'feature': features, 'geometry':triangles})
gdr.to_file(r"C:\Box\MCM Projects\Magic Dam Wood Hydro - Part 12 and other work" \
            r"\24-009 Magic Dam Inundation Mapping\6.0 Plans and Specs\6.6_GIS\GIS_files\data_original\staging\3pts_1to4000_SMK.shp")




