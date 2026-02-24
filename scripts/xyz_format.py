import numpy as np
import pandas as pd
import rasterio
from affine import Affine
import os

# here
# https://gis.stackexchange.com/questions/41180/gdal-doesnt-support-xyz-file
# 20260119 potter valley data
# Opening xyz and saving as tif. can output csv as well.
xyz = r"E:\projects\potter_valley\data_check\CapeHornPP_Lower_05ft_PGE_Bathy_2024.xyz"
xyz = r"E:\projects\potter_valley\data_check\Pillsbury_5ft_PGE_Bathy.xyz"
xyz = r"E:\projects\potter_valley\data_check\To_Be_Filed\CapeHornPP_2020 - Standard\CapeHornPP_Eel_2020.txt"
xyz = r"E:\projects\potter_valley\data_check\ScottDamPP_03ft_2020.xyz"
# dat = pd.read_table(xyz, sep=" ", header=None, dtype=float, low_memory=False)

# # export to csv
# dat.to_csv(r'E:\projects\potter_valley\data_check\Pillsbury_5ft_PGE_Bathy.csv')
# round_dig = 2
# xmin = round(dat[0].min(),round_dig)
# xmax = round(dat[0].max(), round_dig)
# ymin = round(dat[1].min(),round_dig)
# ymax = round(dat[1].max(), round_dig)
# dx = round(dat[0].drop_duplicates().sort_values().diff().median(), round_dig)
# dy = round(dat[1].drop_duplicates().sort_values().diff().median(), round_dig)
#
# # # Manually set spacing for caphorn because floating point precision created issues
# # dx, dy = 0.01,0.01
#
# xv = pd.Series(np.arange(xmin, xmax + dx, dx))
# xv = xv.round(2)
# yv = pd.Series(np.arange(ymin, ymax + dy, dy)[::-1])
# yv=yv.round(2)
# xi = pd.Series(xv.index.values, index=xv)
# yi = pd.Series(yv.index.values, index=yv)
# nodata = -9999.
# zv = np.ones((len(yi), len(xi)), np.float32) * nodata
#
# # # If KeyError, then not equally spaced points, run this to determine points missing
# # # NOT fruitful
# # xi_list, yi_list=[],[]
# # x_missing, y_missing = [],[]
# # for idx in dat.index:
# #     xt = dat.loc[idx,0]
# #     yt = dat.loc[idx,1]
# #     try:
# #         yi[yt]
# #         xi[xt]
# #         xi_list.append(xt)
# #         yi_list.append(yt)
# #     except KeyError:
# #         x_missing.append(xt)
# #         y_missing.append(yt)
# # df_missing = pd.DataFrame(np.column_stack([x_missing, y_missing]), columns = ['x','y'])
# #
# # xv = pd.Series(xi_list)
# # yv = pd.Series(yi_list)
# # xi2 = pd.Series(xv.index.values, index=xv)
# # yi2 = pd.Series(yv.index.values, index=yv)
# # yi = copy.copy(yi2)
# # xi = copy.copy(xi2)
#
# zv[yi[dat[1]].values, xi[dat[0]].values] = dat[2]
#
# # register geotransform based on upper-left corner
# transform = Affine(dx, 0, xmin, 0, -dy, ymax) * Affine.translation(-0.5, -0.5)
# file_out = r"E:\projects\potter_valley\data_check\ScottDamPP_03ft_2020_xyz.tif"
# with rasterio.open(file_out, "w", "GTiff", len(xi), len(yi), 1, "EPSG:6418",
#                    transform, rasterio.float32, nodata) as ds:
#     ds.write(zv.astype(np.float32), 1)

with open(xyz, 'r') as txt:
    l = []
    for ct, line in enumerate(txt):
        t = line.split(' ')
        l.append(t)
df = pd.DataFrame(l,columns = ['x','y','z'])
xmin, xmax, ymin, ymax = min(df['x']), max(df['x']), min(df['y']), max(df['y'])
nrows = len(df)
with open(r"E:\projects\potter_valley\data_check\ScottDamPP_03ft_2020_xyz_summary.txt",'w') as txt_file:
    stats_str = f"xmin: {xmin}\nxmax: {xmax}\nymin: {ymin}\nymax: {ymax}\nnumber of rows: {nrows}"
    txt_file.write(stats_str)
df.to_csv(r"E:\projects\potter_valley\data_check\ScottDamPP_03ft_2020.csv")


