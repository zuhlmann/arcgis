import geopandas as gpd
import fiona
import pandas as pd
import numpy as np
from collections import OrderedDict
from datetime import date

def schema_to_df(schema, prop_key):
    # take a fiona schema object and convert to df
    # 20230127
    k = list(schema[prop_key].keys())
    v = list(schema[prop_key].values())
    df = pd.DataFrame(np.column_stack([k,v]), columns = ['schema_key','schema_val'])
    return(df)
def add_objids(gdf, col_name, **kwargs):
    try:
        prep = kwargs['sequence_prepend']
        gdf[col_name] = ['{}{}'.format(prep, n) for n in list(range(len(gdf)))]
    except KeyError:
        gdf[col_name] = list(range(len(gdf)))
    return(gdf)

def canvas_extents(map_canvas_extents):
    # # get current canvas extents.  ZU 202301
    # Format and round extents
    ex = map_canvas_extents.toString()
    ex = ex.replace(':',',').replace(' ,',',')
    ex = ex.split(',')
    ex = [round(float(e),0) for e in ex]
    return(ex)

def datetime_flds(gdf, date_fields, schema, dt):
    '''
    Format date fields loaded from gpd.read_file().  Must format as datetime.date class to work in ESRI
    ZU 20230131
    Args:
        gdf:            geodateframe to update
        date_fields:    datetime fields to format
        schema:         schema (dict) to update
        dt:             data type = str or date currently (zu 20230131)

    Returns:
        gdf:            updated gdf
        schema:         updated schema

    '''

    # Below try/except if None record - i.e. Null
    # dt string and date due to OpenDataBase (GDAL driver for ESRI gdb??) unable to take datetime.date object
    for fld in date_fields:
        vals = gdf[fld]
        vals_updated = []
        if dt == 'str':
            for v in vals:
                try:
                    vf = v[:10]
                    vals_updated.append(vf)
                except TypeError:
                    vals_updated.append(None)
            schema['properties'][fld]='str:50'
        elif dt == 'date':
            for v in vals:
                try:
                    vf = date.fromisoformat(v[:10])
                    vals_updated.append(vf)
                except TypeError:
                    vals_updated.append(None)
            schema['properties'][fld] = 'date'

        gdf[fld] = vals_updated

    return(gdf, schema)

def gdf_field_mapping(gdf_tgt,gdf_src, geom_type, csv):
    '''

    Args:
        gdf_tgt:            target gdf for join
        gdf_src:            source gdf for join
        csv:                config csv for field mapping

    Returns:
        schema_updatged:      hopefully schema to save out with gdf.to_file()
    '''

    df_config = pd.read_csv(csv)
    # Rename columns before joining
    df_config_tgt = df_config[df_config['dset'] == r'target']
    dict_tgt = dict(zip(df_config_tgt['field'], df_config_tgt['field_new']))
    gdf_tgt = gdf_tgt.rename(columns=dict_tgt)
    df_config_src = df_config[df_config['dset'] == 'source']
    dict_src = dict(zip(df_config_src['field'], df_config_src['field_new']))
    gdf_src = gdf_src.rename(columns=dict_src)

    # If schema vals for target source preferred, then keep = last
    # df_config_unique = df_config.drop_duplicates(subset = ['field_new'], keep='first')
    df_config_ordered = df_config[~pd.isna(df_config['order'])]
    df_config_ordered = df_config_ordered.sort_values('order')
    df_config_ordered = df_config_ordered.set_index('field_new')

    # keys = gdf_joined.columns
    schema_prop_dict = {k: df_config_ordered.loc[k, 'schema_val'] for k in df_config_ordered.index if k != 'geometry'}
    schema_updated = {'properties': OrderedDict(schema_prop_dict), 'geometry': geom_type}
    return(gdf_tgt, gdf_src, schema_updated)


def to_esri_format(gdf_in, schema, feat_out, **kwargs):
    '''

    Args:
        gdf_in:     Geodataframe ready for formatting and export
        schema:     formatted scheme
        feat_out:   list:  [path/to/shp] or [path/to/gdb, feat_name]

    Returns:

    '''

    # OpenFileGDB driver from GDAL unable to handle datetime.date formats
    # If shapefile, datetime.date are valid
    if len(feat_out) == 1:
        # Format datetime fields: shapefiles can handle datetime.date class; gdb cannot
        try:
            gdf_out, schema_out = datetime_flds(gdf_in, kwargs['date_fields'], schema, 'date')
        except KeyError:
            pass
        gdf_out.to_file(feat_out[0], schema=schema_updated)
    else:
        # Format datetime fields: # Format datetime fields: shapefiles can handle datetime.date class; gdb cannot
        try:
            gdf_out, schema_out = datetime_flds(gdf_in, kwargs['date_fields'], schema, r'str')
        except KeyError:
            pass
        gdf_out.to_file(feat_out[0], layer=feat_out[1], driver='OpenFileGDB', schema=schema)
    # return (gdf_out, schema_updated)

def assemble_pstl(gdf, key):
    '''

    Args:
        gdf:        gdf to format
        key:        column name/key to add new pstl address

    Returns:
        gdf:        formatted gdf
    '''
    full_pstl_list = []
    for a1, a2, csz in zip(gdf['PSTLADDRS1'], gdf['PSTLADDRES'], gdf['PSTLCSZ']):
        try:
            if r'' in [a2.strip(), csz.strip()]:
                full_pstl_list.append(np.nan)
            elif a1.strip() == '':
                full_pstl_list.append(r'{}, {}'.format(a2, csz))
            else:
                full_pstl_list.append(r'{}, {}, {}'.format(a1, a2, csz))

        except AttributeError:
            if None in [a2, csz]:
                full_pstl_list.append(np.nan)
            elif a1 == None:
                full_pstl_list.append(r'{}, {}'.format(a2, csz))
            else:
                full_pstl_list.append(r'{}, {}, {}'.format(a1, a2, csz))

    gdf[key] = full_pstl_list
    return(gdf)

def gdf_shp_merge(gdf_tgt, gdf_src, feat_out, csv, geom_type, crs, **kwargs):

    df_config = pd.read_csv(csv)
    # Rename columns before joining
    df_config_tgt = df_config[df_config['dset']==r'target']
    dict_tgt = dict(zip(df_config_tgt['field'], df_config_tgt['field_new']))
    gdf_tgt = gdf_tgt.rename(columns = dict_tgt)
    df_config_src = df_config[df_config['dset'] == 'source']
    dict_src = dict(zip(df_config_src['field'], df_config_src['field_new']))
    gdf_src = gdf_src.rename(columns = dict_src)

    # Want geometry of target but values of source, hence the double combine_first
    gdf_geom = gdf_tgt[['geometry']]
    # Note that gdb_src will trump gdb_tgt if non-null values
    gdf_joined = gdf_src.combine_first(gdf_tgt)
    gdf_joined = gdf_geom.combine_first(gdf_joined)
    # Drop the duplicated geometries from essentially multi to multi squared (i.e. 2 to 1 = 2  --> 2 * 2 = 4
    gdf_joined = gdf_joined.drop_duplicates(subset = ['OBJID_src','geometry'])
    gdf_joined = gdf_joined.set_crs(crs)
    # Pop APN back into dataframe
    gdf_joined = gdf_joined.reset_index(level=0)

    # If schema vals for target source preferred, then keep = last
    # df_config_unique = df_config.drop_duplicates(subset = ['field_new'], keep='first')
    df_config_ordered = df_config[~pd.isna(df_config['order'])]
    df_config_ordered = df_config_ordered.sort_values('order')
    df_config_ordered = df_config_ordered.set_index('field_new')

    # drop shape cols
    cols_drop = [c for c in gdf_joined.columns if 'shape' in c.lower()]
    cols_drop2 = df_config[df_config.delete].field.to_list()
    cols_drop += cols_drop2
    gdf_joined = gdf_joined.drop(columns = cols_drop)

    # keys = gdf_joined.columns
    # schema_prop_dict = {k:df_config_ordered.loc[k,'schema_val'] for k in keys if k != 'geometry'}
    schema_prop_dict = {k:df_config_ordered.loc[k,'schema_val'] for k in df_config_ordered.index if k != 'geometry'}
    schema_updated = {'properties':OrderedDict(schema_prop_dict), 'geometry':geom_type}

    # OpenFileGDB driver from GDAL unable to handle datetime.date formats
    # If shapefile, datetime.date are valid
    if len(feat_out)==1:
        # Format datetime fields: shapefiles can handle datetime.date class; gdb cannot
        try:
            gdf_joined, schema_updated = datetime_flds(gdf_joined, kwargs['date_fields'], schema_updated, 'date')
        except KeyError:
            pass
        gdf_joined.to_file(feat_out[0], schema=schema_updated)
    else:
        # Format datetime fields: # Format datetime fields: shapefiles can handle datetime.date class; gdb cannot
        try:
            gdf_joined, schema_updated = datetime_flds(gdf_joined, kwargs['date_fields'], schema_updated, r'str')
        except KeyError:
            pass
        gdf_joined.to_file(feat_out[0], layer = feat_out[1], driver = 'OpenFileGDB', schema = schema_updated)
    return(gdf_joined, schema_updated)


import geopandas as gpd
import os
def gpd_overlay(config_file):
    '''
    Used this but never developed because the FERC boundary was geometrically way off.
    ZU 20240219
    Args:
        config_file:

    Returns:

    '''
    gdb1 = r'C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\map_documents\SFT_common_maps\SFT_common_maps.gdb'
    gdb2 = r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\gdb\SFT_master.gdb"
    gdf = gpd.read_file(gdb1, layer = 'land_ownership_merged_v3')
    gdf_ferc = gpd.read_file(gdb2, layer = 'p2959_project_bdry')
    seattle_subset = gdf[(gdf.owner_sft=='scl') | (gdf.owner_sft=='spu')]
    union_seattle = gpd.overlay(seattle_subset, gdf_ferc, how='intersection')
    union_seattle = union_seattle.dissolve('owner_sft')

    dir_out = r'C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\gis_requests\requests_McMillen\2024PAD_general\seattle_acreage'
    union_seattle.to_file(os.path.join(dir_out, 'seattle_acreage_ferc_bdry.shp'))


