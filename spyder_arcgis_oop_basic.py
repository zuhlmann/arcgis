# ZRU 7/13/20
# To run this we need to be in arcgispro-py3 environment w/ GIS package:
# go to C:\\Program Files\\ArcGIS\\Pro\\bin\\Python\\Scripts and do: Start proenv.bat
# python2 to python3 compatability: https://pro.arcgis.com/en/pro-app/arcpy/get-started/python-migration-for-arcgis-pro.htm
# coding: utf-8

import os, sys
import glob
import copy
import pandas as pd
import numpy as np
import utilities
import ductape_utilities
import datetime
import math
import xml.etree.ElementTree as ET
sys.path = [p for p in sys.path if '86' not in p]
import arcpy
import logging
# note this protocol from here because debug was not writing to file
# https://stackoverflow.com/questions/31169540/python-logging-not-saving-to-file
from imp import reload
reload(logging)

class metaData(object):
    '''
    ARGS
    df_index_col            ITEM is default for use with Klamath.
    '''
    def __init__(self,  prj_file, fp_maestro, fp_path_list,
                df_str = 'df', df_index_col = 'ITEM', **kwargs):
        df = pd.read_csv(fp_maestro, index_col = df_index_col, na_values = 'NA', dtype='str')
        setattr(self, df_str, df)
        # fp_maestro_archive creation.
        todays_date = datetime.datetime.today().strftime('%Y%m%d')
        self.todays_date = todays_date
        todays_date_verbose = datetime.datetime.today().strftime('%B %d %Y')
        self.todays_date_verbose = todays_date_verbose

        # save path to csv
        if df_str == 'df':
            fp_maestro_prop_str = 'fp_maestro'
        else:
            # passing a different base df
            df_base_str = df_str.replace('df_', '')
            fp_maestro_prop_str = 'fp_maestro_{}'.format(df_base_str)

        setattr(self, fp_maestro_prop_str, fp_maestro)

        # # adds fp_log, csv_archive, csv_temp, etc.
        # self.create_base_properties(df_str)

        df_paths = pd.read_csv(fp_path_list)
        idx_gdb = df_paths.columns.get_loc('path_gdb')
        idx_csv = df_paths.columns.get_loc('path_csv')
        path_gdb_dict = {}
        path_csv_dict = {}
        df_str_dict
        for i, rw in df_paths.iterrows():
            fp_gdb = rw[idx_gdb]
            fp_csv = rw[idx_csv]
            basedir, gdb_name = os.path.splitext(fp_gdb)
            gdb_str = '{}_gdb'.format(gdb_name[:-4])
            df_str = 'df_{}'.format(gdb_name[:-4])
            path_gdb_dict.update({gdb_str:fp_gdb})
            path_csv_dict.update({gdb_str:fp_csv})
            df_str_dict.update({gdb_str:df_str})

    def take_action_mcm(self, df_str, action_type,
                    target_col = 'DATA_LOCATION_MCMILLEN_JACOBS',
                    dry_run = False, replace_action = ''):

        # load dataframe
        df = getattr(self, df_str)

        if df_str == 'df':
            prop_str_fp_logfile = 'fp_log'
        else:
            df_base_str = df_str.replace('df_','')
            prop_str_fp_logfile = 'fp_log_{}'.format(df_base_str)
            prop_str_fp_csv = 'fp_csv_{}'.format(df_base_str)

        fp_logfile = getattr(self, prop_str_fp_logfile)

        logging.basicConfig(filename = fp_logfile, level = logging.DEBUG)

        # Save call string to logfile
        banner = '    {}    '.format('-'*50)
        call_str = 'take_action({}, {}, target_col = {}):\n'.format(df_str, action_type, target_col)
        fct_call_str = 'Performing function called as:\n{}'.format(call_str)
        date_str = datetime.datetime.today().strftime('%D %H:%M')
        msg_str = '\n{}\n{}\n{}\n{}\n'.format(banner, date_str, banner, fct_call_str)
        logging.info(msg_str)

        # DICTIONARY to translate previous col documenting in df
        dict_col_name_orig = {'original':'DATA_LOCATION_MCM_ORIGINAL',
                                'staging':'DATA_LOCATION_MCM_STAGING',
                                'previous':'DATA_LOCATION_MCM_PREVIOUS'}

        if action_type in ['copy']:

            for index in self.indices:
                df_item = df.loc[index]
                fp_fcs_current = os.path.normpath(df_item[target_col])
                fp_move = os.path.normpath(self.path_gdb_dict[df_item['MOVE_LOCATION']])
                dset_move = df_item['MOVE_LOCATION_DSET']
                fc_new_name = df_item['RENAME']
                notes = df_item['NOTES']


                # Get TARGET DF/CSV/STR
                fp_components_target = fp_move.split(os.sep)
                tgt_gdb_or_dir = fp_components_target[-1]
                # dir as target
                if '.gdb' not in tgt_gdb_or_dir:
                    tgt_gdb_or_dir = fp_components_target[-1]
                    tgt_gdb_or_dir_str = '{}_dir'.format(tgt_gdb_or_dir)
                # GDB as target
                else:
                    tgt_gdb_or_dir_str = '{}_gdb'.format(tgt_gdb_or_dir[:-4])
                fp_csv_target = self.path_csv_dict[tgt_gdb_or_dir_str]
                df_str_target = self.df_str_dict[tgt_gdb_or_dir_str]
                # Only grabs TargetGDB once per gdb
                try:
                    df_target = getattr(self, df_str_target)
                # if dataframe NOT already added via self.add_df
                except AttributeError:
                    print('populating target')
                    # note this also creates fp_csv_archive
                    self.add_df(fp_csv_target, df_str_target, 'ITEM')
                    df_target = getattr(self, df_str_target)
                    # save a base archive if NEVER saved and a daily archive if never saved
                    self.save_archive_csv(df_str_target)

                # Get SOURCE DF/CSV/STR
                fp_csv_source = self.path_csv_dict[src_gdb_or_dir_str]
                df_str_source = self.df_str_dict[src_gdb_or_dir_str]
                # Only grabs TargetGDB once per gdb
                try:
                    df_source = getattr(self, df_str_source)
                # if dataframe NOT already added via self.add_df
                except AttributeError:
                    print('populating source')
                    # note this also creates fp_csv_archive
                    self.add_df(fp_csv_source, df_str_source, 'ITEM')
                    df_source = getattr(self, df_str_source)
                    # save a base archive if NEVER saved and a daily archive if never saved
                    self.save_archive_csv(df_str_source)


                # for featureclasstofeatureclass
                fp_dset = os.path.join(fp_move, dset_move)
                # check to make sure output dset exists before proceeding
                if not arcpy.Exists(fp_dset):
                    arcpy.CreateFeatureDataset_management(fp_move, dset_move, self.prj_file)
                # print('fp new: \n{}'.format(fp_dset))
                # if rename specified
                if not pd.isnull(fc_new_name):
                    feat_name = copy.copy(fc_new_name)
                    # flag to change index label
                    update_label = True
                else:
                    feat_name = copy.copy(index)
                    feat_name = feat_name.replace(' ','_')
                    feat_name = feat_name.replace('&','_')
                    print('feat name to copy {}'.format(feat_name))

                    update_label = False
                # full path with featureclass name
                fp_fcs_new = os.path.join(fp_move, dset_move, feat_name)
                # print('fp fcs new: \n{}'.format(fp_fcs_new))
                # print('fp current: \n{}'.format(fp_fcs_current))
                # To document whether fp_fcs_current = Staging, Previous, Original
                col_name_original = df_item['COL_NAME_ARCHIVAL']
                col_name_original = dict_col_name_orig[col_name_original]
                try:
                    if not dry_run:
                        # Should only trigger if move not copy (i.e. move into same gdb)
                        if rename_delete_protocol:
                            print('Rename Protocol GO!!!')
                            fp_fcs_current_comp = fp_fcs_current.split(os.sep)
                            fc_current_renamed = fp_fcs_current_comp[-1] + '_1'
                            fp_fcs_renamed = os.path.sep.join(fp_fcs_current_comp[:-1] + [fc_current_renamed])
                            # arcpy_msg to debug where failed
                            arcpy_msg = 'RENAME False FC to FC False DELETE False'
                            arcpy.Rename_management(fp_fcs_current, fc_current_renamed)
                            arcpy_msg = 'RENAME: True FC to FC: False DELETE: False'
                            arcpy.FeatureClassToFeatureClass_conversion(fp_fcs_renamed, fp_dset, feat_name)
                            arcpy_msg = 'RENAME: True FC to FC: True DELETE: False'
                            arcpy.Delete_management(fp_fcs_renamed)
                        else:
                            arcpy.FeatureClassToFeatureClass_conversion(fp_fcs_current, fp_dset, feat_name)
                            arcpy_msg = 'FC to FC True DELETE False'
                            # delete if file is moved
                            if action_type == 'move':
                                print('Delete Protocol GO!!!')
                                arcpy.Delete_management(fp_fcs_current)
                                arcpy_msg = 'df_source.drop FAILED, index does not exist'
                                df_source.drop(index, inplace = True)
                                setattr(self, df_str_source, df_source)

                    df.at[index, target_col] = fp_fcs_new
                    df.at[index, col_name_original] = fp_fcs_current
                    df.at[index, 'ACTION'] = ''
                    df.at[index, 'MOVE_LOCATION'] = ''
                    df.at[index, 'MOVE_LOCATION_DSET'] = ''
                    if update_label:
                        df = df.rename(index = {index:feat_name})
                    # TARGET DF UPDATES
                    # Assemble Series to append to Master DF
                    print('did we make it here above the append')
                    d = {col_name_original: fp_fcs_current, 'FEATURE_DATASET':dset_move,
                        'DATA_LOCATION_MCMILLEN_JACOBS':fp_fcs_new,'NOTES_APPEND':notes}
                    ser_append = pd.Series(data = d,
                                 index = [col_name_original, 'FEATURE_DATASET',
                                        'DATA_LOCATION_MCMILLEN_JACOBS','NOTES_APPEND'],
                                 name = feat_name)
                    print('DID WE MAKE IT HERE')
                    # append new row from Series
                    df_target = df_target.append(ser_append)
                    if update_label:
                        df_target = df_target.rename(index = {index:feat_name})
                    print('now legs set attribute')
                    # SAVE TO TARGET_DF every Iter in case Exception
                    setattr(self, df_str_target, df_target)
                    setattr(self, df_str, df)
                    print('doth we seteth')
                    if not dry_run:
                        msg_str = '\nMOVING:  {}\nTO:      {}'.format(fp_fcs_current, fp_fcs_new)
                        print(msg_str)
                        logging.info(msg_str)

                except Exception as e:
                    if not dry_run:
                        msg_str = '\nUNABLE TO MOVE:  {}\nARCPY DEBUG: {}'.format(fp_fcs_current, arcpy_msg)
                        logging.info(msg_str)
                        logging.info(e)
