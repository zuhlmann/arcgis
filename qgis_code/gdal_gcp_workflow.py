# -*- coding: utf-8 -*-
"""
Created on Tue May 19 15:24:27 2026

@author: ZacharyUhlmann
"""

# 20260520

# Converting Max's satellite imagery (panchromatic) from Tolt to tile package
# Data was from Max rubbersheeted orig imagery.  Data was .tif, .tfw, .xml with GCD coords
# Step 1 Formated GCD from xml into csv (csv below)
# Step 2 gdal_translate to assign projection and utilize .tfw into output
# Step 3 convert source GCD point coords to pixel values (row, col) PYTHON BELOW.
#    b) Note that step 2 was relevant to format a tif
# Step 4 gdal-translate with -gcp
#  Note that somewhere the projection assignemnt is lost.
# step 5 gdalwarp with -s_srs -dstnodata -r near -order 1

import numpy as np
import rasterio
csv = r"E:\tolt\2026\GCP_raw.csv"
df=pd.read_csv(csv)
gcp_str = []
xs = np.array(df.e_src)
ys = np.array(df.n_src)

with rasterio.open(r"E:\tolt\2026\Panchromatic_26APR0422111_Formatted_Step1.tif") as src:
    rows, cols = rasterio.transform.rowcol(src.transform, xs, ys)

for i, idx in enumerate(df.index):
    e_tgt, n_tgt = df.loc[idx, 'e_tgt'], df.loc[idx, 'n_tgt']
    gcp_str.append(f"-gcp {cols[i]} {rows[i]} {e_tgt} {n_tgt}")
edit_str = ' '.join(gcp_str)
gdal_str = f"gdal_translate {edit_str} E:/tolt/2026\Panchromatic_26APR0422111_Formatted_Step1.tif E:/tolt/2026\Panchromatic_26APR0422111_Formatted_Step2.tif"
with open(r'E:\tolt\2026\gdal_format_str2.txt', 'w') as txt:
          txt.write(gdal_str)