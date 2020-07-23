import os
import utilities
import pandas as pd
import numpy as np
import gdal
import matplotlib.pyplot as plt
import copy
import plotables as pltz
import math

def get_overlap(ds1, ds2):
    # from here: https://gis.stackexchange.com/questions/16834/how-to-add-different-sized-rasters-in-gdal-so-the-result-is-only-in-the-intersec
    gt1 = ds1.GetGeoTransform()
    gt2 = ds2.GetGeoTransform()
    # note geotransform yields list with 6 items (https://gdal.org/user/raster_data_model.html):
    # [easting, x-transform, y-transform, northing, x-transform, y-transform]
    # translation: [west_bdry, step easting, step northing, north boundar, step easting, step northing]

    # r1 has left, top, right, bottom of dataset's bounds in geospatial coordinates.
    # note Raster<X,Y>Size = ncells
    # west, north, east, south
    r1 = [gt1[0], gt1[3], gt1[0] + (gt1[1] * ds1.RasterXSize), gt1[3] + (gt1[5] * ds1.RasterYSize)]

    # Do the same for dataset 2 ...
    r2 = [gt2[0], gt2[3], gt2[0] + (gt2[1] * ds2.RasterXSize), gt2[3] + (gt2[5] * ds2.RasterYSize)]
    intersection = [max(r1[0], r2[0]), min(r1[1], r2[1]), min(r1[2], r2[2]), max(r1[3], r2[3])]
    xsize1, ysize1 = ds1.RasterXSize, ds1.RasterXSize
    # x_offset1 = [math.ceil(intersection[0] - r2[0]), math.floor(intersection[2] - r2[0])]
    x_offset1 = [intersection[0] - r1[0], intersection[2] - r1[0]]
    x_buff1 = x_offset1[1] - x_offset1[0]
    x_offset2 = [intersection[0] - r2[0], intersection[2] - r2[0]]
    x_buff2 = x_offset2[1] - x_offset2[0]
    # the offsets are from west to east easting vals.  For some reason buffer is used
    # for the second subset position. It's the distance from the first easting
    # to the second eastng.  Ditto for y_offset but from north to south
    y_offset1 = [r1[1] - intersection[1], r1[1] - intersection[3]]
    y_buff1 = y_offset1[1] - y_offset1[0]
    y_offset2 = [r2[1] - intersection[1], r2[1] - intersection[3]]
    y_buff2 = y_offset2[1] - y_offset2[0]
    print('x_extents: ', ds2.RasterXSize + intersection[0])
    print('y_extents: ', ds2.RasterYSize - intersection[1])
    print('intersection: ', intersection)
    print('gt1: ', gt1)
    print('gt2: ', gt2)
    print('xoffset: {} x_buff: {}'.format(math.ceil(x_offset1[0]), math.floor(x_buff1)))
    print('yoffset: {} y_buff: {}'.format(math.ceil(y_offset1[0]), math.floor(y_buff1)))
    print('xoffset2: {} x_buff: {}'.format(math.ceil(x_offset2[0]), math.floor(x_buff2)))
    print('yoffset2: {} y_buff: {}'.format(math.ceil(y_offset2[0]), math.floor(y_buff2)))
    arr1 = ds1.ReadAsArray(math.ceil(x_offset1[0]), math.ceil(y_offset1[0]), math.floor(x_buff1), math.floor(y_buff1))
    arr2 = ds2.ReadAsArray(math.ceil(x_offset2[0]), math.ceil(y_offset2[0]), math.floor(x_buff2), math.floor(y_buff2))
    return(arr1, arr2)

# file paths
fp_copco_10 = os.path.join(utilities.get_path(22), 'bathymetry_project/Bathy_1ft_Copco_2010.tif')
fp_IG_10 = os.path.join(utilities.get_path(22), 'bathymetry_project/Bathy_1ft_IG_2010.tif')
fp_diff_copco = os.path.join(utilities.get_path(22), 'bathymetry_project/2018_2010_diff_copco_exactly_1ft.tif')
fp_diff_IG = os.path.join(utilities.get_path(22), 'bathymetry_project/2018_2010_diff_IG_exactly_1ft.tif')

# 1) Get arrays clipped to common extent
ds1 = gdal.Open(fp_diff_copco)
ds2 = gdal.Open(fp_diff_IG)
ds3 = gdal.Open(fp_copco_10)
ds4 = gdal.Open(fp_IG_10)
arr_copco_diff, arr_copco_10 = get_overlap(ds1, ds3)
arr_IG_diff, arr_IG_10 = get_overlap(ds2, ds4)

# DELETE Just to determine non-nans
c10 = np.sum(arr_copco_10 == np.min(arr_copco_10))
cdiff = np.sum(arr_copco_diff == np.min(arr_copco_diff))
IG10 = np.sum(arr_IG_10 == np.min(arr_IG_10))
IGdiff = np.sum(arr_IG_diff == np.min(arr_IG_diff))
print('num c10 {} cdiff {} IG10 {} IGdiff {}'.format(c10, cdiff, IG10, IGdiff))
#
print('min {} {}'.format(np.min(arr_copco_10), np.min(arr_copco_diff)))
print('min {} {}'.format(np.min(arr_IG_10), np.min(arr_IG_diff)))


# THIS WILL NEED TO BE MODIFIED ON CUSTOM BASIS to mask out nans.  IG for some
# reason had two nans prob from diffing
mask_IG = (arr_IG_diff != np.min(arr_IG_diff)) & (arr_IG_10 > -100)
IG_diff_masked = np.min(arr_IG_diff[mask_IG])
IG_10_masked = np.min(arr_IG_10[mask_IG])
print('min diff {} 10 {}'.format(IG_diff_masked, IG_10_masked))
print(type(arr_copco_diff), type(arr_copco_diff[0,0]))
print(type(arr_IG_diff), type(arr_IG_10[0,0]))

print('shape slim: {} shape_orig: {}'.format(arr_copco_diff.shape, arr_copco_10.shape))
print('shape slim: {} shape_orig: {}'.format(arr_IG_diff.shape, arr_IG_10.shape))
# replace nans with numpy nan value
# in this version nans were wierd negative neglible vals
print('line 20')
mask_copco = arr_copco_diff!=np.nanmin(arr_copco_diff)
# mask_IG = (arr_IG_diff>-100) & (arr_IG_diff<100)
mask_IG = (arr_IG_diff!=np.nanmin(arr_IG_diff)) & (arr_IG_10 > 2000)
print('IG sum: {}  copco sum: {}'.format(np.sum(mask_IG), np.sum(mask_copco)))
# elevations from Greg assumed to be at 100% reservoir fill
elev_copco = 2607.5
elev_IG = 2328
elev_copco = np.full(arr_copco_diff.shape, elev_copco)
elev_IG = np.full(arr_IG_diff.shape, elev_IG)
# table first
print('line 28')
acres_convert = 2.29568 * (10**-5)
arr_masked_copco_diff = arr_copco_diff[mask_copco]
arr_masked_copco_10 = arr_copco_10[mask_copco]
elev_masked_copco = elev_copco[mask_copco]
arr_storage_copco = elev_masked_copco - arr_masked_copco_10

#
reservoir_storage_copco = round(np.mean(arr_storage_copco),1)
reservoir_acre_copco = round(np.sum(mask_copco) *acres_convert, 1)
reservoir_mean_change_copco = round(np.mean(arr_masked_copco_diff), 1)
reservoir_min_change_copco = round(np.quantile(arr_masked_copco_diff, 0.01), 1)
reservoir_max_change_copco = round(np.quantile(arr_masked_copco_diff, 0.99), 1)
acre_feet_copco = round(np.mean(arr_storage_copco) * reservoir_acre_copco)
pct_storage_change_copco = (-1) *  np.mean(arr_masked_copco_diff) / np.mean(arr_storage_copco) * 100
acre_feet_change_copco = reservoir_mean_change_copco * reservoir_acre_copco
#
# IG
print('line 38')
arr_masked_IG_diff = arr_IG_diff[mask_IG]
arr_masked_IG_10 = arr_IG_10[mask_IG]
print('IG min {} copco min {}'.format(np.min(arr_masked_IG_10), np.min(arr_masked_copco_10)))
print('mean bath copco {} IG {}'.format(np.mean(arr_masked_copco_10), np.mean(arr_masked_IG_10)))
elev_masked_IG = elev_IG[mask_IG]
arr_storage_IG = elev_masked_IG - arr_masked_IG_10
print('mean storage copco {} IG {}'.format(np.mean(arr_storage_copco), np.mean(arr_storage_IG)))
reservoir_storage_IG = round(np.mean(arr_storage_IG),1)
reservoir_acre_IG = round(np.sum(mask_IG) * acres_convert, 1)
reservoir_mean_change_IG = round(np.mean(arr_masked_IG_diff), 1)
reservoir_min_change_IG = round(np.quantile(arr_masked_IG_diff, 0.01), 1)
reservoir_max_change_IG = round(np.quantile(arr_masked_IG_diff, 0.99), 1)
acre_feet_IG = round(np.mean(arr_storage_IG) * reservoir_acre_IG)
pct_storage_change_IG = (-1) *  np.mean(arr_masked_IG_diff) / np.mean(arr_storage_IG) * 100
acre_feet_change_IG = reservoir_mean_change_IG * reservoir_acre_IG

reservoirs = ['Copco1', 'IronGate']
res_acre = [reservoir_acre_copco, reservoir_acre_IG]
res_storage = [reservoir_storage_copco, reservoir_storage_IG]
acre_feet = [acre_feet_copco, acre_feet_IG]
res_mean = [reservoir_mean_change_copco, reservoir_mean_change_IG]
res_min = [reservoir_min_change_copco, reservoir_min_change_IG]
res_max = [reservoir_max_change_copco, reservoir_max_change_IG]
pct_storage = [pct_storage_change_copco, pct_storage_change_IG]
pct_storage = [round(pct,1) for pct in pct_storage]
acre_feet_change = [acre_feet_change_copco, acre_feet_change_IG]
acre_feet_change = [round(ac_change, 1) for ac_change in acre_feet_change]
df = pd.DataFrame(np.column_stack([res_mean, res_min, res_max, res_acre, res_storage, acre_feet,
                        pct_storage, acre_feet_change]),
                columns = ['mean sediment change (feet)', '0.01 quantile sediment change (feet)',
                        '0.99 quantile sediment change (feet)', 'reservoir size (acres)', 'reservoir depth (avg)',
                        'reservoir storage (acre-feet)', 'percent storage change',
                        'acre-feet change'],
                index = reservoirs)
print(df)
pd.DataFrame.to_csv(df, os.path.join(utilities.get_path(22), 'sediment_summary_stats.csv'))

# Figures
# replace nans with numpy nan value
arr = arr_copco_diff
mask = mask_copco
# in this version nans were wierd negative neglible vals
pltz_obj = pltz.Plotables(arr, mask)
pltz_obj.trim_extent_nan('array')
cbar_string = 'Elevation \u0394 (ft; 2018 minus 2010)'
reservoir = 'Copco'
suptitle_string = '{}: Sediment \u0394 2010 to 2018'.format(reservoir)
fp_out = os.path.join(utilities.get_path(22), 'bathymetry_project/{}_Sediment_Change_2018_2010b.png'.format(reservoir))
pltz_obj.basic_plot('mat_trimmed_nan_masked', cbar_string, suptitle_string, fp_out)

# fig, axes = plt.subplots(nrows = 1, ncols = 1)
# # h = axes.imshow(diff_map, cmap = self.cmap_marks, norm=MidpointNormalize(midpoint = 0))
# h = axes.imshow(arr_IG_10)
# # IG lims
# # h.set_clim(2170, 2330)
# # h.set_clim(-3, 3)
# # axes.axis('off')
# cbar = fig.colorbar(h, ax=axes, fraction = 0.04, pad = 0.04, \
#         orientation = 'vertical', extend = 'both')
# cbar.ax.tick_params(labelsize = 8)
# plt.show()
