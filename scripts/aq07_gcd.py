import pandas as pd
import os

# # cloudcompare
# clouds = [c1, c2]
#
# param_file =
# cloudComPy.M3C2.computeM3C2()
#
# in_cloud =
# cloudComPy.RasterizeGeoTiffOnly(in_cloud, gridStep=1.5, )

# # Adding 0 to improper NV5 index for 2023
# csv = r"C:\Users\ZacharyUhlmann\Documents\staging\tolt\AQ07\gcd\2023\2023_Tiles_GCD_test.csv"
# df=pd.read_csv(csv)
#
# for idx in df.index:
#     orig = df.loc[idx, 'Tile_ID']
#     p1, p2 = orig.split('_')
#     new = f"{p1}_0{p2}"
#     df.at[idx, 'Tile_ID_new'] = new
# df.to_csv(csv)

# #  basically write_folder_contents to csv
# las_dir = r'C:\Users\ZacharyUhlmann\Documents\staging\tolt\2024_LiDAR\2024_LAS\2024_LAS\Full_Classification\Full_Classification'
# csv = r"C:\Users\ZacharyUhlmann\Documents\staging\tolt\AQ07\gcd\2024_las_inv.csv"
# las_files = [f for f in os.listdir(las_dir) if f[-4:]=='.las']
# df = pd.DataFrame(las_files, columns = ['las_name'])

# # Add las_name from path
# csv_inv = r'C:\Users\ZacharyUhlmann\Documents\staging\tolt\AQ07\gcd\2024\2024_las_inv.csv'
# df = pd.read_csv(csv_inv)
# Tile_ID = [os.path.split(fp)[-1][:-4] for fp in df['las_path']]
# df['las_name']=Tile_ID
# df.to_csv(csv_inv)

# # Used when pdal tindex was failing and could not follow pdal tutorial on tile index to merge pipeline
# # Note - due to character limit in CL, had to split command into two command (two merged tiles) and then merge into single
# # 20251114
# fname_merged = '2020_merged.las'
# las_dir = r'C:\Users\ZacharyUhlmann\Documents\staging\tolt\AQ07\gcd\2023\2023_las_BE'
# txt_path = os.path.join(las_dir, '2023_las_PDAL_CL_call.txt')
# las_files = [fn for fn in os.listdir(las_dir) if os.path.splitext(fn)[-1] in ['.las','.laz']]
# str1 = ' '.join(las_files)
# pdal_str = f"pdal merge {str1} {fname_merged}"
# with open(txt_path, 'w') as t:
#     t.write(pdal_str)

# Histgram
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import copy

# def get_stats(al, fname, fp_csv):
#     m,mx,mn,sd = [],[],[],[]
#     for a in al:
#         m.append(round(np.mean(a),2))
#         sd.append(round(np.std(a),2))
#         mn.append(round(np.min(a),2))
#         mx.append(round(np.max(a),2))
#     df = pd.DataFrame(np.column_stack([fname, m, mn, mx, sd]), columns=['fname','mean', 'min','max',' std'])
#     df.to_csv(fp_csv)
#
#
# fp_2024_2020 = r"C:\Users\ZacharyUhlmann\Documents\staging\tolt\AQ07\gcd\m3c2_processed\2024_2020_m3c2.tif"
# fp_2024_2014 = r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\field_planning\study_data\gcd\m3c2_processed\2024_2014_m3c2.tif"
# ds1 = gdal.Open(fp_2024_2020)
# ds2 = gdal.Open(fp_2024_2014)
# ds1_b1 = ds1.GetRasterBand(1)
# ds2_b1 = ds2.GetRasterBand(1)
# img_array1 = ds1_b1.ReadAsArray()
# img_array2 = ds2_b1.ReadAsArray()
# img_array1 = img_array1[~np.isnan(img_array1)]
# img_array2 = img_array2[~np.isnan(img_array2)]
#
# csv = r'C:\Users\ZacharyUhlmann\Documents\staging\tolt\AQ07\gcd\gcd_stats.csv'
# fname = [fp_2024_2020, fp_2024_2014]
# array_list = [img_array1, img_array2]
# get_stats(array_list, fname, csv)
#
# arr = copy.copy(img_array1)
# t =  'Surface Change: 2020 to 2024'
# fname = "GCD_2020_to_2024"
# # STd Dev
# m = np.mean(arr)
# sd = np.std(arr)
#
#
#
# fig, axs = plt.subplots(1, 1, sharey=True, tight_layout=True)
# # axs[0].hist(img_array1, bins=100)
# axs.hist(arr, bins=100, color='c', edgecolor='k')
# axs.axvline(m, color='k', linestyle='dashed')
# axs.axvline(m+sd, color='y', linestyle='dashed')
# axs.axvline(m-sd, color='y', linestyle='dashed')
# axs.axvline(m + 2*sd, color='y', linestyle='dashed')
# axs.axvline(m- 2*sd, color='y', linestyle='dashed')
# axs.axvline(m+ 3*sd, color='y', linestyle='dashed')
# axs.axvline(m- 3* sd, color='y', linestyle='dashed')
# mx = round(max(arr),1)
# mn = round(min(arr),1)
# tv = [mn,-5,-2.5,0,2.5,5, mx]
# tl = [str(v) for v in tv]
# axs.set_xticks(tv)
# axs.set_xticklabels(tl)
# axs.set_xlabel('Change (ft)', fontsize=12)
# axs.set_ylabel('Relative Abundance', fontsize=12)
# axs.set_title(t)
# axs.set_yticks([])
#
# plt.savefig(f"C:/Users/ZacharyUhlmann/Documents/staging/tolt/AQ07/gcd/{fname}.png",dpi=300)

#
# rng = np.random.default_rng(19680801)
# N_points = 100000
# n_bins = 20
#
# # Generate two normal distributions
# dist1 = rng.standard_normal(N_points)
# dist2 = 0.4 * rng.standard_normal(N_points) + 5
#
# fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
#
# # We can set the number of bins with the *bins* keyword argument.
# axs[0].hist(dist1, bins=n_bins)
# axs[1].hist(dist2, bins=n_bins)
#
# plt.savefig(r'C:\Users\ZacharyUhlmann\Documents\staging\tolt\AQ07\gcd\test_hist.png')

#
# # Control Points Vert Error 1951 contours
# csv=r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\field_planning\study_data\bathy\1951\1951_ground_control_WA_N_Table.csv"
# df = pd.read_csv(csv)
# delta = df['2021_minus_1951']
# m = delta.mean()
# variance1 = [((x-m)**2)**0.5 for x in delta]
# variance1 = np.mean(variance1)
# delta=delta.tolist()
# fig, axs = plt.subplots(1, 1, sharey=True, tight_layout=True)
# # axs[0].hist(img_array1, bins=100)
# counts, edges, bars = axs.hist(delta, bins=5, color='c', edgecolor='k')
# axs.axvline(m, color='k', linestyle='dashed')
# # mx = round(max(arr),1)
# # mn = round(min(arr),1)
# # tv = [mn,-5,-2.5,0,2.5,5, mx]
# # tl = [str(v) for v in tv]
# # axs.set_xticklabels(tl)
# anno_str = f'mean = {round(m,2)} \nvariance = {round(variance1,2)} \n   (total count = {len(df)})'
# axs.annotate(anno_str, xy=(m, 6), xytext=(3, 6),
#             arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
#
# axs.bar_label(bars)
# axs.set_xlabel('Difference 2021 - 1951 (ft)', fontsize=12)
# axs.set_ylabel('Count', fontsize=12)
# axs.set_title('Uncertainty 1951 Contours')
# axs.set_yticks([])
#
# plt.savefig(f"C:/Box/MCMGIS/Project_Based/South_Fork_Tolt/data/field_planning/study_data/gcp_correction_1951_fmt.png",dpi=300)

# contours for formatting
def contour_range(start,stop, incr):
    l = list(range(start, stop, incr))
    l = [str(v) for v in l]
    l  = ' '.join(l)
    return(l)

ll = contour_range(1750,1762, 2)
lu = contour(range)