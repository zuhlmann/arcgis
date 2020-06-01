import os
import pandas as pd
from tabulate import tabulate
from compare_data import *

def show_table():
    paths_table = """C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers/path_list.csv"""
    # use index_col = 0 for show_table.  So .iloc values will accompany table
    df = pd.read_csv(paths_table, index_col = 0)
    df.index.name = 'index'
    # somehow need to be accessed this way
    df2 = df[['alias', 'desc']]
    table = tabulate(df2, headers = 'keys', colalign = ["left",  "left"], tablefmt = "github")
    # display table with options for filepaths
    print('')
    print(table)
def get_path(idx):
    '''
    args:
    idx         integer for iloc or string of alias
    '''
    paths_table = """C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers/path_list.csv"""
    df = pd.read_csv(paths_table, index_col = 1)
    # if passing index with iloc
    if isinstance(idx, int):
        path_out = df.iloc[idx]['path']
    # if passing string of alias
    else:
        path_out = df.loc[idx]['path']
    return(path_out)
    pd.DataFrame.to_csv(df, paths_table)
def add_table_entry(alias, desc, fp):
    paths_table = """C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers/path_list.csv"""
    df = pd.read_csv(paths_table, index_col = 0)
    if isinstance(df, pd.DataFrame):
        pass
    else:
        df = pd.read_csv(df, index_col = 0)
    cols = df.columns.tolist()
    row_list = [alias, desc, fp]
    new_row = {c: row_list[idx] for idx, c in enumerate(cols)}
    new_row = pd.Series(new_row)
    df_concat = pd.concat([df, pd.DataFrame(new_row).T])
    # reindex hack
    df_concat.index = range(len(df_concat))
    pd.DataFrame.to_csv(df_concat, paths_table)
def remove_table_entry(alias):
    paths_table = """C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers/path_list.csv"""
    df = pd.read_csv(paths_table, index_col = 1)
    # get index of row
    row_idx = df.index[getattr(df, 'alias') == alias]
    # remove the row
    df.drop(row_idx, inplace = True)
    # reindex
    df.index = range(len(df))
    pd.DataFrame.to_csv(df, paths_table)
def replace_table_entry(alias_or_path, original, replacement):
    '''
    replace alias or path with a new value
    Useful if alias is off or path has been changed.
    ZRU 5/29/2020
    ARGS
    alias_or_path       string. acceptable values 'alias' or 'path'
    original            original value for alias
    replacement         value to replace with
    '''
    paths_table = """C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers/path_list.csv"""
    df = pd.read_csv(paths_table, index_col = 0)
    row_idx = df.index[getattr(df, 'alias') == original]
    if alias_or_path.lower() == 'alias':
        df.loc[row_idx, 'alias'] = replacement
    elif alias_or_path.lower() == 'path':
        df.loc[row_idx, 'path'] = replacement
    pd.DataFrame.to_csv(df, paths_table)
def attribute_inventory(fp_feat, fp_out, exclude, attr_list):
    '''
    adapted and updated from compare_data.py unique_values
    ZRU 5/26/20 need to update utils

    ARGS
    fp_feat           path/to/feature
    fp_out            base/path/to/save
    exclude           boolean if True then list of fields will be excluded.
                      otherwise the list will be considered fields desired
    attr_list         list. common fields like shape_Length
    '''
    import arcpy
    import pandas as pd


    # exclude fields
    if exclude:
        # get attribute fields
        fields = [str(f.name) for f in arcpy.ListFields(fp_feat)]
        fields = list(set(fields) - set(attr_list))
    # use fields provided
    else:
        fields = attr_list
    feat_name = fp_feat.split('\\')[-1]
    for field in fields:
        print(field)
        with arcpy.da.SearchCursor(fp_feat, [field]) as cursor:
            # This row[0] will access teh object to grab the field.  If n fields > 1, n idx >1
            vals = [row[0] for row in cursor]
            df = pd.DataFrame(vals, columns = ['value'])
            series_sort = df.groupby('value').size()
            df = pd.DataFrame(series_sort.sort_values())
            pd.DataFrame.to_csv(df, os.path.join(fp_out, '{}_{}.csv'.format(feat_name, field)))

def list_unique_fields(fp_feat, field):
    '''
    ZRU 6/1/20
    '''
    import arcpy
    import pandas as pd

    # exclude fields
    feat_name = fp_feat.split('\\')[-1]
    with arcpy.da.SearchCursor(fp_feat, [field]) as cursor:
        # This row[0] will access teh object to grab the field.  If n fields > 1, n idx >1
        vals = [row[0] for row in cursor]
        df = pd.DataFrame(vals, columns = ['value'])
        series_sort = df.groupby('value').size()
        df = pd.DataFrame(series_sort.sort_values())
    return(df)

def where_clause_create(fp_list, field_list, val_list):
    where_clause=[]
    for fp, field, val in zip(fp_list, field_list, val_list):
        field_delim = arcpy.AddFieldDelimiters(fp, field)
        # check here and here to find code and learn unicode background:
        # https://gis.stackexchange.com/questions/153444/using-select-layer-by-attribute-in-arcpy
        # https://pro.arcgis.com/en/pro-app/help/data/geodatabases/overview/a-quick-tour-of-unicode.htm
        where_clause.append("{field} = '{val}'".format(field=field_delim, val=val))
    return where_clause

def parse_dir(obj, substr):
    '''
    matchses substrings to dir(obj) from python interactive
    document and add to: ZRU 5/26/2020
    '''
    methods = dir(obj)
    indices_match = [idx for idx, method in enumerate(methods) if substr in method]
    methods_match = [methods[idx] for idx in indices_match]
    return(indices_match, methods_match)
