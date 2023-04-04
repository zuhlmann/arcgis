import numpy as np
from osgeo import gdal
import pandas as pd

clip_dir = r'D:\box_offline\small_projects\eklutna_d\lidar_geomorph\GIS Files for Geomorphology\clipped_stats'
fn = [fn for fn in os.listdir(clip_dir) if 'tif' == fn[-3:]]
fn = [f for f in fn if r'22_20' in f]

symb = []
for fp_in in fn:
    fp_in = os.path.join(clip_dir, fp_in)
    ds1 = gdal.Open(fp_in)
    arr_orig = ds1.ReadAsArray()
    # NOTE!! this will destroy values less than -9998.  Will work on -3.28 e ... and -9999.  Terrible Hack
    arr_orig[arr_orig<-9998] = np.nan
    std_dev = np.nanstd(arr_orig)
    mn = np.nanmean(arr_orig)
    mn = 0
    mx = np.nanmax(arr_orig)
    minm = np.nanmin(arr_orig)
    upper = [mn + std_dev * (n+1) for n in range(3)]
    lower = [mn - std_dev * (n+1) for n in range(3)]
    vals = [minm] + lower + [mn] + upper + [mx]
    vals.sort()
    vals = [round(v,2) for v in vals]
    symb.append(vals)
df = pd.DataFrame(symb)
ser = pd.Series(fn, name = 'fname')
df = df.join(ser)
df = df.set_index('fname')
df.to_csv(os.path.join(clip_dir, r'symbology_bounds_22_20_mean0.csv'))

