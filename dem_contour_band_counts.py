import os
# import utilities
import pandas as pd
import numpy as np
import gdal


# 2022 March 31 - Acreage at elevation bands for Swancove
# gdal array reading capability pulled from geotiff_summary_stats

# Path/to/DEM
fp_tiff = r'D:\box_offline\swancove_2022\backbarrier_20220314\rasters\SC_BathwithSurv.tif'
ds1 = gdal.Open(fp_tiff)
arr = ds1.ReadAsArray()
# Save series to csv
csv_out = r'D:\box_offline\swancove_2022\backbarrier_20220314\swan_pool_exist_acreage.csv'

# HARDCODED - could be adapted to take path to csv with vals in rows, etc.
bands =[-1.16, -0.85, 1.0, 1.26, 1.35, 1.89, 3.63]
d = {}
for i in range(len(bands) -1):
    # in this case the bands are from band[i] to band [i+1]
    bound1 = bands[i]
    print(type(bound1))
    bound2 = bands[i+1]
    print(bound2)
    mask = (arr >= bound1) & (arr < bound2)
    ct = np.sum(mask)
    str(bound1)
    bound1 = str(bound1)
    bound2 = str(bound2)
    b1_str = bound1.replace('.','').replace('-','neg_')
    b2_str = bound2.replace('.','').replace('-','neg_')
    name = '{}_to_{}'.format(b1_str, b2_str)
    d.update({name:ct})
ser = pd.Series(d)
ser.to_csv(csv_out)
