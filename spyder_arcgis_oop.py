# ZRU 7/13/20
# To run this we need to be in arcgispro-py3 environment w/ GIS package:
# go to C:\\Program Files\\ArcGIS\\Pro\\bin\\Python\\Scripts and do: Start proenv.bat
# python2 to python3 compatability: https://pro.arcgis.com/en/pro-app/arcpy/get-started/python-migration-for-arcgis-pro.htm
# coding: utf-8

from __future__ import print_function, unicode_literals, absolute_import
from arcgis.gis import GIS
from arcgis.gis import Group
import os, sys
import glob
import copy
import pandas as pd
import numpy as np
import utilities
import datetime
import math
import xml.etree.ElementTree as ET
sys.path = [p for p in sys.path if '86' not in p]
import arcpy


class metaData(object):
    def __init__(self, fp_csv = r'C:\Users\uhlmann\Box\GIS\Project_Based\Klamath_River_Renewal_MJA\GIS_Data\item_descriptions.csv'):
        self.df = pd.read_csv(fp_csv, index_col = 'ITEM', na_values = 'NA', dtype='str')
        # scratch copy to add working data NOT intended for retainingin updated csv/database
        self.df_working = self.df.copy(deep = True)
        # fp_csv_archive creation.
        todays_date = datetime.datetime.today().strftime('%B %d %Y')
        self.fp_csv_archive = '{}_archive_{}.csv'.format(os.path.splitext(fp_csv)[0], todays_date)

    def zip_agol_upload(self):
        # 1) ZIP SHAPEFILES

        inDir = self.df.loc[self.indices]['DATA_LOCATION_MCMILLEN_JACOBS'].tolist()[0]
        outDir = '{}_zip'.format(inDir)
        if os.path.exists(outDir):
            pass
        else:
            os.mkdir(outDir)
        utilities.zipShapefilesInDir(inDir, outDir)
        setattr(self, 'outDir', outDir)

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
        '''
        # SELECT BY TAGS
        df = getattr(self, df_str)
        try:
            target_tag = kwargs['target_tag']
            # list will be passed for multiple target tags
            if not isinstance(target_tag, list):
                target_tag = [target_tag]
            # pull tags column from df (list)
            parsed_list = self.parse_comma_sep_list(df_str, col_to_parse = 'TAGS')
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
            self.indices_iloc = copy.copy(iloc_tag)
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
            # pull tags column from df (list)
            parsed_list = self.parse_comma_sep_list(df_str, col_to_parse = 'ACTION')
            print(parsed_list)

            # get proper df
            df_working_str = '{}_working'.format(df_str)
            df_working = getattr(self, df_working_str)

            # add actions to working dataframe
            df_working.assign(target_action = parsed_list)
            setattr(self, df_working_str, df_working)

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
                            print(ct)
                            iloc_temp.append(ct)
                    # type error with nans in parsed list
                    except TypeError:
                        pass
                    ct += 1
                ct += 1
            # if multiple target_actions using set will slim down duplicate indices
            iloc_action = list(set(iloc_temp))
            # get index names from iloc vals
            self.indices_iloc = copy.copy(iloc_action)
            self.indices = df.iloc[iloc_action].index.tolist()
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
                self.indices = df.iloc[indices].index.tolist()
                self.indices_iloc = copy.copy(indices)
            # If indices were index_column vals (stirng)
            except ValueError:
                try:
                    self.indices = df.loc[indices].index.tolist()
                #Check that the index_col vals passes EXIST
                except KeyError:
                    print('index_col indices are not in index.  For examples\n'
                            'check spelling of item names')
        except KeyError:
            # there should be a a key either tags or indices so delete or resoovle code somehow
            pass

        # if using column other than tags to select rows.  Note: it is a dict
        try:
            indices_dict = kwargs['alternative_select_col']
            col_title = list(indices_dict.keys())[0]
            target_val = list(indices_dict.values())[0]
            # note a1), despite df.loc[] with just [], since subsetting we get a dataframe
            self.indices = df.loc[self.df[col_title] == target_val].index.tolist()
            # get iloc vals TURN INTO FUNCTION SOMETIME
            iloc_temp = []
            ct = 0
            try:
                # note a2) even though [] like a1) this yields a series
                for alternative_val in self.df[col_title].to_list():
                    if target_val == alternative_val:
                        iloc_temp.append(ct)
                    ct += 1
            except TypeError:
                ct += 1
            self.indices_iloc = iloc_temp
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
                parsed_csl_temp.append(items)
        # for idx, item in enumerate(parsed_csl_temp):
        #     print(idx, ' ', item)
        return(parsed_csl_temp)

    def assemble_metadata(self):
        '''
        Create new metadata formatted in csv for updating element tree elements
        in write_xml.  If metadata already exists and we just want to append
        more data to idPurp then skip this step.
        '''
        # index of last column bracketing Purpose statement items
        idx_purpose = self.df.columns.get_loc('PURPOSE') -1
        # create string from columns with \\n delimeters
        purp = []
        # loop through columns which created or will create Purpose Statement
        for rw in self.df.iterrows():
            # rw = tuple of len 2 - rw[0] = row index beginning with 0. rw[1] = series of particular row
            # so this is a series with the columns as rows
            row_full = rw[1]
            dict = row_full[1:idx_purpose].dropna().to_dict()
            # create list of strings i.e. ['key1: val1', 'key2: val2']
            purp_indiv = ['{}: {}'.format(key, val) for key, val in zip(dict.keys(), dict.values())]
            # make string from list with \\n between items
            purp_indiv = '\n'.join(purp_indiv)
            purp.append(purp_indiv)
            # # now append abstract and credits if exist
            # abstract.append(row_full.ABSTRACT)
            # credits.append(row_full.CREDITS)

        # get purpose, abstract, credits from csv
        purpose_new = copy.copy(purp)
        abstract_new = self.df['ABSTRACT'].to_list()
        credits_new = self.df['CREDITS'].to_list()

        # escape characters not follow prob due to i don't know.
        credits_new_temp = []
        for cred in credits_new:
            try:
                # fixes escape character issue
                cred = cred.replace('\\n', '\n')
            except AttributeError:
                pass
            credits_new_temp.append(cred)

        # create new df to grab these elements the same indexing as main df
        index_df = self.df.index.tolist()
        self.df_meta_add = pd.DataFrame(np.column_stack(
                            [index_df, purpose_new, credits_new_temp, abstract_new]),
                            columns = ['index', 'purpose_new', 'credits_new', 'abstract'],
                            index = index_df)



    def write_xml(self, df_str, **kwargs):
        '''
        Update metadata to include assemble_metadata() statement or skip that
        step and add lines to existing Item Description.  This can be fleshed
        out to include add_credits, add_abstract too.
        ARGUMENTS
        df_str:                     same as add_df and duplicate_column - string to
                                    access dataframe assigned to self.  Allows
                                    to select non item_descriptions.csv ZU march 2021
        add_lines_purp (kwargs):    comma separated entry from item_desc with items
                                    being column titles from item_desc.
                                    i.e. DATA_LOCATION_MCMILLEN_JACOBS
        '''

        # FIND file paths to xmls of shapefiles FIGURE OUT FOR GDB
        fp_base = self.df.loc[self.indices]['DATA_LOCATION_MCMILLEN_JACOBS'].tolist()
        index_names = self.df.loc[self.indices].index.to_list()
        print(index_names)
        # glob strings will create the string to pass to  glob.glob which
        # uses th *xml wildcard to pull JUST the xml files from shapefile folder
        glob_strings = ['{}\\{}*.xml'.format(fp_base, index_name) for fp_base, index_name in zip(fp_base, index_names)]
        # ...(glob_string)[0] because it is a list of list - [[path/to/file]]
        # for item in glob_strings:
        #     print('NAME {}\nTYPE: {}'.format(item, type(item)))
        for glob_string in glob_strings:
            print('GLOBBING: {}'.format(glob_string))
            glob.glob(glob_string)[0]

        fp_xml_orig = [glob.glob(glob_string)[0] for glob_string in glob_strings]

        for item in fp_xml_orig:
            print(item)
        ct = 0
        # NOTE: In fury of AECOM dump AgOL upload THIS was added as a method simply
        # to append DATA_LOCATION_MCMILLEN_JACOBS key/pair to Item Description
        # need to fix all columns in this regard when writing xml
        # FIX THIS it is not prepared to handle other cases.
        add_new_purp_list = self.parse_comma_sep_list(df_str, col_to_parse = 'ADD_LINES_PURP')
        for idx, fp_xml in enumerate(fp_xml_orig):
            print('indice {}. path {}'.format(self.indices_iloc[ct], fp_xml))# refer to notes below for diff betw trees and elements
            ct+=1

            tree = ET.parse(fp_xml)
            # root is the root ELEMENT of a tree
            root = tree.getroot()
            # remove the mess in root
            # Parent for idPurp
            dataIdInfo = root.find('dataIdInfo')
            # search for element <idPurp> - consult python doc for more methods. find
            # stops at first DIRECT child.  use root.iter for recursive search
            # if doesn't exist.  Add else statements for if does exist and update with dict
            purp = dataIdInfo.find('idPurp')
            abstract = dataIdInfo.find('idAbs')
            credits = dataIdInfo.find('idCredit')

            index_name = index_names[idx]
            # the try block will add new lines to existing idPurp element
            # if specified.  Thus far used when adding a McMillen_Path : path/to/file
            # to Item Description when idPurp exists.
            new_purp_items = add_new_purp_list[self.indices_iloc[idx]]
            print('iloc {} new purp: {}'.format(self.indices_iloc[idx], new_purp_items))
            # if is a string this means there is a value.  if empty value it will be
            # a float for dumb reason.
            if isinstance(new_purp_items[0], str):
                purp_item, purp_value = [], []
                for item in new_purp_items:
                    purp_item.append(item)
                    purp_value.append(self.df.loc[index_name][item])

                # If add_purp but no purp exists(blank item desc) add new sub items
                if purp is None:
                    purpose_new = ['{}: {}'.format(key, val) for key, val in zip(purp_item, purp_value)]
                    purpose_new = '\n'.join(purpose_new)
                    print('new purp will be this:\n{}'.format(purpose_new))
                # add new purp to existing
                else:
                    # assemble new purpose items
                    sub_item_lst = purp.text.splitlines()
                    for key, val in zip(purp_item, purp_value):
                        print(purp_item, purp_values)
                        sub_item_lst = utilities.parse_item_desc(sub_item_lst, key, val)

                    # once the list is scoured and new items are either added or replaced
                    # join into one big string
                    purpose_new = '\n'.join(sub_item_lst)
                    print('should be adding this to EXISTING purp:\n{}'.format(purpose_new))
                    # purpose_new = purp.text + purpose_new

                element_text_list = [purpose_new]
                element_list = [purp]
                element_title = ['idPurp']

                # try:
                #     credits = kwargs['abstract']
                #     if credits.lower() == 'replace':
                #         credits_new = self.df.iloc[self.indices_iloc[ct]]['CREDITS']


            # If not adding lines to purp, etc.
            else:
                # get new element text
                index_name = index_names[idx]
                credits_new = self.df_meta_add.loc[index_name]['credits_new']
                abstract_new = self.df_meta_add.loc[index_name]['abstract']
                purpose_new = self.df_meta_add.loc[index_name]['purpose_new']
                element_text_list = [purpose_new, abstract_new, credits_new]
                element_list = [purp, abstract, credits]
                element_title = ['idPurp', 'idAbs', 'idCredit']

            for el, el_title, el_text in zip(element_list, element_title, element_text_list):
                # print('{}\\n{}\\n{}\\n'.format(el,el_title,el_text))
                # print('\\nel_text: \\n{}\\nel_type:\\n{}'.format(el_text[idx], type(el_text[idx])))
                if el is not None:
                    el.text = el_text
                    el.set('updated', 'ZRU_{}'.format(datetime.datetime.today().strftime('%d, %b %Y')))
                    # tree.write(fp_xml)

                # if the element does not exist yet
                elif (el is None):
                    # wierd if/else but if string means it exists
                    if isinstance(el_text, str):
                        # purp = purpose.text
                        el = ET.SubElement(dataIdInfo, el_title)
                        el.text = el_text
                        ET.dump(dataIdInfo)
                        # OPTIONAL: this adds an attribute - a key, val pair
                        el.set('updated', 'ZRU_{}'.format(datetime.datetime.today().strftime('%d, %b %Y')))

                    # when csv has no value - i.e. nan, str becomes a float to signify nan
                    # isnan() is a proxy for that.  Could is isinstanc(el_text, float) too
                    elif math.isnan(el_text):
                        print('this means nan float for thing')
                        pass

            tree.write(fp_xml)

    def quickie_inventory(self, **kwargs):
        '''
        quick grab item description to add to new csv for the gang.  ZRU 20201207
        '''

        # FIND file paths to xmls of shapefiles FIGURE OUT FOR GDB
        fp_base = self.df.loc[self.indices]['DATA_LOCATION_MCMILLEN_JACOBS'].tolist()
        index_names = self.df.loc[self.indices].index.to_list()
        print(index_names)

        # glob strings will create the string to pass to  glob.glob which
        # uses th *xml wildcard to pull JUST the xml files from shapefile folder
        glob_strings = ['{}\\{}*.xml'.format(fp_base, index_name) for fp_base, index_name in zip(fp_base, index_names)]
        fp_xml_orig = []
        for idx, glob_string in enumerate(glob_strings):
            try:
                # ...[0] because it is a list of list - [[path/to/file]]
                temp = glob.glob(glob_string)[0]
                print(temp)
                fp_xml_orig.append(temp)
            # if file not_uploaded, credit_crush, etc.  ZU 20210122
            except IndexError:
                fp_xml_orig.append(fp_base[idx])
        ct = 0
        # NOTE: In fury of AECOM dump AgOL upload THIS was added as a method simply
        # to append DATA_LOCATION_MCMILLEN_JACOBS key/pair to Item Description
        # need to fix all columns in this regard when writing xml
        # FIX THIS it is not prepared to handle other cases.
        purp_list = []
        abstract_list = []
        credits_list = []
        for idx, fp_xml in enumerate(fp_xml_orig):
            print('indice {}. path {}'.format(self.indices_iloc[idx], fp_xml))# refer to notes below for diff betw trees and elements
            try:
                tree = ET.parse(fp_xml)
                # root is the root ELEMENT of a tree
                root = tree.getroot()
                # remove the mess in root
                # Parent for idPurp
                dataIdInfo = root.find('dataIdInfo')
                # search for element <idPurp> - consult python doc for more methods. find
                # stops at first DIRECT child.  use root.iter for recursive search
                # if doesn't exist.  Add else statements for if does exist and update with dict
                purp = dataIdInfo.find('idPurp')
                abstract = dataIdInfo.find('idAbs')
                credits = dataIdInfo.find('idCredit')
                try:
                    purp_list.append(purp.text)
                except AttributeError:
                    purp_list.append(None)
                try:
                    abstract_list.append(abstract.text)
                except AttributeError:
                    abstract_list.append(None)
                try:
                    credits_list.append(credits.text)
                except AttributeError:
                    credits_list.append(None)
            except FileNotFoundError:
                str = 'AGOL upload status: {}'.format(fp_base[idx])
                purp_list.append(str)
                abstract_list.append(None)
                credits_list.append(None)
        # print('index {}\npurp {}\nabstract {}\ncredits {}\n'.format(index_names, purp_list, abstract_list, credits_list))

        df_quick_inventory = pd.DataFrame(np.column_stack(
                                [index_names, purp_list, abstract_list, credits_list]),
                                columns = ['feature_name', 'purpose', 'abstract', 'credits'])
        fp_out = r'C:\Users\uhlmann\Box\GIS\Project_Based\Klamath_River_Renewal_MJA\GIS_Request_Tracking\data_hunting_and_inventory\agol_klamath_data_assessment_2021b.csv'
        pd.DataFrame.to_csv(df_quick_inventory, fp_out)

    def add_df(self, fp_csv, df_str, index_field):
        '''
        for adding additional dataframes. ZU 20210302
        fp_csv              path to new csv
        df_str               i.e. df2 or mxd_inventory
        index_field         for assigning index_col in DataFrame constructor
        '''
        df = pd.read_csv(fp_csv, index_col = index_field, na_values = 'NA', dtype='str')
        setattr(self, df_str, df)
        # create working copy
        df_working_str = '{}_working'.format(df_str)
        setattr(self, df_working_str, df.copy(deep = True))
    def take_action_delete(self, action_type = 'delete'):
        for index in self.indices:
            fp_fcs = self.df.loc[index]['DATA_LOCATION_MCMILLEN_JACOBS']
            if arcpy.Exists(fp_fcs):
                print('deleting feature: {}'.format(index))
                arcpy.Delete_management(fp_fcs)
                self.df_working.drop(index, inplace = True)
            else:
                print('feature with ACTION == delete does not exist\n:{}'.format(index))
        pd.DataFrame.to_csv(self.df_working, self.fp_csv_archive)
            # pd.DataFrame.to_csv(self.df, self.fp_csv_archive)

    def df_sets(self, df_list, col_list):
        '''
        utility to find overlapping and symmetric differences between different
        dataframes and columns.  Can add more funcitonality.  ZU 20210301
        Protocol: first agolZ.add_df (x2) for two csvs.  Then find overlapping
        values in selected fields (col_list).
        this was used to determine if a csv of inventories contained all mxds in another
        csv for the ramp
        ARGUMENTS
        df_list         ['dataframe1', 'dataframe2']
        col_list        ['col_dframe1', 'col_dframe2'] At this point, col_list items
                        cannot be index fields
        '''
        df1_str = df_list[0]
        df2_str = df_list[1]
        df1 = getattr(self, df1_str)
        df2 = getattr(self, df2_str)
        col1 = col_list[0]
        col2 = col_list[1]
        set1 = set(df1[col1])
        set2 = set(df2[col2])
        df1_present_df2_absent = set1.difference(set2)
        df2_present_df1_absent = set2.difference(set1)
        df_names = [df1_str] * len(df1_present_df2_absent) + [df2_str] * len(df2_present_df1_absent)
        symmetric_diff = list(df1_present_df2_absent) + list(df2_present_df1_absent)
        df_symm_diff = pd.DataFrame(np.column_stack([df_names, symmetric_diff]),
                    columns = ['field_name', 'data'])
        df_name = '{}_{}_symmetric_difference'.format(df1_str, df2_str)
        setattr(self, df_name, df_symm_diff)
        print('Property with symmetric difference dataframe saved as: \n{}'.format(df_name))
    def mark_duplicate_rows(self, df_str, target_col):
        '''
        function for finding duplicates from "seen = set()" to "seen.add()"
        should be decomposed into utilities and imported here.
        This funciton was used when cleaning up the Klamath mess to find duplicate
        files used so I would not delete a fc that was turned off (unnecessary)
        in one map, but present in another 200 rows down.  ZU 20210302
        ARGUMENTS
        df_str                  string to access dataframe attribute.  Note: use
                                self.add_df(fp_csv_target) to add dataframe to
                                object
        target_col              column in dataframe to find duplicates
        '''
        df = getattr(self, df_str)
        # adapted from here:
        # https://stackoverflow.com/questions/9835762/how-do-i-find-the-duplicates-in-a-list-and-create-another-list-with-them
        seen = set()
        dup = []
        target_lst = df[target_col].to_list()
        for x in target_lst:
            if x in seen:
                dup.append(x)
            else:
                seen.add(x)
        # remove duplicate duplicates
        dup = list(set(dup))
        # initiate new column
        df['duplicate'] = math.nan
        for idx, item in enumerate(dup):
            loc = df.index[df[target_col] == item]
            df.loc[loc, 'duplicate'] = idx
        # setattr to replace original dataframe with new df with added col
        setattr(self, df_str, df)

    def merge_feats(self, df_str, target_fc, action = 'merge', **kwargs):
        '''
        belongs in python 2 mxd_utilities with arcpy.Mapping module, but that shit's
        broken.  ZU 3/3/2021.  updated 3/10/21
        ARGUMENTS
        kwargs[field_mappings]      list of fields to RETAIN.  Additionally, orig_fname
                                    and orig_fpath will be added
        df_str                      select dataframe from self
        target_fc                   output fc
        action                      just merge at this point
        '''

        arcpy.env.overwriteOutput = True
        merge_lyrs = []
        # if field mappings requested
        try:
            fields_to_map = kwargs['field_mappings']
            if not isinstance(fields_to_map, list):
                fields_to_map = [fields_to_map]
            field_mappings = arcpy.FieldMappings()
            field_mappings_true = True
        except KeyError:
            field_mappings_true = False

        for i, index in enumerate(self.indices):
            df = getattr(self, df_str)
            # replace or else unicode error
            fp_fcs = df.loc[index]['layer_source'].replace('\\','/')
            fcs_name = os.path.basename(fp_fcs)
            if arcpy.Exists(fp_fcs):
                lyr_name = 'merge_lyr_{}'.format(i + 1)
                fcs_obj = arcpy.FeatureClassToFeatureClass_conversion(fp_fcs, 'in_memory', lyr_name)
                # get feature path
                lyr_path = fcs_obj[0]
                # add new field
                print('adding fname {}'.format(fcs_name))
                arcpy.AddField_management(lyr_path, 'orig_fname', 'text', field_length = 50)
                arcpy.CalculateField_management(lyr_path, 'orig_fname', '"{}"'.format(fcs_name), "PYTHON")
                arcpy.AddField_management(lyr_path, 'orig_fpath', 'text',field_length = 254)
                arcpy.CalculateField_management(lyr_path, 'orig_fpath', '"'+fp_fcs+'"', "PYTHON")
                # arcpy.CalculateField_management(lyr_path, 'orig_fpath', '"{}"'.format(fp_fcs), "PYTHON")
                print('adding fcs to merge list:\n{}'.format(fcs_name))
                merge_lyrs.append(lyr_path)  #list of feat names
                if field_mappings_true:
                    field_mappings.addTable(lyr_path)
            else:
                print('feature with ACTION == delete does not exist:\n{}'.format(fcs_name))
        # direct from field mappings arc documentation
        fields_to_map.extend(['orig_fname', 'orig_fpath'])
        if field_mappings_true:
            for field in field_mappings.fields:
                if field.name not in fields_to_map:
                    field_mappings.removeFieldMap(field_mappings.findFieldMapIndex(field.name))
            arcpy.Merge_management(merge_lyrs, target_fc, field_mappings)
        else:
            arcpy.Merge_management(merge_lyrs, target_fc)

class AgolAccess(metaData):
    '''
    Basic init for AGOL access
    '''

    def __init__(self, fp_csv, credentials):
        '''
        need to add credentials like a key thing.  hardcoded currently
        '''
        super().__init__(fp_csv)
        u_name = 'uhlmann@mcmjac.com'
        u_name2 = 'zuhlmann@mcmjac.com'
        p_word = 'Gebretekle24!'
        p_word2 = 'Mcmjac081'
        setattr(self, 'mcmjac_gis',  GIS(username = u_name, password = p_word))
        print('Connected to {} as {}'.format(self.mcmjac_gis.properties.portalHostname, self.mcmjac_gis.users.me.username))
        # dictionary that can be expanded upon
        self.item_type_dict = {'shapefile': 'shapefile', 'feature': 'Feature Layer Collection', 'feature2': 'Feature Layer'}

    def get_group(self, group_key):
        '''
        hardcoded. update if more groups become necessary.
        '''
        group_dict = {'krrp_geospatial': 'a6384c0909384a43bfd91f5d9723912b',
                        'klamath_river_test': '01b12361c9e54386a955ba6e3279b09'}
        group_id = group_dict[group_key]
        krrp_geospatial = Group(getattr(self, 'mcmjac_gis'), group_id)
        setattr(self, group_key, krrp_geospatial)

    def identify_items_online(self, itemType=['shapefile', 'feature'], **kwargs):
        '''
        find items already online
        '''
        if isinstance(itemType, list):
            pass
        else:
            itemType = [itemType]
        # item_type_dict created in __init__
        for item in itemType:
            itemType = self.item_type_dict[item]
            items = self.mcmjac_gis.content.search('owner: uhlmann@mcmjac.com',
                                            item_type = itemType, max_items = 900)
            itemType = itemType.replace(' ', '_').lower()
            setattr(self, 'user_content_{}'.format(itemType), items)
            # filtered tags attribute
        try:
            tags = kwargs['tags']
            items_filtered = [item for item in items if tags in item.tags]
            # format text for attribute to replace spaces with underSc
            itemType_text = itemType.replace(' ', '_')
            setattr(self, 'user_content_{}_{}'.format(tags, itemType_text), items_filtered)
        except KeyError:
            pass

    def take_action(self, action_type, itemType = ['feature','shapefile']):
        '''
        perform applicable actions from action column. ZU 202102025.  Thus far
        only for remove.  will add others and perhaps a log for each run.
        ARGS
        itemType       same as identify_items_online method. pass as list of
                        strings or one string.  i.e 'shapefile'.  Default =
                        ['shapefile', 'feature']
        action_type     thus far just 'remove' but need to add 'tags', publish
                        and 'share'
        '''
        ct = 1
        for item in itemType:
            item = self.item_type_dict[item]
            item = item.replace(' ', '_').lower()
            str = 'user_content_{}'.format(item)
            user_content = getattr(self, str)
            if action_type == 'remove':
                for content_item in user_content:
                    title = content_item.title
                    if title in self.indices:
                        content_item.delete()
                        # Only need update csv once! Not both for shapefile and feature
                        if ct == 1:
                            # gets idx in df; assumes just ONE item with exact name -NOT > 1
                            # this is for useing ALTERNATE column - not INDEX
                            # idloc = (self.df_working.ITEM == title).idxmax()
                            # fancy method to value for action at idloc
                            initial_vals = self.df_working.at[title, 'ACTION']
                            # basically parse comma separated While removing spaces
                            updated_vals = [vals.strip(' ') for vals in initial_vals.split(',')]
                            updated_vals.remove('remove')
                            # if no actions remain, then set to nan
                            # seems to work without converting NoneType to math.nan, but just in case
                            # upon import None and NaN = NaN (df = pd.read_csv(fp_csv))
                            # checking for None - interesting post:
                            # https://stackoverflow.com/questions/23086383/how-to-test-nonetype-in-python
                            if updated_vals is None:
                                updated_vals = math.nan
                            # otherwise, join back into comma separated string
                            else:
                                updated_vals = ', '.join(updated_vals)
                            print('updating vals for {}'.format(content_item))
                            self.df_working.at[title, 'ACTION'] = updated_vals
                            # set status to offline
                            self.df_working.at[title, 'AGOL_STATUS'] = 'offline'
            # keep count going
            ct += 1
        fp_out = r'C:\Users\uhlmann\code\item_description_updated_test.csv'
        pd.DataFrame.to_csv(self.df_working, fp_out)


    def add_agol_upload(self, **kwargs):
        '''
        currently passing snippets as kwarg but could be drawn from column in
        csv in future.  shapefiles need to be zipped and in file structure
        before using this.
        df_str:                     same as add_df and duplicate_column - string to
                                    access dataframe assigned to self.  Allows
                                    to select non item_descriptions.csv ZU march 2021
        '''

        # grab tags of iloc ONLY if they were zipped  CONSIDER MOVING TO def indices
        # OR ABSTRACT as function with values and column names to ignore
        ignore_upload = ['not_zipped', 'shapefile_failed', 'not_uploaded']
        indices_loc = [idx for idx in self.indices_iloc if self.df.iloc[idx].DATA_LOCATION_MCMILLEN_JACOBS not in ignore_upload]

        titles = self.df.iloc[indices_loc].index.values.tolist()

        # tags
        # try except grabs all parsed_tags in df
        # tags_temp will pull those selected in index
        try:
            tags = self.tags_from_df
        except AttributeError:
            tags = self.parse_comma_sep_list(df_str, 'TAGS')
        # subset tags in index
        tags_temp = []
        for iloc in indices_loc:
            tags_temp.append(tags[iloc])
        tags = tags_temp


        # consider adding snippets to item_description.csv
        try:
            snippets = kwargs['snippets']
            # we want a list
            if isinstance(snippets, list):
                pass
            # cast as list if string
            elif isinstance(snippets, str):
                snippets = [snippets]
            # DETERMINE snippet creation based on what was pased
            # same snippet for all
            if len(indices) == 1:
                snippets = snippets * len(titles)
            # custom snippets
            elif len(snippets) == len(titles):
                pass
            else:
                sys.exit('len(snippet) != len(indices)')
        except:
            snippets =[None] * len(titles)

        # need indices from self.selection_idx
        # YES this is correct.  Each shapefile gets its OWN zip folder
        upload_folders = self.df.loc[titles]['DATA_LOCATION_MCMILLEN_JACOBS'].values.tolist()
        parent_zip_folder = ['{}_zip'.format(upload_folder) for upload_folder in upload_folders]
        zipped_folders = [os.path.join(zip_folder, title) for zip_folder, title in zip(parent_zip_folder, titles)]
        zipped_folders = ['{}.zip'.format(zip_folder) for zip_folder in zipped_folders]
        # check if they exist:
        for zip_dir in zipped_folders:
            print(zip_dir)
            if os.path.exists(zip_dir):
                pass
            else:
                sys.exit('paths dont exist')

         # zipped_dir will be index title
        for idx, shp in enumerate(zipped_folders):
            properties_dict = {'title':titles[idx],
                                'tags':tags[idx],
                                'snippet':snippets[idx]}
            fc_item = self. mcmjac_gis.content.add(properties_dict, data = shp)
            # fc_item.share(groups = 'a6384c0909384a43bfd91f5d9723912b')
            print('ct = {} \\n fc_item {} '.format(idx, fc_item))

    def email_group(self):
        signature = 'Zach Uhlmann     GIS Specialist     (206) 920-2478     uhlmann@mcmjac.com'
        #
        # Group User Info: dict with keys - owner, admins, users
        try:
            members_dict = krrp_geospatial.get_members()
        except NameError:
            self.get_group('krrp_geospatial')
            members_dict = self.krrp_geospatial.get_members()
        # create list of lists
        list_list = [members_dict[key] for key in members_dict.keys()]
        # flatten list
        all_members = [member for members in list_list for member in members if isinstance(members, list)]

        zach = members_dict['owner']
        subject = 'Klamath River Renewal ArcGIS Online Reorganizing'
        email_body = '''Hi everybody,\n\nApologies on the formatting of this
                        message but I have limited communication functionality
                        in Groups for ArcGIS Online, particularly formatting text.
                        I wanted to let everyone know that we have rearranged
                        some content on our ArcGIS Online Group "KRRP_Geospatial".
                        I updated and added metadata to the existing datasets -
                        feature layers and shapefiles - to ensure that Item
                        Descriptions in ArcGIS products are informative and
                        archival.  This includes metadata describing
                        data origins, status (current or
                        archival), file location, type, etc.\n\n
                        I also parsed the existing geodatabases (gdb)
                        into individual shapefiles and will REMOVE the
                        gdbs.  The only data this pertains to is the Wetlands.gdb
                        and requested_layers_working.gdb (FERC bdrs
                        and LoW_60Design).  The exact contents of those gdbs are
                        now available as individual shapefiles.  I have yet to
                        remove them, so if anybody objects please let me know.
                        I wanted to give everyone a heads up in case those files
                        slated for replacement are used in personal maps online.
                        \n\nFeel free to contact me if you have questions.  Also,
                        please RESPOND WITH YOUR EMAIL ADDRESS FOR FUTURE COMMUNICATION.
                        That way I can format e-mails properly.   {}.
                        \n\n'''.format(signature)
        self.krrp_geospatial.notify(all_members, subject, email_body, 'email')


    # # used to remove subelements made messing arounc
    # el_list = ['idTestZRU', 'idPurp']
    # for el_str in el_list:
    #     el_remove = root.find(el_str)
    #     try:
    #         root.remove(el_remove)
    #     except TypeError:
    #         pass
    # tree.write(fp_xml)

# XML NOTES
# 1) ATTRIBUTTES are useful for metadata (data about data)
# 8/6/2020
# Use attributes for Metadata (https://www.w3schools.com/xml/xml_attributes.asp):
# SEE the id="501".  GOOD IDEA
# <messages>
#     <note id="501">
#         <to>bnasty</to>
#         <from>zach</from>
#     </note>
#     note id="502">
#         <to>mom</to>
#         <from>zach</from>
#     </note>
# </messages>

# 2) TREES and ELEMENTS
# 8/6/2020
# from here: https://docs.python.org/2/library/xml.etree.elementtree.html
# XML is an inherently hierarchical data format, and the most natural way to represent it is
# with a tree. ET has two classes for this purpose - ElementTree represents the whole XML document
# as a tree, and Element represents a single node in this tree. Interactions with the whole
# document (reading and writing to/from files) are usually done on the ElementTree level.
# Interactions with a single XML element and its sub-elements are done on the Element level.

# 3)  RANDOM
# dir from ET object
# root iterates with [child for child in root] to datatype xml.etree.ElementTree.Element with dir of each element or child
# ['__class__', '__copy__', '__deepcopy__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
# '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__len__',
#'__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__setstate__',
# '__sizeof__', '__str__', '__subclasshook__', 'append', 'attrib', 'clear', 'extend', 'find', 'findall', 'findtext', 'get',
# 'getchildren', 'getiterator', 'insert', 'items', 'iter', 'iterfind', 'itertext', 'keys', 'makeelement', 'remove', 'set', 'tag', 'tail', 'text']

# # 4) share items
# feat_layer_list = mcmjac_gis.content.search(query = 'owner: uhlmann@mcmjac.com', item_type = 'Feature Layer Collection', max_items = 50)
# target_tag = 'wetlands'
# # find features which are wetlands
# feats = [feat for feat in feat_layer_list if target_tag in feat.tags]
#
# # publishing is EASY:
# for feat in feats:
#     feat.publish()
# # sharing is EASY
# for feat in feats:
#     feat.share(groups = [krrp_geospatial])
# # for feat in feats:
# #     print(feat)


# # 4) One off eagle data
# eagle_gdb = 'eagle_features\\KlamathEagleImpactAnalysis_20200714_gdb\\KlamathEagleImpactAnalysis_20200714.gdb'
# fp_gdb = os.path.join(fp_new_data, eagle_gdb)
# fcs = ['BaldEagleTerritoryZones_20200424', 'EagleTerritoryPoints_20200415_Proj',
#     'EagleViewingLocations_20200312', 'GoldenEagleTerritoryZones_20200424',
#     'GoldenEagleViewsheds_20200114']
# fp_fcs = [os.path.join(fp_gdb, fc) for fc in fcs]
# [arcpy.FeatureClassToGeodatabase_conversion(fc, fp_out) for fc in fp_fcs]

# # 4) GIS Random tidbits
# # print content
# krrp_content = krrp_geospatial.content()
# # string search from parse_dir
# target_content = krrp_content[5]
# print(target_content)
# target_id = target_content.id
# feature_collection = mcmjac_gis.content.get(target_id)
# fp_download = 'C:\\Users\\uhlmann\\box_offline\\test_download'
# gdb_name = 'eagle.gdb'
# result = feature_collection.export(gdb_name, 'File Geodatabase')
# result.download(fp_download)


# # dir(feat) from features mcmjac_gis.content.search()
# '_ux_item_type', '_workdir', 'access', 'accessInformation', 'add_comment', 'add_relationship',
#  'appCategories', 'app_info', 'avgRating', 'banner', 'categories', 'clear', 'comments', 'content_status',
#  'copy', 'copy_feature_layer_collection', 'create_thumbnail', 'create_tile_service', 'created', 'culture',
#   'delete', 'delete_rating', 'delete_relationship', 'dependencies', 'dependent_to', 'dependent_upon',
#   'description', 'documentation', 'download', 'download_metadata', 'download_thumbnail', 'export', 'extent',
#    'fromkeys', 'get', 'get_data', 'get_thumbnail', 'get_thumbnail_link', 'groupDesignations', 'guid',
#    'homepage', 'id', 'industries', 'isOrgItem', 'itemid', 'items', 'keys', 'languages', 'largeThumbnail',
#    'layers', 'licenseInfo', 'listed', 'metadata', 'modified', 'move', 'name', 'numComments', 'numRatings',
#    'numViews', 'owner', 'ownerFolder', 'pop', 'popitem', 'properties', 'protect', 'protected', 'proxies',
#    'proxyFilter', 'publish', 'rating', 'reassign_to', 'register', 'related_items', 'resources', 'scoreCompleteness',
#    'screenshots', 'setdefault', 'share', 'shared_with', 'snippet', 'spatialReference', 'status', 'tables', 'tags',
#     'thumbnail', 'title', 'type', 'typeKeywords', 'unregister', 'unshare', 'update', 'url', 'usage', 'values']
