import numpy as np
from osgeo import gdal
import os
import pandas as pd

# Used for pend oreille box canyon initially in 2022ish
# This was for SFT FERC SWCA PAD Terrestrial July 2023

dir_analysis = r'C:\Users\UhlmannZachary\Box\MCMGIS\Project_Based\South_Fork_Tolt\gis_requests\requests_SWCA\20230713\analysis\landfire'
dir_data = r'C:\Users\UhlmannZachary\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\raster\land_classfiication'
fn = os.path.join(dir_data, r'landfire_pv_nodata.tif')
d1 = gdal.Open(fn)

# # A) Dictionary for NLCD (specifically box_canyon; 2021ish)
# udict = {11:'Open Water', 21:'Developed Open Space', 22:'Developed Low Intensity',
#        23:'Developed Medium Intensity',41:'Deciduous Forest', 42:'Evergreen Forest', \
#        43:'Mixed Forest',52:'Scrub/Shrub', 71:'Grassland Herbaceous', 31:'Barren Rock Land',\
#        90:'Woody Wetlands', 95:'Emergent Herbaceous Wetlands', 255:'null'}

# B) If csv / dictionary for data exists, use instead
csv = os.path.join(dir_data, r'landfire_clip_LF_140EVT_09152016.csv')
df_dict = pd.read_csv(csv)
udict = {v:c for v, c in zip(df_dict.VALUE, df_dict.CLASSNAME)}

arr1 = d1.ReadAsArray()
unique_key, counts = np.unique(arr1, return_counts=True)

# Try/ Except because the nodata val was 0, and there was no key.
keys_matched, counts_matched, unique_val = [],[],[]
for u,c in zip(unique_key, counts):
    try:
        unique_val.append(udict[u])
        keys_matched.append(u)
        counts_matched.append(c)
    except KeyError:
        print('WAS NOT found: {}'.format(u))
counts_normalized = [(round(c/sum(counts_matched),3)) * 100 for c in counts_matched]
df1 = pd.DataFrame(np.column_stack([keys_matched, unique_val, counts_matched, counts_normalized]),
                   columns = ['VALUE','CLASSNAME','counts','percentage'])

df1.to_csv(os.path.join(dir_analysis, 'landfire_counts.csv'))


#print(np.asarray((unique, counts)).T)