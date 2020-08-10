import os
import utilities
import pandas as pd
import numpy as np
import gdal
import matplotlib.pyplot as plt
import copy
import plotables as pltz
import math

# file paths PRIOR to getting surgical with this shit
fp_box_offline = 'C:\\Users\\uhlmann\\box_offline'
fp_copco_10 = os.path.join(utilities.get_path(22), 'bathymetry_project/Bathy_1ft_Copco_2010.tif')
fp_IG_10 = os.path.join(utilities.get_path(22), 'bathymetry_project/Bathy_1ft_IG_2010.tif')
fp_diff_copco = os.path.join(utilities.get_path(22), 'bathymetry_project/2018_2010_diff_copco_exactly_1ft.tif')
fp_diff_IG = os.path.join(utilities.get_path(22), 'bathymetry_project/2018_2010_diff_IG_exactly_1ft.tif')
fp_JCB_10 = os.path.join(fp_box_offline, 'bathymetry_project\\Bathy_1ft_JCBoyle_2010.tif')
fp_diff_JCB = os.path.join(fp_box_offline, 'bathymetry_project\\2018_2010_diff_JCB_1ft.tif')

# OpenTopo datasets
fp_copco_10_nad83 = os.path.join(utilities.get_path(22), 'bathymetry_project\\Copco_1ft_2010_nad83.tif')
fp_diff_copco_openTopo = os.path.join(utilities.get_path(22), 'bathymetry_project/Copco_diff_openTopo18_10_nad83.tif')
fp_IG_10_nad83 = os.path.join(utilities.get_path(22), 'bathymetry_project\\IronGate_1ft_2010_nad83.tif')
fp_diff_IG_openTopo = os.path.join(utilities.get_path(22), 'bathymetry_project/IronGate_diff_openTopo18_10_nad83.tif')

# Other layers used
fp_IG_18_OpenTopo_3m = os.path.join(fp_box_offline, 'Bathymetry_OpenTopography_2018/rasters_sdem/IronGate_2018_3m.tif')
fp_IG_10_2m = os.path.join(fp_box_offline, 'bathymetry_project/Bathy_2ft_IronGate.tif')

# 1) Get arrays clipped to common extent
ds1 = gdal.Open(fp_diff_copco_openTopo)
ds2 = gdal.Open(fp_diff_IG_openTopo)
ds3 = gdal.Open(fp_copco_10_nad83)
ds4 = gdal.Open(fp_IG_10_nad83)
ds5 = gdal.Open(fp_JCB_10)
ds6 = gdal.Open(fp_diff_JCB)

arr_copco_diff, arr_copco_10 = utilities.get_overlap(ds1, ds3, output_args = True)
arr_IG_diff, arr_IG_10 = utilities.get_overlap(ds2, ds4, output_args = True)

# ALREADY CLIPPED (ie don't need get overlap)
# Note got overlap using get_overlap and adjusting returns for just a txt file
arr_JCB_10 = ds5.ReadAsArray()
arr_JCB_diff = ds6.ReadAsArray()

# THIS WILL NEED TO BE MODIFIED ON CUSTOM BASIS to mask out nans.  IG for some
# reason had two nans prob from diffing
mask_IG = (arr_IG_diff != np.min(arr_IG_diff)) & (arr_IG_10 > -100)
IG_diff_masked = np.min(arr_IG_diff[mask_IG])
IG_10_masked = np.min(arr_IG_10[mask_IG])

print('shape slim: {} shape_orig: {}'.format(arr_copco_diff.shape, arr_copco_10.shape))
print('shape slim: {} shape_orig: {}'.format(arr_IG_diff.shape, arr_IG_10.shape))

# replace nans with numpy nan value
# in this version nans were wierd negative neglible vals
mask_copco = arr_copco_diff!=np.nanmin(arr_copco_diff)
# mask_IG = (arr_IG_diff>-100) & (arr_IG_diff<100)
mask_IG = (arr_IG_diff!=np.nanmin(arr_IG_diff)) & (arr_IG_10 > 2000)

mask_JCB = arr_JCB_diff!=np.nanmin(arr_JCB_diff)

# elevations from Greg assumed to be at 100% reservoir fill
# https://www.pacificorp.com/content/dam/pcorp/documents/en/pacificorp/energy/hydro/klamath-river/relicensing/klamath-final-license-application/Exhibit_B_Project_Operation_and_Resource_Utilization.pdf
elev_copco = 2607.5
elev_IG = 2328
elev_JCB = 3793.5
elev_copco = np.full(arr_copco_diff.shape, elev_copco)
elev_IG = np.full(arr_IG_diff.shape, elev_IG)
elev_JCB = np.full(arr_JCB_diff.shape, elev_JCB)
# table first
acres_convert = 2.29568 * (10**-5)
arr_masked_copco_diff = arr_copco_diff[mask_copco]
arr_masked_copco_10 = arr_copco_10[mask_copco]
elev_masked_copco = elev_copco[mask_copco]
arr_storage_copco = elev_masked_copco - arr_masked_copco_10

#
# reservoir_storage_copco = round(np.mean(arr_storage_copco),1)
# reservoir_acre_copco = round(np.sum(mask_copco) *acres_convert, 1)
# reservoir_mean_change_copco = round(np.mean(arr_masked_copco_diff), 1)
# reservoir_min_change_copco = round(np.quantile(arr_masked_copco_diff, 0.01), 1)
# reservoir_max_change_copco = round(np.quantile(arr_masked_copco_diff, 0.99), 1)
# acre_feet_copco_2010 = round(np.mean(arr_storage_copco) * reservoir_acre_copco)
# pct_storage_change_copco = (-1) *  np.mean(arr_masked_copco_diff) / np.mean(arr_storage_copco) * 100
# acre_feet_change_copco = reservoir_mean_change_copco * reservoir_acre_copco
# acre_feet_copco_2018 = acre_feet_copco_2010 - acre_feet_change_copco

# IG
arr_masked_IG_diff = arr_IG_diff[mask_IG]
arr_masked_IG_10 = arr_IG_10[mask_IG]
elev_masked_IG = elev_IG[mask_IG]
arr_storage_IG = elev_masked_IG - arr_masked_IG_10

# reservoir_storage_IG = round(np.mean(arr_storage_IG),1)
# reservoir_acre_IG = round(np.sum(mask_IG) * acres_convert, 1)
# reservoir_mean_change_IG = round(np.mean(arr_masked_IG_diff), 1)
# reservoir_min_change_IG = round(np.quantile(arr_masked_IG_diff, 0.01), 1)
# reservoir_max_change_IG = round(np.quantile(arr_masked_IG_diff, 0.99), 1)
# acre_feet_IG_2010 = round(np.mean(arr_storage_IG) * reservoir_acre_IG)
# pct_storage_change_IG = (-1) *  np.mean(arr_masked_IG_diff) / np.mean(arr_storage_IG) * 100
# acre_feet_change_IG = reservoir_mean_change_IG * reservoir_acre_IG
# acre_feet_IG_2018 = acre_feet_IG_2010 - acre_feet_change_IG

arr_masked_JCB_diff = arr_JCB_diff[mask_JCB]
arr_masked_JCB_10 = arr_JCB_10[mask_JCB]
elev_masked_JCB = elev_JCB[mask_JCB]
arr_storage_JCB = elev_masked_JCB - arr_masked_JCB_10

# reservoir_storage_JCB = round(np.mean(arr_storage_JCB),1)
# reservoir_acre_JCB = round(np.sum(mask_JCB) *acres_convert, 1)
# reservoir_mean_change_JCB = round(np.mean(arr_masked_JCB_diff), 1)
# reservoir_min_change_JCB = round(np.quantile(arr_masked_JCB_diff, 0.01), 1)
# reservoir_max_change_JCB = round(np.quantile(arr_masked_JCB_diff, 0.99), 1)
# acre_feet_JCB_2010 = round(np.mean(arr_storage_JCB) * reservoir_acre_JCB)
# pct_storage_change_JCB = (-1) *  np.mean(arr_masked_JCB_diff) / np.mean(arr_storage_JCB) * 100
# acre_feet_change_JCB = reservoir_mean_change_JCB * reservoir_acre_JCB
# acre_feet_JCB_2018 = acre_feet_JCB_2010 - acre_feet_change_JCB
#
# reservoirs = ['Copco1', 'IronGate', 'JCBoyle']
# res_acre = [reservoir_acre_copco, reservoir_acre_IG, reservoir_acre_JCB]
# res_storage = [reservoir_storage_copco, reservoir_storage_IG, reservoir_storage_JCB]
# acre_feet_2010 = [acre_feet_copco_2010, acre_feet_IG_2010, acre_feet_JCB_2010]
# acre_feet_2018 = [acre_feet_copco_2018, acre_feet_IG_2018, acre_feet_JCB_2018]
# res_mean = [reservoir_mean_change_copco, reservoir_mean_change_IG, reservoir_mean_change_JCB]
# res_min = [reservoir_min_change_copco, reservoir_min_change_IG, reservoir_min_change_JCB]
# res_max = [reservoir_max_change_copco, reservoir_max_change_IG, reservoir_max_change_JCB]
# pct_storage = [pct_storage_change_copco, pct_storage_change_IG, pct_storage_change_JCB]
# pct_storage = [round(pct,1) for pct in pct_storage]
# acre_feet_change = [acre_feet_change_copco, acre_feet_change_IG, acre_feet_change_JCB]
# acre_feet_change = [round(ac_change, 1) for ac_change in acre_feet_change]
# df = pd.DataFrame(np.column_stack([res_mean, res_min, res_max, res_acre, res_storage, acre_feet_2018, acre_feet_2010,
#                         acre_feet_change, pct_storage]),
#                 columns = ['mean sediment change (feet)', '0.01 quantile sediment change (feet)',
#                         '0.99 quantile sediment change (feet)', 'reservoir size (acres)',
#                         'reservoir depth (avg)', '2018 reservoir storage (acre-ft)',
#                         '2010 reservoir storage (acre-feet)','acre-feet change',
#                         'percent storage change'],
#                 index = reservoirs)
# print(df)
# pd.DataFrame.to_csv(df, os.path.join(utilities.get_path(22), 'sediment_summary_stats_all_openTopo.csv'))

# Figures
# replace nans with numpy nan value
arr = arr_copco_diff
mask = mask_copco
# in this version nans were wierd negative neglible vals
pltz_obj = pltz.Plotables(arr, mask)
pltz_obj.trim_extent_nan('array')
cbar_string = 'Elevation \u0394 (ft; 2018 minus 2002)'
reservoir = 'Copco'
suptitle_string = '{}: Sediment \u0394 2002 to 2018'.format(reservoir)
fp_out = os.path.join(utilities.get_path(22), 'bathymetry_project/{}_Sediment_Change_2018_2002.png'.format(reservoir))
pltz_obj.basic_plot('mat_trimmed_nan_masked', cbar_string, suptitle_string, fp_out)
#
# # fig, axes = plt.subplots(nrows = 1, ncols = 1)
# # # h = axes.imshow(diff_map, cmap = self.cmap_marks, norm=MidpointNormalize(midpoint = 0))
# # h = axes.imshow(arr_IG_10)
# # # IG lims
# # # h.set_clim(2170, 2330)
# # # h.set_clim(-3, 3)
# # # axes.axis('off')
# # cbar = fig.colorbar(h, ax=axes, fraction = 0.04, pad = 0.04, \
# #         orientation = 'vertical', extend = 'both')
# # cbar.ax.tick_params(labelsize = 8)
# # plt.show()
