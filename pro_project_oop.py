import os, sys
import copy
import pandas as pd
import numpy as np
from imp import reload
sys.path = [p for p in sys.path if '86' not in p]
import arcpy



class commonUtils(object):
    def __init__(self):
        pass
    def selection_idx(self, df_str, **kwargs):
        '''
        use item_descriptions.csv tags to find indices OR pass integer
        indices.  Use kwargs to indicate type
        ARGS:
        df_str:                     same as add_df and duplicate_column - string to
                                    access dataframe assigned to self.  Allows
                                    to select non item_descriptions.csv ZU march 2021
        target_tags (kwarg)         item or list of strings with desired tags
        indices (kwargs)            integer zero based indices - iloc. list of int
        alternative_select_col      dictionary with one key and val.  Created for
                                    management plan data candidates csv where diff
                                    groups want different layers uploaded.
        boolean                     column with boolean vals
        '''
        # SELECT BY TAGS
        df = getattr(self, df_str)

        if df_str == 'df':
            prop_str_indices_iloc = 'indices_iloc'
        else:
            df_base_str = df_str.replace('df_', '')
            prop_str_indices_iloc = '{}_indices_iloc'.format(df_base_str)
        try:
            target_tag = kwargs['target_tag']
            # list will be passed for multiple target tags
            if not isinstance(target_tag, list):
                target_tag = [target_tag]
            # pull tags column from df (list)
            parsed_list = self.parse_comma_sep_list(df_str, col_to_parse='TAGS')
            self.tags_from_df = parsed_list
            # find index if tags are present in col (list) and if tag matches target
            # iloc_tag = [idx for idx, tags in enumerate(tags_from_df) for val_targ in target_tag if (isinstance(tags, list)) and (val_targ in tags)]
            iloc_temp = []
            for target in target_tag:
                # the count will be index of dataframe rows.  It will repeat with
                # multiple target_tags but duplicates removed with set(iloc_temp)
                ct = 0
                try:
                    for tags in self.tags_from_df:
                        if target in tags:
                            iloc_temp.append(ct)
                        ct += 1
                except TypeError:
                    ct += 1
            # if multiple target_tags using set will slim down duplicate indices
            iloc_tag = list(set(iloc_temp))
            # get index names from iloc vals
            setattr(self, prop_str_indices_iloc, iloc_tag)
            self.indices = df.iloc[iloc_tag].index.tolist()
        # see if another target keyword is passed
        except KeyError:
            pass

        try:
            target_action = kwargs['target_action']
            # list will be passed for multiple target tags
            print('now we are in target action')
            if not isinstance(target_action, list):
                target_action = [target_action]
            # Provide column to match action values i.e. ACTION_agol (from join)
            try:
                fld = kwargs['alt_action_field']
            except KeyError:
                fld = 'ACTION'
            # pull tags column from df (list)

            parsed_list = self.parse_comma_sep_list(df_str, col_to_parse=fld)

            # find index if tags are present in col (list) and if tag matches target
            # iloc_tag = [idx for idx, tags in enumerate(tags_from_df) for val_targ in target_action if (isinstance(tags, list)) and (val_targ in tags)]
            iloc_temp = []
            for target in target_action:
                # the count will be index of dataframe rows.  It will repeat with
                # multiple target_actions but duplicates removed with set(iloc_temp)
                ct = 0
                for actions in copy.copy(parsed_list):
                    # check for nan vals
                    try:
                        if target in actions:
                            iloc_temp.append(ct)
                    # type error with nans in parsed list
                    except TypeError:
                        pass
                    ct += 1
                ct += 1
            # if multiple target_actions using set will slim down duplicate indices
            iloc_action = list(set(iloc_temp))
            iloc_action.sort()
            # get index names from iloc vals
            setattr(self, prop_str_indices_iloc, iloc_action)
            self.indices = df.iloc[iloc_action].index.tolist()
            print('iloc')
            print(' --- '.join([str(i) for i in iloc_action]))
            print('indices')
            print(' --- '.join(df.iloc[iloc_action].index.tolist()))
            # if not tags selection then indices will be     passed
        except KeyError:
            pass

        # SELECT BY ROW INDICES
        try:
            indices = kwargs['indices']
            # cast to list if not already (i.e. an int)
            # so dataframe NOT series is returned with .iloc
            if isinstance(indices, list):
                pass
            else:
                indices = [indices]
            # If indices passed were integers
            try:
                int(indices[0])
                print('indices {}'.format(indices))
                setattr(self, prop_str_indices_iloc, indices)
                self.indices = df.iloc[indices].index.tolist()
            # If indices were index_column vals (stirng)
            except ValueError:
                try:
                    self.indices = df.loc[indices].index.tolist()
                # Check that the index_col vals passes EXIST
                except KeyError:
                    print('index_col indices are not in index.  For examples\n'
                          'check spelling of item names')
        except KeyError:
            # there should be a a key either tags or indices so delete or resoovle code somehow
            pass

        try:
            # find matching indice in another dataframe in object and find
            # iloc values. ZU 20210525
            df_str_target = kwargs['get_iloc_alternate_df']
            df_target = getattr(self, df_str_target)
            alternate_df_iloc = []
            for indice in self.indices:
                try:
                    alternate_df_iloc.append(df_target.index.get_loc(indice))
                except KeyError:
                    print('missing index {}'.format(indice))
            attribute_str = '{}_indices_iloc'.format(df_str_target)
            print(attribute_str)
            setattr(self, attribute_str, alternate_df_iloc)
        except KeyError:
            pass

        # if using column other than tags to select rows.  Note: it is a dict
        try:
            indices_dict = kwargs['alternative_select_col']
            col_title = list(indices_dict.keys())[0]
            target_val = list(indices_dict.values())[0]
            print(col_title)
            print(target_val)
            # note a1), despite df.loc[] with just [], since subsetting we get a dataframe
            self.indices = df[df[col_title] == target_val].index.tolist()
            # get iloc vals TURN INTO FUNCTION SOMETIME
            iloc_temp = []
            ct = 0
            try:
                # note a2) even though [] like a1) this yields a series
                for alternative_val in df[col_title].to_list():
                    if target_val == alternative_val:
                        iloc_temp.append(ct)
                    ct += 1
            except TypeError:
                ct += 1
            self.indices_iloc = iloc_temp
        except KeyError:
            pass

        # using boolean vals in a col to get indices
        try:
            # pass a column name
            target_col_name = kwargs['boolean']
            target_col_vals = df[target_col_name].to_list()
            iloc_list = [idx for idx, item in enumerate(target_col_vals) if item is True]
            self.indices_iloc = copy.copy(iloc_list)
            self.indices = df.iloc[iloc_list].index.tolist()
        except KeyError:
            pass

    def parse_comma_sep_list(self, df_str, col_to_parse):
        '''
        takes string from tags column and parse into list of strings
        '''
        df = getattr(self, df_str)
        csl = df[col_to_parse].values.tolist()
        parsed_csl_temp = []
        for items in csl:
            try:
                # i.e. tags = 'wetlands, krrc'
                # tags.split(',') == ['wetlands', ' krrc']
                # tag.strip(' ') removes leading space for tags after position 1 (idx 0)
                # hence string to list
                parsed_csl_temp.append([item.strip(' ') for item in items.split(',')])
            except AttributeError:
                # nans from pd.read_csv(...) are saved as floats which have
                parsed_csl_temp.append([items])
        # for idx, item in enumerate(parsed_csl_temp):
        #     print(idx, ' ', item)
        return (parsed_csl_temp)

    def add_df(self, fp_csv, df_str, index_field):
        '''
        for adding additional dataframes. ZU 20210302
        fp_csv              path to new csv
        df_str               i.e. df2 or mxd_inventory
        index_field         for assigning index_col in DataFrame constructor
        '''
        # save df
        df = pd.read_csv(fp_csv, index_col = index_field, na_values = 'NA', dtype = 'str')
        setattr(self, df_str, df)

        # save path to csv
        df_base_str = df_str.replace('df_', '')
        fp_csv_prop_str = 'fp_csv_{}'.format(df_base_str)
        setattr(self, fp_csv_prop_str, fp_csv)

class proProject(commonUtils):
    '''
    INSERT / FLESH OUT
    '''
    def __init__(self, fp_aprx, fp_aprx_inv, target_col = 'DATA_LOCATION_MCMILLEN'):
        aprx_name = os.path.split(fp_aprx)[-1][:-5]
        setattr(self, 'fp_{}'.format(aprx_name), fp_aprx)
        aprx = arcpy.mp.ArcGISProject(fp_aprx)
        aprx_str = 'aprx_{}'.format(aprx_name)
        setattr(self, aprx_str, aprx)

        df_aprx_lyR_str = 'df_{}_lyR'.format(aprx_str[5:])
        df_aprx_lyR = pd.read_csv(fp_aprx_inv, index_col=target_col)
        setattr(self, df_aprx_lyR_str, df_aprx_lyR)

        aprx_lyR_csv_str = 'fp_{}_lyR_inv'.format(aprx_str[5:])
        setattr(self, aprx_lyR_csv_str, fp_aprx_inv)


    def get_base_aprx_content(self, aprx_str):
        '''
        fetches aprx maps and layouts from init attributes
        Args:
            aprx_str:       <aprx name>_aprx

        Returns:
        '''
        aprx = getattr(self, aprx_str)
        m =  aprx.listMaps()
        map_str = aprx_str.replace('aprx','maps')
        setattr(self, map_str, m)
        l = aprx.listLayouts()
        layout_str = aprx_str.replace('aprx','layouts')
        setattr(self, layout_str, l)
    def re_source_lyR_move(self, aprx_str, fp_csv_aprx_lyR_inv):
        # REMAP
        # 20240904

        import copy
        aprx = getattr(self, aprx_str)

        maps = aprx.listMaps()
        layers = []
        map_name = []
        ct = 0
        for m in maps:
            t = m.listLayers()
            layers.extend(t)
            map_name.extend([m.name] * len(t))
            ct += 1
        fp_csv_aprx_lyR_inv = getattr(fp_csv_aprx_lyr_inv)
        df_lyr_inv = pd.read_csv(fp_csv_aprx_lyR_inv)
        # normalize path
        fp_src_formatted = [os.path.normpath(fp) for fp in df_lyr_inv.source]
        df_lyr_inv['source'] = fp_src_formatted
        df_lyr_inv = df_lyr_inv.set_index('source')
        df_lyr_inv = df_lyr_inv[df_lyr_inv.develop]

        for lyr_src, mn in zip(layers, map_name):
           # Supports datasource?  i.e. servicer
           try:
               lyr_src.dataSource
               dsource = True
           except AttributeError:
               dsource = False
               pass
        if dsource:
           try:
               dbase_mapped = df_lyr_inv.loc[os.path.normpath(lyr_src.dataSource), 'connection_dbase']
               print('MAPNAME {} MAPPED:     {}'.format(mn, lyr_src))
               cp = lyr_src.connectionProperties
               cp_replace = copy.deepcopy(cp)
               cp_replace['connection_info']['database'] = dbase_mapped
               lyr_src.updateConnectionProperties(lyr_src.connectionProperties, cp_replace)
           except KeyError:
               print('MAPNAME {} NOT MAPPED: {}'.format(mn, lyr_src))
               pass

    def format_lyR_inv_datasource_standard(self, aprx_str, df_str, source_orig = 'DATA_LOCATION_MCM_ORIGINAL',
                             source_new='DATA_LOCATION_MCMILLEN'):
        # A) Gather Connetion Info
        df_aprx_lyR_str = 'df_{}_lyR'.format(aprx_str[5:])
        df_aprx_lyR = getattr(self, df_aprx_lyR_str)
        df_gdb_inv = getattr(self, df_str)

        # Use orig (path/to/fc i.e. DATA_LOCATION_MCMILLEN
        for idx in self.indices:
            idx_lyR = os.path.normpath(df_gdb_inv.loc[idx, source_orig])
            fp_new = os.path.normpath(df_gdb_inv.loc[idx, source_new])
            if fp_new[-4:] == '.shp':
                dbase_connection, fname = os.path.split(fp_new)
                df_aprx_lyR.at[idx_lyR, 'workspace_factory'] = 'Shape File'
            else:
                dbase_connection = '{}.gdb'.format(fp_new.split('.gdb')[0])
                fname = os.path.split(fp_new)[-1]
                df_aprx_lyR.at[idx_lyR, 'workspace_factory'] = 'File Geodatabase'
            df_aprx_lyR.at[idx_lyR, 'dataset'] = fname
            df_aprx_lyR.at[idx_lyR, 'dbase_connection'] = dbase_connection
            df_aprx_lyR.at[idx_lyR, 'ACTION'] = 'Update'
        aprx_lyR_csv_str = 'fp_{}_lyR_inv'.format(aprx_str[5:])
        df_aprx_lyR.to_csv(getattr(self, aprx_lyR_csv_str))


    def re_source_lyR_maestro(self, aprx_str, df_str, source_orig = 'DATA_LOCATION_MCM_ORIGINAL',
                              source_new='DATA_LOCATION_MCMILLEN'):
        # B) Connect
        idx_lyR_all = df_gdb_inv.loc[self.index, source_orig]
        df_aprx_lyR_subset = df_aprx_lyR.loc[idx_lyR_all]
        map_names_update = utilities_pro.unique_comma_sep_string(df_aprx_lyR_subset, 'map_name')
        map_objects = getattr(aprx_str.replace('aprx','maps'))
        for m in map_objects:
            if m.name in map_names_update:
                layers = m.listLayers()
                for lyr in layers:
                    try:
                        wsf = df_aprx_lyR_subset.loc[os.path.normpath(lyr.dataSource), 'workspace_factory']
                        dc = df_aprx_lyR_subset.loc[os.path.normpath(lyr.dataSource), 'dbase_connection']
                        dset = df_aprx_lyR_subset.loc[os.path.normpath(lyr.dataSource), 'dataset']

                        cp = lyr.connectionProperties
                        cp_replace = copy.deepcopy(cp)
                        cp_replace['workspace_factory'] = wsf
                        cp_replace['connection_info']['database'] = dc
                        cp_replace['dataset'] = dset
                        lyr.updateConnectionProperties(lyr.connectionProperties, cp_replace)
                    except KeyError:
                        pass






