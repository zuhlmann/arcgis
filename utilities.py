import os
import pandas as pd
from tabulate import tabulate


def show_table():
    paths_table = """C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers/path_list.csv"""
    df = pd.read_csv(paths_table, index_col = 0)
    df.index.name = 'alias'
    # somehow need to be accessed this way
    df2 = df[['desc']]
    table = tabulate(df2, headers = 'keys', colalign = ["left",  "right"], tablefmt = "github")
    # display table with options for filepaths
    print(table)
def get_path(iloc):
    paths_table = """C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers/path_list.csv"""
    df = pd.read_csv(paths_table, index_col = 0)
    path_out = df.iloc[iloc]['path']
    return(path_out)
