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

# load basics
base_dir = r'D:\box_offline\temp\gpd_practice_20230118'
csv = r'C:\Users\UhlmannZachary\Box\GIS\Project_Based\Klamath_River_Renewal_MJA\GIS_Data\data_inventory_and_tracking\working_datasets\parcels\parcels_field_mapping.csv'

ex = [6467308.0, 2595000.0, 6491072.0, 2608924.0]

# B)
gdb_master = r'D:\box_offline\temp\gpd_practice_20230118\master.gdb'
gdb_parcels = r'D:\box_offline\temp\gpd_practice_20230118\klamath_d_drive2.gdb'
#
feats_master = fiona.listlayers(gdb_master)
lyr_master_rect = [l for l in feats_master if 'Parcels_2019_Master_Rectified' in l][0]
feats_parcel = fiona.listlayers(gdb_parcels)
lyr_siskiyou = [l for l in feats_parcel if 'matched_v2' in l][0]
idx_sisk = 'APN'
idx_master = 'apn'

# 1) Load gdf
gdf_tgt = gpd.read_file(gdb_master, layer = lyr_master_rect)
gdf_src = gpd.read_file(gdb_parcels, layer = lyr_siskiyou)

#gdf_tgt = gdf_tgt.cx[ex[0]:ex[2],ex[1]:ex[3]]
#gdf_src = gdf_src.cx[ex[0]:ex[2],ex[1]:ex[3]]

gdf_tgt = gdf_tgt.rename(columns = {idx_master:idx_sisk})
gdf_src[idx_sisk] = gdf_src[idx_sisk].astype(str)
gdf_tgt[idx_sisk] = gdf_tgt[idx_sisk].astype(str)
gdf_src = gdf_src.set_index(idx_sisk)
gdf_tgt = gdf_tgt.set_index(idx_sisk)

# 2) Manaully add objectids
gdf_tgt = pygis_utils.add_objids(gdf_tgt, 'OBJID_tgt', sequence_prepend = 'master')
gdf_src = pygis_utils.add_objids(gdf_src, 'OBJID_src', sequence_prepend = 'sisk')

# 2a) city, state zip and other manual Klamath stuff
# Assemble csz field to match non-sisk counties in master_parcels
# ONLY NECESSARY for Klamath
csz = []
for c, st, zp in zip(gdf_src['PSTLCITY'], gdf_src['PSTLSTATE'],gdf_src['PSTLZIP5']):
    if not any(l in c.lower() for l in list('abcdefghijklmnopqrstuvwxyz')):
        csz.append(np.nan)
    else:
        csz.append('{}, {} {}'.format(c,st,zp))

gdf_src['PSTLCSZ'] = csz
# In Care Of or Attention.  Master Dset copied and added more to this field in OR
gdf_src['PSTLADDRS1'] = gdf_src['InCareOf']

###  3)Assimilate schemas and add schema_type from both dsets(str:10, etc. to df_config and csv)
### Once complete, comment out
##c = fiona.open(gdb_parcels, layer=lyr_siskiyou)
##schema1 = c.schema
##c2 = fiona.open(gdb_master, layer=lyr_master_rect)
##schema2 = c2.schema
#
### 3a) schema df to join with field df for schema creation and dtype fidelity
### Used to add schema type to df_config.  One-ish time thing.  i.e. str:100 | Int, etc.
### create df and format
##df_schema1 = pygis_utils.schema_to_df(schema1, 'properties')
##df_schema1['dset']='source'
##df_schema2 = pygis_utils.schema_to_df(schema2, 'properties')
##df_schema2['dset']='target'
##
### combine schemas and merge to df_confit
##df_schemas = df_schema2.append(df_schema1)
##df_schemas = df_schemas.rename(columns = {'schema_key':'field'})
##df_schemas = df_schemas.set_index(['dset','field'])
##df_config = pd.read_csv(csv)
##df_config = df_config.set_index(['dset','field'])
##df_config_merged = df_config.merge(df_schemas, on=['dset','field'], how='inner')
##
### Append new synthetic OBJID fields to config table
### note could not get on=left or anything to merge columns with join??
### manually fix in excel
##c1, c2, c3 = ['source','target'],['OBJID_src','OBJID_tgt'],['str:100']*2
##df_append_config = pd.DataFrame(np.column_stack([c1,c2,c3]), columns = ['dset','field','schema_val'])
##df_config_merged = pd.concat([df_config_merged, df_append_config.set_index(['dset','field'])])
###df_config_merged.to_csv(csv)

crs = r'epsg:6416'
dtf = ['CurrentDoc','LASTUPDATE']
feat_out = r'gdf_joined_20230206'
#shp_out = os.path.join(base_dir, '{}.shp'.format(feat_out))
# if using shapefile, set feat_out = [shp_out]
feat_out = [gdb_parcels, feat_out]
gdf_joined, schema_updated = pygis_utils.gdf_shp_merge(gdf_tgt, gdf_src, feat_out, csv, 'MultiPolygon', crs, date_fields = dtf)