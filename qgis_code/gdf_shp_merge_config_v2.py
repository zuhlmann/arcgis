import geopandas as gpd
import pandas as pd
import numpy as np
import fiona
import os
import sys
sys.path.append('c:/users/uhlmann/code/qgis_code')
import pygis_utils
import importlib
importlib.reload(sys.modules['pygis_utils'])

# ZU Jan 2023.  Joining geopandas dataframes and outputting csv
# NOTE!  This is cut and pasted from qgis python scripting window.  Easier to edit config there and pygis_utils in pycharm ZU (jan 2023)
#
# load basics
base_dir = r'D:\box_offline\temp\gpd_practice_20230118'
csv = r'C:\Users\UhlmannZachary\Box\GIS\Project_Based\Klamath_River_Renewal_MJA\GIS_Data\data_inventory_and_tracking\working_datasets\parcels\parcels_field_mapping_add_labels.csv'
df_config = pd.read_csv(csv)

ex = [6467308.0, 2595000.0, 6491072.0, 2608924.0]

# B)
gdb_master = r'D:\box_offline\temp\gpd_practice_20230118\master.gdb'
gdb_parcels = r'D:\box_offline\temp\gpd_practice_20230118\klamath_d_drive2.gdb'

#
feats_parcel = fiona.listlayers(gdb_parcels)
lyr_joined = [l for l in feats_parcel if 'gdf_joined_subset_20230131_v2' in l][0]
lyr_labels = [l for l in feats_parcel if 'parcels_master_joined_siskiyou_dissolve' in l][0]
idx_sisk = 'APN'

# 1) Load gdf

# 1a) while troubleshooting, load once and comment out  ...orig
gdf_tgt_orig = gpd.read_file(gdb_parcels, layer = lyr_joined)
gdf_src_orig = gpd.read_file(gdb_parcels, layer = lyr_labels)
#gdf_tgt = gdf_tgt_orig.cx[ex[0]:ex[2],ex[1]:ex[3]]
#gdf_src_ex = gdf_src_orig.cx[ex[0]:ex[2],ex[1]:ex[3]]
#gdf_src = gdf_src_ex[[r'apn',r'label',r'symbol']]

# 1b) otherwise
gdf_tgt = gpd.read_file(gdb_parcels, layer = lyr_joined)
gdf_src = gpd.read_file(gdb_parcels, layer = lyr_labels)

# 2_ proceed
gdf_src = gdf_tgt_orig
gdf_src = gdf_src.rename(columns = {'apn':'APN'})
gdf_src[idx_sisk] = gdf_src[idx_sisk].astype(str)
gdf_tgt[idx_sisk] = gdf_tgt[idx_sisk].astype(str)
gdf_src = gdf_src.set_index(idx_sisk)
gdf_tgt = gdf_tgt.set_index(idx_sisk)

vals = ['BLM', 'GDC', 'Klamath County', 'Klamath NF', 'Parcel A', 'Parcel B', 'State of CA']
gdf_src = gdf_src[gdf_src.index!='Una-ssi-gne-d']
gdf_src = gdf_src[gdf_src['label'].isin(vals)]

gdf_tgt, gdf_src, schema_updated = pygis_utils.gdf_field_mapping(gdf_tgt,gdf_src,'MultiPolygon',csv)
gdf_joined = gdf_tgt.merge(gdf_src,  how='left', left_index = True , right_index=True)
gdf_joined = gdf_joined.reset_index(level=0)

# drop shape cols
cols_drop = [c for c in gdf_joined.columns if 'shape' in c.lower()]
cols_drop2 = df_config[df_config.delete].field.to_list()
cols_drop += cols_drop2
gdf_joined = gdf_joined.drop(columns = cols_drop)

crs = r'epsg:6416'
dtf = ['CurrentDoc','LASTUPDATE']
feat_out = r'gdf_joined_subset_20230131_v2c'
##shp_out = os.path.join(base_dir, '{}.shp'.format(feat_out))
## if using shapefile, set feat_out = [shp_out]
feat_out = [gdb_parcels, feat_out]
gdf_joined = gdf_joined.set_crs(crs)
pygis_utils.to_esri_format(gdf_joined, schema_updated, feat_out, date_fields = dtf)

