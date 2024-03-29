import os
import utilities
import pandas as pd
import numpy as np
import gdal
import matplotlib.pyplot as plt
import copy
import plotables as pltz
from math import floor, ceil, log10

fp_box_offline_d = utilities.get_path(28)
fp_JCB_10 = os.path.join(fp_box_offline_d, 'bathymetry_project\\JCB_1ft_2010_nad83.tif')
fp_diff_JCB = os.path.join(fp_box_offline_d, 'bathymetry_project\\JCB_diff_openTopo18_10_nad83_redo21.tif')
fp_JCB_18 = os.path.join(fp_box_offline_d, 'bathymetry_project\\JCBoyle_OpenTopography_2018_1ft.tif')
fp_copco_10_nad83 = os.path.join(fp_box_offline_d, 'bathymetry_project\\Copco_1ft_2010_nad83.tif')
fp_diff_copco_openTopo = os.path.join(fp_box_offline_d, 'bathymetry_project/Copco_diff_openTopo18_10_nad83.tif')
fp_copco_18 = os.path.join(fp_box_offline_d, 'bathymetry_project/Copco_OpenTopography_2018_1ft.tif')
fp_IG_10_nad83 = os.path.join(fp_box_offline_d, 'bathymetry_project\\IronGate_1ft_2010_nad83.tif')
fp_diff_IG_openTopo = os.path.join(fp_box_offline_d, 'bathymetry_project/IronGate_diff_openTopo18_10_nad83.tif')
fp_IG_18 = os.path.join(fp_box_offline_d, 'bathymetry_project\\Iron_Gate_OpenTopography_2018_download022021_processed.tif')

# 1) Get arrays clipped to common extent
ds1 = gdal.Open(fp_diff_copco_openTopo)
ds2 = gdal.Open(fp_diff_IG_openTopo)
ds3 = gdal.Open(fp_copco_10_nad83)
ds4 = gdal.Open(fp_IG_10_nad83)
ds5 = gdal.Open(fp_JCB_10)
ds6 = gdal.Open(fp_diff_JCB)
ds7 = gdal.Open(fp_IG_18)
ds8 = gdal.Open(fp_JCB_18)
ds9 = gdal.Open(fp_copco_18)

# arr_copco_diff, arr_copco_10 = utilities.get_overlap(ds1, ds3, output_args = True)
# arr_IG_diff, arr_IG_10 = utilities.get_overlap(ds2, ds4, output_args = True)
# arr_IG_diff, arr_IG_18 = utilities.get_overlap(ds2, ds4, output_args = True)

# ALREADY CLIPPED (ie don't need get overlap)
# Note got overlap using get_overlap and adjusting returns for just a txt file
arr_copco_diff = ds1.ReadAsArray()
# arr_copco_10 = ds3.ReadAsArray()
arr_IG_diff = ds2.ReadAsArray()
# arr_IG_10 = ds4.ReadAsArray()
# arr_JCB_10 = ds5.ReadAsArray()
arr_JCB_diff = ds6.ReadAsArray()
# arr_JCB_18 = ds8.ReadAsArray()
# arr_IG_18 = ds7.ReadAsArray()
# arr_copco_18 = ds9.ReadAsArray()

# print('shape slim: {} shape_orig: {}'.format(arr_copco_diff.shape, arr_copco_18.shape))

# replace nans with numpy nan value
# in this version nans were wierd negative neglible vals
# mask_copco = arr_copco_diff!=np.nanmin(arr_copco_diff)

# mask_IG = (arr_IG_diff!=np.nanmin(arr_IG_diff)) & (arr_IG_10 > 2000)
mask_IG = arr_IG_diff!=np.nanmin(arr_IG_diff)

# mask_JCB = arr_JCB_diff!=np.nanmin(arr_JCB_diff)

# # elevations from Greg assumed to be at 100% reservoir fill
# # https://www.pacificorp.com/content/dam/pcorp/documents/en/pacificorp/energy/hydro/klamath-river/relicensing/klamath-final-license-application/Exhibit_B_Project_Operation_and_Resource_Utilization.pdf
# elev_copco = 2607.5
# elev_IG = 2328
# elev_JCB = 3793.5
# elev_copco = np.full(arr_copco_diff.shape, elev_copco)
# elev_IG = np.full(arr_IG_diff.shape, elev_IG)
# elev_JCB = np.full(arr_JCB_diff.shape, elev_JCB)
# # table first
# acres_convert = 2.29568 * (10**-5)  #confirmed value 1/28/21 ZU
# arr_masked_copco_diff = arr_copco_diff[mask_copco]
# arr_masked_copco_10 = arr_copco_10[mask_copco]
# elev_masked_copco = elev_copco[mask_copco]
# arr_storage_copco = elev_masked_copco - arr_masked_copco_10
#
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
#
# # IG
# arr_masked_IG_diff = arr_IG_diff[mask_IG]
# arr_masked_IG_10 = arr_IG_10[mask_IG]
# elev_masked_IG = elev_IG[mask_IG]
# arr_storage_IG = elev_masked_IG - arr_masked_IG_10
#
# reservoir_storage_IG = round(np.mean(arr_storage_IG),1)
# reservoir_acre_IG = round(np.sum(mask_IG) * acres_convert, 1)
# reservoir_mean_change_IG = round(np.mean(arr_masked_IG_diff), 1)
# reservoir_min_change_IG = round(np.quantile(arr_masked_IG_diff, 0.01), 1)
# reservoir_max_change_IG = round(np.quantile(arr_masked_IG_diff, 0.99), 1)
# acre_feet_IG_2010 = round(np.mean(arr_storage_IG) * reservoir_acre_IG)
# pct_storage_change_IG = (-1) *  np.mean(arr_masked_IG_diff) / np.mean(arr_storage_IG) * 100
# acre_feet_change_IG = reservoir_mean_change_IG * reservoir_acre_IG
# acre_feet_IG_2018 = acre_feet_IG_2010 - acre_feet_change_IG
#
# arr_masked_JCB_diff = arr_JCB_diff[mask_JCB]
# arr_masked_JCB_10 = arr_JCB_10[mask_JCB]
# elev_masked_JCB = elev_JCB[mask_JCB]
# arr_storage_JCB = elev_masked_JCB - arr_masked_JCB_10
#
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
# pd.DataFrame.to_csv(df, os.path.join(fp_box_offline_d, 'sediment_summary_stats_all_2021redo.csv'))

# Figures
# replace nans with numpy nan value
# arr = arr_IG_diff
mask = mask_IG
reservoir = 'Iron Gate'
reservoir_formatted = 'Iron_Gate'

# # in this version nans were wierd negative neglible vals
# arr_diff = arr_copco_diff
# # note: Plotting difference change change from: int(round(item, 1)) to round(item,1)
# # in plottables.cb_readable
# pltz_obj = pltz.Plotables(arr_diff, mask)
# pltz_obj.trim_extent_nan('array')
# cbar_string = 'Elevation \u0394 (ft; 2018 minus 2002)'
# suptitle_string = '{}: Sediment \u0394 2002 to 2018'.format(reservoir)
# fp_out = os.path.join(utilities.get_path(28), 'bathymetry_project/for_matt_robart_20210128/{}_Sediment_Change_2018_2002.png'.format(reservoir_formatted))
# pltz_obj.basic_plot('mat_trimmed_nan_masked', cbar_string, suptitle_string, fp_out)

# arr_10 = arr_IG_10
# pltz_obj = pltz.Plotables(arr_10, mask)
# pltz_obj.trim_extent_nan('array')
# cbar_string = 'Elevation (ft)'
# suptitle_string = '{} Reservoir Bathymetry 2002'.format(reservoir)
# fp_out = os.path.join(utilities.get_path(28), 'bathymetry_project/for_matt_robart_20210128/{}_2002_reservoir_bathymetry.png'.format(reservoir_formatted))
# pltz_obj.basic_plot('mat_trimmed_nan_masked', cbar_string, suptitle_string, fp_out)

# # in this version nans were wierd negative neglible vals
# arr_18 = arr_IG_18
# pltz_obj = pltz.Plotables(arr_18, mask)
# pltz_obj.trim_extent_nan('array')
# cbar_string = 'Elevation (ft)'
# suptitle_string = '{} Reservoir Bathymetry 2018'.format(reservoir)
# fp_out = os.path.join(utilities.get_path(28), 'bathymetry_project/for_matt_robart_20210128/{}_2018_reservoir_bathymetry.png'.format(reservoir_formatted))
# pltz_obj.basic_plot('mat_trimmed_nan_masked', cbar_string, suptitle_string, fp_out)


# histograms
arr_list = [arr_JCB_diff, arr_copco_diff, arr_IG_diff]
max_loss = 0
max_gain = 0
hist_res_list = []
edges_list = []
reservoirs = ['J.C. Boyle', 'Copco', 'Iron Gate']
# fig_num = ['a)', 'b)', 'c)']
# from https://stackoverflow.com/questions/3410976/how-to-round-a-number-to-significant-figures-in-python
round_to_n = lambda x, n: round(x, -int(floor(log10(x))) + (n - 1))
for arr in arr_list:
    arr_nan = copy.copy(arr)
    arr_nan[arr_nan == np.min(arr_nan)] = np.nan
    arr_min = np.nanpercentile(arr_nan, 1)
    arr_max = np.nanpercentile(arr_nan, 99)
    arr_range = ceil(arr_max) - floor(arr_min)
    bin_edges = np.arange(floor(arr_min), ceil(arr_max) + 1, 0.25)
    max_loss = min(bin_edges[0], max_loss)
    max_gain = max(bin_edges[-1], max_gain)
    edges_list.append(bin_edges)

fig, ax = plt.subplots(3)
for idx in range(len(reservoirs)):
    reservoir = reservoirs[idx]
    # reservoir_formatted = reservoir.replace('.','').replace(' ', '_')
    edges = edges_list[idx]
    arr_nan = arr_list[idx]
    # temp = object with temp[0] = bin values
    temp = ax[idx].hist(arr_nan[~np.isnan(arr_nan)], edges[:-1], color = 'brown')
    # get ytickmarks
    # extract as function as some point
    yticks = temp[0]
    yticks = yticks.tolist()
    yticks.sort()
    middle_tick = yticks[-1]  * 0.5
    # pull ~middle and last highest value
    yticks = [middle_tick, yticks[-1]]
    # buffer top of tick marks
    yticks[-1] = yticks[-1] * 1.1
    yticks = [round_to_n(item, 5) for item in yticks]
    # value of 0 will create ValueError in log10(0)
    # add first tick manually
    yticks_final = [0]
    yticks_final.extend(yticks)
    ax[idx].set_yticks(yticks_final)
    ax[idx].set_xlim(max_loss, max_gain)
    ax[idx].set_xlabel('Difference in bathymetric surface (ft)')
    # title_str = '{} {}'.format(fig_num[idx], reservoir)
    ax[idx].set_title(reservoir, position = (0.85,0.7))
    ax[idx].label_outer()

fig.suptitle('Distribution of Bathymetric Change')
fig.text(0.01, 0.5, 'Frequency', va = 'center', rotation = 'vertical')
fname = 'histogram_2002_to_2018_change2.png'
fp_out = os.path.join(fp_box_offline_d, 'bathymetry_project\\for_matt_robart_20210128', fname)
plt.savefig(fp_out, dpi = 300)
