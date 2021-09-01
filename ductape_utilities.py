# New Utilities for agol_obj or related utilites
# utilities.py is more of arcpy specific stuff
import os
import numpy as np
import pandas as pd
import copy

def parse_csl(csl_string, is_list = False):
      '''
      Reverse-abstracted from spyder_arcgis_oop to use in ductape_utilities.Takes
      strings and outputs csls
      ZU 20210826
      ARGS
      csl_string:           list of or single string to cast into list
      is_list               janky approach. Boolean.  this indicates that you are passing a
                            list of strings, presumable from df.loc[ITEM, 'TAGS']
      '''
      if is_list:
          parsed_csl = []
          for items in csl_string:
              try:
                  # split by ',' and remove spaces from items in parsed_list
                  parsed_csl.append([item.strip(' ') for item in items.split(',')])
              except AttributeError:
                  # nans from pd.read_csv(...) are saved as floats which have
                  parsed_csl.append([items])
      else:
          parsed_csl = [item.strip(' ') for item in csl_string.split(',')]
      return(parsed_csl)

def unique_vals_df(list_in):
    '''
    Returns dataframe with unique values and count for each unique value.  Input
    is a list with duplicate elements (hopefully)
    ARGS
    list_in:            list, ideally (or function makes no sense) with duplicates
    '''
    # List of unique elements
    unique_elements = list(set(list_in))
    # count per unique element
    unique_el_count = [list_in.count(el) for el in unique_elements]
    df = pd.DataFrame(np.column_stack([unique_elements, unique_el_count]),
                        columns = ['NAME', 'COUNT'], index = unique_elements)
    return(df)

def csv_to_dict(fp_transfer_csv, fp_dict_csv, target_col):
    '''
    A wierd shitty Monday concoction used in a workflow to update tags in spreadsheet
    that will be updated on AGOL.
    ARGS
    fp_transfer_csv            the inventory to key out with dictionary and replace
                                tags
    fp_dict_csv                csv with key, val, action cols
    target_col                  col with tags to key
    '''
    df_dict = pd.read_csv(fp_dict_csv)
    # Key = NAME from unique_vals_df
    # Val = VAL from unique_vals_df
    key_list = df_dict.KEY.to_list()
    val_list = df_dict.VAL.to_list()
    remove_list = df_dict.KEY[df_dict.ACTION == 'remove'].to_list()
    print(remove_list)
    dict1 = {}
    for key, val in zip(key_list, val_list):
        if pd.isnull(val):
            val = copy.copy(key)
        dict1.update({key:val})
    df_transfer = pd.read_csv(fp_transfer_csv)
    df_temp = df_transfer[df_transfer.AGOL_STATUS]
    for i, row in df_temp.iterrows():
        target_row = getattr(row, target_col)
        tags_list = target_row.split(',')
        tags_list = [item.strip(' ') for item in tags_list]
        trans_tags = []
        for tag in tags_list:
            if tag not in remove_list:
                try:
                    trans_tags.append(dict1[tag])
                except KeyError:
                    trans_tags.append(tag)
        trans_tags = list(set(trans_tags))
        trans_tags_str = ', '.join(trans_tags)
        df_transfer.at[i, 'UPDATED_TAGS2']=trans_tags_str
    return(df_transfer)
