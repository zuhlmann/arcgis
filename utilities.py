import os
import pandas as pd
from tabulate import tabulate
from compare_data import *

def show_table():
    paths_table = """C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers/path_list.csv"""
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

def add_table_entry(df, alias, desc, fp):
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
    return(df_concat)

def unique_values(fp_feat, fp_out, exclude_fields):
    import arcpy
    import pandas as pd
    with arcpy.da.SearchCursor(fp_feat, ['OBJECTID']) as cursor:
        print(sorted({row[0] for row in cursor}))

    # get attribute fields
    fields = [str(f.name) for f in arcpy.ListFields(fp_feat)]
    fields = list(set(fields) - set(exclude_fields))
    df = pd.DataFrame({'fp_feat':['feat1']})
    for field in fields:
        with arcpy.da.SearchCursor(fp_feat, [field]) as cursor:
            # note sorted({set}) = type list
            list_sorted = sorted({row[0] for row in cursor})
            df[field] = unpack_list(list_sorted, False)
    pd.DataFrame.to_csv(df, fp_out)
