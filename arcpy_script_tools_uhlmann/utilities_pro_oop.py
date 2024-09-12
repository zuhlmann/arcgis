import pandas as pd
import os
import ntpath
import arcpy

def format_lyR_inv_datasource_moved(csv_remap, csv_inv):
    '''
    Essentially uses dictionary from csv_remap to replace base paths with new
    base paths in dataframe csv_layer_inv.  i.e. bad/path/to/shapefile would
    become good/path/to/shapefile wherein {bad:good} in csv_remap row.
    20240904
    Args:
        csv_remap:          essentially a dictionary as a csv wherein the field
                            root_subdir will demarcate split location in file path
                            for replaceing base file path
        csv_layer_inv:      layer inventory with path/to/<layer or file>

    Returns:
        csv_inv             saves csv_in with new field and upated paths
    '''
    df_key = pd.read_csv(csv_remap, index_col='path_source')
    df_lyr_inv = pd.read_csv(csv_inv)
    df_lyr_inv['source_new']=pd.Series(dtype='string')
    for idx_src in df_lyr_inv.index:
        for idx_key in df_key.index:
            if os.path.normpath(idx_key) in df_lyr_inv.loc[idx_src, 'source']:
                base = df_key.loc[idx_key, 'path_target']
                root_subdir = df_key.loc[idx_key, 'root_subdir']
                top = os.path.normpath(df_lyr_inv.loc[idx_src,'source'].split(root_subdir)[-1])[1:]
                updated_source = os.path.join(base, top)
                df_lyr_inv.at[idx_src,'source_new']=updated_source

    # Add column for connection_database (pro object) i.e. gdb or shapefile dir
    # 20240903
    dbase_connection = []
    for idx in df_lyr_inv.index:
        if df_lyr_inv.loc[idx, 'develop']:
            fp_src = df_lyr_inv.loc[idx, 'source_new']
            if os.path.splitext(fp_src)[-1] == '.shp':
                t = os.path.split(fp_src)[0]
            else:
                t = '{}.gdb'.format(fp_src.split('.gdb')[0])
            dbase_connection.append(t)
        else:
            dbase_connection.append('NONE')
    df_lyr_inv['dbase_connection'] = dbase_connection
    df_lyr_inv.to_csv(csv_inv)

def format_lyR_inv_datasource_standard(csv_inv, df_gdb, match_col, replace_col):
    df_lyr_inv = pd.read_csv(csv_inv)
    fp_lyr = df_gdb.loc[idx, match_col]
    fp_lyR_new = df_gdb.loc[idx, replace_col]
    # Use orig (path/to/fc i.e. DATA_LOCATION_MCMILLEN
    for orig, new in zip(fp_lyr,fp_lyR_new):
        if new[-4:]=='.shp':
            dbase_connection, fname = os.path.splitext(orig)
            df_lyr_inv.at[orig, 'workspace_factory'] = 'Shape File'
        else:
            dbase_connection = '{}.gdb'.format(fp_lyR_new.split('.gdb')[0])
            fname = os.path.split(fp_lyR_new)[-1]
            df_lyr_inv.at[orig, 'workspace_factory'] = 'File Geodatabase'
        df_lyr_inv.at[orig, 'dataset'] = fname
        df_lyr_inv.at[orig, 'dbase_connection'] = shp_dir
    df_lyr_inv.to_csv(csv_inv)




def aggregate_layers(csv_in, csv_out, group_by_field, agg_field):
    '''
    Groupby a field (group_by_field), aggregate all unique values in another field (agg_field)
    as a new field with values being unique values as string with commas separating values.
    20240904
    Args:
        csv_in:             path/to/csv source
        csv_out:            path/to/csv_out; can be same as csv_in
        group_by_field:     field to groupby
        agg_field:          field to create unique value comma-separated string

    Returns:

    '''
    df = pd.read_csv(csv_in)

    def join_list(v):
      vn = v.to_list()
      vn = list(set(vn))
      vn = ', '.join(vn)
      return (vn)

    groupby_source = df.groupby(group_by_field).agg({agg_field: join_list})
    groupby_source = groupby_source.reset_index()

    fnames = [os.path.splitext(ntpath.basename(fp))[0] for fp in groupby_source.source]
    groupby_source['ITEM'] = fnames
    groupby_source = groupby_source.set_index('ITEM')
    groupby_source.to_csv(csv_out)

def unique_comma_sep_string(csv_in, string_field):
    '''
    After creating lyR inventory, return all unique map names as a list.
    For instance, the map_names column contains values from the aggregate_layers
    function which yields a single string with commas separating map_names.
    i.e. a dataframe with two rows:
    row1 = "map1, map2, extent_map, tolt_land_use".
    row2 = "map1,map3,extent_map"
    would yield a list containing the 5 unique map_names from both rows (all rows).
    i.e. [map1,map2,map3, extent_map, tolt_land_use]
    20240904
    Args:
        csv_in:             lyR inventory
        string_field:       field with strings of comma separated names i.e. map names
                            i.e. "map1, map7, map_georgia,map7"

    Returns:
        unique_{}_{}        list of unique split strings from aggregated list.

    '''
    df = pd.read_csv(csv_in)
    l = ', '.join(df[string_field])
    l = l.split(',')
    l = [i.strip() for i in l]
    l = list(set(l))
    return(l)

def project_lyT_inv(prodoc, **kwargs):
    '''
    Same as ArcPro toolbox tool.
    20240904
    Args:
        self:           self
        prodoc:         path/to/prodoc.aprx
        **kwargs:       csv = path/to/csv

    Returns:

    '''
    aprx = arcpy.mp.ArcGISProject(prodoc)
    lyt_list = aprx.listLayouts()
    lyt_name = []
    el_map_formatted = []
    for lyt in lyt_list:
        el = lyt.listElements()
        try:
            el_map = [e.map.name for e in el if e.type == 'MAPFRAME_ELEMENT']
            el_map_formatted = el_map_formatted + el_map
            lyt_name = lyt_name + ([lyt.name] * len(el_map))
        except RuntimeError:
            # This means that there is a map element with a map linked that no longer exists
            el_map_formatted = el_map_formatted + ['RUNTIME ERROR - most likely map element linked does not exist']
            lyt_name = lyt_name + [lyt.name]
    df = pd.DataFrame(np.column_stack([lyt_name, el_map_formatted]), columns=['LAYOUT', 'SOURCE_MAP'])
    try:
        csv = kwargs['csv']
        df.to_csv(csv)
    except KeyError:
        return(df)

