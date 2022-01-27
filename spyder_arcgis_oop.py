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
    def __init__(self,  prj_file, subproject_str,
                df_str = 'df', df_index_col = 'ITEM', **kwargs):
        '''
        KEYWORD ARGS:
        fill in now that reworked
        '''
        fp_csv_lookup = r'C:\Users\uhlmann\Box\GIS\Project_Based\Klamath_River_Renewal_MJA\GIS_Data\data_inventory_and_tracking\path_list_updated.csv'
        lookup_table = pd.read_csv(fp_csv_lookup, index_col = 'gdb_str',dtype='str')
        setattr(self, 'lookup_table', lookup_table)
        fp_csv = lookup_table[lookup_table.subproject==subproject_str].fp_maestro_csv.values[0]
        setattr(self, 'subproject_str', subproject_str)
        df = pd.read_csv(fp_csv, index_col = df_index_col, na_values = 'NA', dtype='str')
        setattr(self, df_str, df)
        # fp_csv_archive creation.
        todays_date = datetime.datetime.today().strftime('%Y%m%d')
        self.todays_date = todays_date
        todays_date_verbose = datetime.datetime.today().strftime('%B %d %Y')
        self.todays_date_verbose = todays_date_verbose
        basepath = os.path.splitext(fp_csv)[0]

        # save path to csv
        if df_str == 'df':
            fp_csv_prop_str = 'fp_csv'
        else:
            # passing a different base df
            df_base_str = df_str.replace('df_', '')
            fp_csv_prop_str = 'fp_csv_{}'.format(df_base_str)

        setattr(self, fp_csv_prop_str, fp_csv)

        # adds fp_log, csv_archive, csv_temp, etc.
        self.create_base_properties(df_str)

        # PRJ FILE
        self.prj_file = prj_file
    def fcs_to_shp_agol_prep(self, df_str, target_col = 'DATA_LOCATION_MCMILLEN_JACOBS'):
        '''
        Created long time ago.  Edited for different workflow - i.e. pass indices
        for one here to fcs to fcs then zip in separate funcion which calls zipping utilities

        ARGS:
        df_str              df for example
        target_col          col name for  col with file path to fcs for conversion
        '''

        df = getattr(self, df_str)
        ct = 0
        for indice in self.indices:
            inDir = df.loc[indice, 'AGOL_DIR']
            inDir = os.path.join(inDir, indice)
            # shp subdir does not exist
            if not os.path.exists(inDir):
                os.mkdir(inDir)
            fp_fcs_in = df.loc[indice][target_col]
            symb = '-'*20
            fp_shp = os.path.join(inDir, indice + '.shp')
            if not arcpy.Exists(fp_shp):
                print('{}  CONVERTING  {}\nInput FCS: {}\nOutput SHP: {}'.format
                                (symb, symb, fp_fcs_in, '{}.shp'.format(indice)))
                arcpy.FeatureClassToFeatureClass_conversion(fp_fcs_in, inDir, indice)
                print('{}  CONVERSION COMPLETE  {}'.format(symb, symb))
            else:
                print('SHAPEFILE EXISTS\n {}\nDID NOT CONVERT'.format(fp_shp))

    def zip_shp_agol_prep(self, base_dir_shp, **kwargs):
        '''
        Created long time ago.  Edited for different workflow - i.e. pass indices
        for one fell swoop within function as opposed to calling within for loop.
        Also, convert fcs to shp AND zip in one fell swoop.  ZU 5/21/21

        ARGS:
        base_dir_shp:           path/to/dir/with/agol_Uploads/2020_10_05
        exclude_files:          take from self.indices --> string of shapefile name
                                to exclude from zipping (already zipped)
        '''

        yyyy_mm_dd = os.path.basename(base_dir_shp)
        # create subdir JUST for shapefiles

        inDir = os.path.join(base_dir_shp, yyyy_mm_dd)
        # shp subdir does not exist
        if not os.path.exists(inDir):
            os.mkdir(inDir)

        outDir = '{}_zip'.format(inDir)
        # ensure shp_dir does not already exist
        if not os.path.exists(outDir):
            os.mkdir(outDir)

        # 3) ZIP all Files at once
        try:
            # exclude files if already zipped
            exclude_files = kwargs['exclude_files']
            utilities.zipShapefilesInDir(inDir, outDir, exclude_files = exclude_files)
        except KeyError:
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
        boolean                     column with boolean vals
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
            self.indices_iloc = copy.copy(iloc_action)
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
        return(parsed_csl_temp)

    def write_xml(self, df_str, shp = False, **kwargs):
        '''
        Update metadata to include assemble_metadata() statement or skip that
        step and add lines to existing Item Description.  This can be fleshed
        out to include add_credits, add_abstract too.
        ARGUMENTS
        df_str:                     same as add_df and duplicate_column - string to
                                    access dataframe assigned to self.  Allows
                                    to select non item_descriptions.csv ZU march 2021
        '''
        df = getattr(self, df_str)

        # archive before deleting - this saves an archive csv
        self.save_archive_csv(df_str)

        if df_str == 'df':
            prop_str_fp_logfile = 'fp_log'
            prop_str_indices_iloc = 'indices_iloc'
        else:
            df_base_str = df_str.replace('df_','')
            prop_str_fp_logfile = 'fp_log_{}'.format(df_base_str)
            prop_str_fp_csv = 'fp_csv_{}'.format(df_base_str)
            prop_str_indices_iloc = '{}_indices_iloc'.format(df_str)

        fp_logfile = getattr(self, prop_str_fp_logfile)

        logging.basicConfig(filename = fp_logfile, level = logging.DEBUG)

        # Save call string to logfile
        banner = '    {}    '.format('-'*50)
        fct_call_str = 'Performing function write_xml'
        date_str = datetime.datetime.today().strftime('%D %H:%M')
        msg_str = '\n{}\n{}\n{}\n{}\n'.format(banner, date_str, banner, fct_call_str)
        logging.info(msg_str)

        # may not use too often -  legacy from before master.gdb and direct gdb
        # updating ZU 20210505
        if shp:
            # FIND file paths to xmls of shapefiles FIGURE OUT FOR GDB
            # NOTE fp_base is refering to base name for shapefiles (since multiple file extensions
            # under same BASE name)
            fp_shp = df.loc[self.indices]['DATA_LOCATION_MCMILLEN_JACOBS'].tolist()
            index_names = df.loc[self.indices].index.to_list()
            # glob strings will create the string to pass to  glob.glob which
            # uses th *xml wildcard to pull JUST the xml files from shapefile folder
            glob_strings = ['{}*.xml'.format(fp_shp) for fp_shp in fp_shp]
            # ...(glob_string)[0] because it is a list of list - [[path/to/file]]
            # for item in glob_strings:
            #     print('NAME {}\nTYPE: {}'.format(item, type(item)))
            # # PRINT BELOW DEBUG
            # for glob_string in glob_strings:
            #     print('GLOBBING: {}'.format(glob_string))
            #     glob.glob(glob_string)[0]

            fp_xml_orig_shp = [glob.glob(glob_string)[0] for glob_string in glob_strings]

        # key/val and key lists for add and subtract purpose list respectively
        add_new_purp_list = self.parse_comma_sep_list(df_str, col_to_parse = 'ADD_LINES_PURP')
        subtract_new_purp_list = self.parse_comma_sep_list(df_str, col_to_parse = 'REMOVE_LINES_PURP')
        ct = 0

        indices_iloc = getattr(self, prop_str_indices_iloc)
        for indice, indice_iloc in zip(self.indices, indices_iloc):
            if shp:
                fp_xml = fp_xml_orig_shp[ct]
                temp_path = copy.copy(fp_xml)
            elif not shp:
                fp_fcs = df.loc[indice]['DATA_LOCATION_MCMILLEN_JACOBS']
                temp_path = copy.copy(fp_fcs)
                tgt_item_md = arcpy.metadata.Metadata(fp_fcs)
                fp_xml = arcpy.CreateScratchName('.xml', workspace = arcpy.env.scratchFolder)
                # copy xml of feature class -- next up - update it
                tgt_item_md.saveAsXML(fp_xml, 'EXACT_COPY')
            ct += 1

            print('indice {}. path {}'.format(indice_iloc, temp_path))# refer to notes below for diff betw trees and elements
            tree = ET.parse(fp_xml)
            # root is the root ELEMENT of a tree
            root = tree.getroot()
            # remove the mess in root
            # Parent for idPurp
            dataIdInfo = root.find('dataIdInfo')

            # search for element <idPurp> - consult python doc for more methods. find
            # stops at first DIRECT child.  use root.iter for recursive search
            # if doesn't exist.  Add else statements for if does exist and update with dict
            if pd.isnull(dataIdInfo):
                fp_xml_template = r'C:\Users\uhlmann\Box\WR Users\Employees\zuhlmann\prj_files\xml_template_source.xml'
                print('\n{} contained no Item Desc - \nTemplate used instead: \n{}\n'.format(indice, fp_xml_template))
                tree = ET.parse(fp_xml_template)
                # root is the root ELEMENT of a tree
                root = tree.getroot()
                dataIdInfo = root.find('dataIdInfo')


            purp = dataIdInfo.find('idPurp')
            abstract = dataIdInfo.find('idAbs')
            credits = dataIdInfo.find('idCredit')


            # ADD NEW PURP
            new_purp_items = add_new_purp_list[indice_iloc]
            # SUBTRACT NEW PURP
            subtract_purp_items = subtract_new_purp_list[indice_iloc]

            # the try block will add new lines to existing idPurp element
            # if specified.  Thus far used when adding a McMillen_Path : path/to/file
            # to Item Description when idPurp exists.

            # if is a string this means there is a value.  if empty value it will be
            # a float for dumb reason.
            if not isinstance(new_purp_items[0], str):
                # Marks To Do if - do NOT update purp unless subtract_lines_purp specified below
                update_purp = False
                pass
            else:
                # Marks To Do if - proceed with updating Purp
                update_purp = True
                purp_item, purp_value = [], []
                for item in new_purp_items:
                    purp_item.append(item)
                    purp_value.append(df.loc[indice][item])

                # If add_purp but no purp exists(blank item desc) add new sub items
                if purp is None:
                    purpose_new = ['{}: {}'.format(key, val) for key, val in zip(purp_item, purp_value)]
                    purpose_new = '\n'.join(purpose_new)
                elif purp.text is None:
                    purpose_new = ['{}: {}'.format(key, val) for key, val in zip(purp_item, purp_value)]
                    purpose_new = '\n'.join(purpose_new)
                # add new purp if existing
                else:
                    # assemble new purpose items
                    sub_item_lst = purp.text.splitlines()
                    # ADDING lines
                    for key, val in zip(purp_item, purp_value):
                        sub_item_lst = utilities.parse_item_desc(sub_item_lst, key, val)

                    # once the list is scoured and new items are either added or replaced
                    # join into one big string
                    purpose_new = '\n'.join(sub_item_lst)

                # LOG and DOCUMENT DF
                msg_str = 'NEW PURPOSE for\n{}:\n{}'.format(indice, purpose_new)
                # purpose_new = purp.text + purpose_new
                df.at[indice, 'ADD_LINES_PURP'] = ''

            # Nan from pd.dataframe.read_csv == dtype float
            if isinstance(subtract_purp_items[0], str):
                if purp is None:
                    # no purpose to extract
                    pass
                elif purp.text is None:
                    pass
                else:
                    # Did not update Add
                    if not update_purp:
                        sub_item_lst = purp.text.splitlines()
                    # Updated add
                    else:
                        sub_item_lst = purpose_new.splitlines()
                    # Update Subtract
                    for key in subtract_purp_items:
                        sub_item_lst = utilities.parse_item_desc(sub_item_lst, key, '', False)
                        purpose_new = '\n'.join(sub_item_lst)

                    # Marks To Do - proceed with updating Purp
                    update_purp = True

                    msg_str = 'NEW PURPOSE for\n{}:\n{}'.format(indice, purpose_new)
                    df.at[indice, 'REMOVE_LINES_PURP']=''

            if update_purp:
                element_text_list = [purpose_new]
                element_list = [purp]
                element_title = ['idPurp']

                # log what the new purp will look like
                logging.info(msg_str)

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
                            # ET.dump(dataIdInfo)
                            # OPTIONAL: this adds an attribute - a key, val pair
                            el.set('updated', 'ZRU_{}'.format(datetime.datetime.today().strftime('%d, %b %Y')))

                        # when csv has no value - i.e. nan, str becomes a float to signify nan
                        # isnan() is a proxy for that.  Could is isinstanc(el_text, float) too
                        elif math.isnan(el_text):
                            print('this means nan float for thing')
                            pass

            # ABSTRACT
            try:
                abstract_new = df.loc[indice]['ABSTRACT']
                if isinstance(abstract_new, str):
                    if abstract is not None:
                        abstract.text = abstract_new
                    else:
                        abstract = ET.SubElement(dataIdInfo, 'idAbs')
                        abstract.text = abstract_new
                        # ET.dump(datIdInfo)
                        df.at[indice, 'ABSTRACT'] = ''
                elif math.isnan(abstract_new):
                    print('this means nan float for thing')
                    pass
            except KeyError:
                # no ABSTRACT col in csv
                pass
            # CREDITS
            # standard credits --> set col value to 'standard' in csv
            credits_stamp = 'Zachary Uhlmann\nMcMillen Jacobs\nuhlmann@mcmjac.com'
            try:
                #   NEEDS WORK - doesn't erase existimng --> see RAMP_restoration_bdry
                credits_new = df.loc[indice]['CREDITS']
                if isinstance(credits_new, str):
                    el = ET.SubElement(dataIdInfo, 'idCredit')
                    # stamp with standard credits or use specific
                    if credits_new == 'standard':
                        credits_new = copy.copy(credits_stamp)
                    else:
                        pass
                    el.text = credits_new
                    df.at[indice, 'CREDITS'] = ''
                elif math.isnan(credits_new):
                    print('this means nan float for thing')
                    pass
            except KeyError:
                # No CREDITS col in csv
                pass

            # for standalone xmp in shapefile --> this is all you need
            tree.write(fp_xml)
            # if added/subtracted purp then lines removed
            setattr(self, df_str, df)
            # additional step for fcs in gdb
            if not shp:
                # copy new metadata
                src_template_md = arcpy.metadata.Metadata(fp_xml)
                # apply to fcs (tgt)
                tgt_item_md.copy(src_template_md)
                tgt_item_md.save()

    def quickie_inventory(self, df_str, target_col = 'DATA_LOCATION_MCMILLEN_JACOBS',
                        shp = False, standard_credits = True, **kwargs):
        '''
        quick grab item description to add to new csv for the gang.  ZRU 20201207
        updated (slightly 5/11/2021) for functionality with feature classes.
        ARGUMENTS
        df_str              string of datatrame to getattr
        target_col          data location column
        shp                 True or False.  Nowadays (May 2021) most likely fcs
                            not shapefiles
        standard_credits    use same credits throughout.  Saves cut and pasting
                            credits in spreadsheet
        '''

        # FIND file paths to xmls of shapefiles FIGURE OUT FOR GDB
        df = getattr(self, df_str)
        fp_base = df.loc[self.indices][target_col].tolist()
        index_names = df.loc[self.indices].index.to_list()
        print(index_names)

        # initiate lists
        purp_list = []
        abstract_list = []
        credits_list = []

        # If standard credits stamp
        credits_stamp = 'Zachary Uhlmann\nMcMillen Jacobs\nuhlmann@mcmjac.com'
        # If feature classes
        if not shp:
            for indice in self.indices:
                fp_fcs = df.loc[indice][target_col]
                tgt_item_md = arcpy.metadata.Metadata(fp_fcs)
                purp_list.append(tgt_item_md.summary)
                abstract_list.append(tgt_item_md.description)
                if standard_credits:
                    credits = credits_stamp
                else:
                    credits = tgt_item_md.credits
                credits_list.append(credits)

        #If SHAPEFILE ---> relic
        else:
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

        # EXPORT INVENTORY
        df_quick_inventory = pd.DataFrame(np.column_stack(
                                [index_names, purp_list, abstract_list, credits_list]),
                                columns = ['feature_name', 'purpose', 'abstract', 'credits'])
        fp_out = r'C:\Users\uhlmann\Box\GIS\Project_Based\Klamath_River_Renewal_MJA\GIS_Data\compare_vers\database_contents\master_gdb\\agol_master_gdb_assessmen_2021c.csv'
        pd.DataFrame.to_csv(df_quick_inventory, fp_out)

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

        self.create_base_properties(df_str)

        # # set path to archive for later archiving
        # # 1) create object name or archive csv path
        # str_csv_archive_obj = 'fp_csv_archive_{}'.format(df_base_str)
        #
        # # 2) create path to csv to save to object
        # fp_csv_archive = '{}_archive_{}.csv'.format(os.path.splitext(fp_csv)[0], self.todays_date)
        # setattr(self, str_csv_archive_obj, fp_csv_archive)

    def take_action(self, df_str, action_type,
                    target_col = 'DATA_LOCATION_MCMILLEN_JACOBS',
                    dry_run = False, replace_action = '', save_df = False, **kwargs):
        '''
        Move has no checks for if the index_col == fcs name.  If it's an integer,
        that's what the new feature name will save out as.
        ARGUMENTS
        df_str          access dataframe from object (self)
        action_type     phase this out one day, but for now only ONE action at a time (ZU 20210815)
                        move and copy housed under one if/else.
                        rename and delete are standalone for now
        target_col      location of source FCS to performa ction on
        dry_run         True or False.  If True, then DONT copy, move or log Makeshift
                        functionality to populate dataframe i.e. DATA_LOCATION...
        replace_action  either set as empty string "''" or new string if for instance
                        intention is to perform another action sequentially on the
                        same indices

        '''

        # load dataframe
        df = getattr(self, df_str)

        # archive before deleting - this saves an archive csv
        self.save_archive_csv(df_str)

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

        lookup_table = copy.copy(self.lookup_table)
        # if gdb not in viable subproject, then add to poo poo platter
        project_str = lookup_table[lookup_table.subproject == self.subproject_str].project.values[0]
        lookup_table_project = lookup_table[lookup_table['project']==project_str]
        # standdard stuff
        viable_gdbs = lookup_table_project.index.to_list()
        inventory_dir = lookup_table_project.inventory_dir.to_list()[0]

        if action_type == 'delete':
            logging.info('DELETING FEATURES:')
            for index in self.indices:
                fp_fcs_current = os.path.normpath(df.loc[index][target_col])
                if arcpy.Exists(fp_fcs_current):
                    logging.info(fp_fcs_current)
                    try:
                        arcpy.Delete_management(fp_fcs_current)
                        df.drop(index, inplace = True)
                        setattr(self, df_str, df)

                        # UPDATE SOURCE inventory
                        # ABSTRACT into FUNCTION someday 20210819 ZU
                        fp_components = fp_fcs_current.split(os.sep)
                        for idx, comp in enumerate(fp_components):
                            if '.gdb' in comp:
                                # Get Source STR
                                src_gdb_or_dir_str = '{}_gdb'.format(comp[:-4])
                                if src_gdb_or_dir_str in viable_gdbs:
                                    standalone = False
                                else:
                                    standalone = True
                                # Once gdb is found in path, then break
                                break
                            # translation - there was no gdb in fp_fcs_orig
                            elif idx == (len(fp_components) - 1):
                                # No gdb found == shapefile passed - use dir/folder
                                standalone = True
                        if not standalone:
                            fp_csv_source = lookup_table.loc[src_gdb_or_dir_str, 'fp_csv']
                            df_str_source = lookup_table.loc[src_gdb_or_dir_str, 'df_str']
                        else:
                            # clunky way of grabbing any inventory dir value
                            fname_csv = '{}_standalone_data_inventory.csv'.format(self.project_str)
                            fp_csv_source = os.path.join(inventory_dir, fname_csv)
                            df_str_source = 'df_{}_standalone'.format(self.project_str)

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
                        df_source.drop(index, inplace = True)
                        setattr(self, df_str_source, df_source)

                    except Exception as e:
                        logging.info(e)
                else:
                    logging.info('feature with ACTION == delete does not exist\n:{}'.format(index))

        elif action_type in ['rename']:
            for index in self.indices:
                print('did we make it here?')
                df_item = df.loc[index]
                fp_fcs_current = os.path.normpath(df_item[target_col])
                # create new filename components
                fc_new_name = df_item['RENAME']
                col_name_original = df_item['COL_NAME_ARCHIVAL']
                col_name_original = dict_col_name_orig[col_name_original]
                fp_components = fp_fcs_current.split(os.sep)
                # all but original file name
                fp_base = os.sep.join(fp_components[:-1])
                # full path to new fcs
                fp_fcs_new = os.path.join(fp_base, fc_new_name)

                # NEW COL VALUES
                df.at[index, target_col] = fp_fcs_new.replace(os.sep, '//')
                df.at[index, col_name_original] = fp_fcs_current.replace(os.sep, '//')
                df.at[index, 'ACTION'] = ''
                df.at[index, 'RENAME'] = ''

                msg_str = '\nRENAMING: {}\nTO:        {}'.format(fp_fcs_current, fp_fcs_new)
                arcpy.Rename_management(fp_fcs_current, fp_fcs_new)
                # Now fp is renamed, so change alias on NEW fcs
                arcpy.AlterAliasName(fp_fcs_new, fc_new_name)

                # RENAME label
                df = df.rename(index = {index:fc_new_name})
                setattr(self, df_str, df)

                # UPDATE SOURCE inventory
                # ABSTRACT into FUNCTION someday 20210819 ZU
                fp_components = fp_fcs_current.split(os.sep)
                for idx, comp in enumerate(fp_components):
                    if '.gdb' in comp:
                        # Get Source STR
                        src_gdb_or_dir_str = '{}_gdb'.format(comp[:-4])
                        if src_gdb_or_dir_str in viable_gdbs:
                            standalone = False
                        else:
                            standalone = True
                        # Once gdb is found in path, then break
                        break
                    # translation - there was no gdb in fp_fcs_orig
                    elif idx == (len(fp_components) - 1):
                        # No gdb found == shapefile passed - use dir/folder
                        standalone = True
                if not standalone:
                    fname_csv = lookup_table.loc[src_gdb_or_dir_str, 'fname_csv']
                    fp_csv_source = os.path.join(inventory_dir, fname_csv)
                    df_str_source = lookup_table.loc[src_gdb_or_dir_str, 'df_str']
                else:
                    # clunky way of grabbing any inventory dir value
                    fname_csv = '{}_standalone_data_inventory.csv'.format(self.project_str)
                    fp_csv_source = os.path.join(inventory_dir, fname_csv)
                    df_str_source = 'df_{}_standalone'.format(self.project_str)

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
                df_source.at[index, target_col] = fp_fcs_new.replace(os.sep, '//')
                df_source.at[index, col_name_original] = fp_fcs_current.replace(os.sep, '//')
                setattr(self, df_str_source, df_source)

                print(msg_str)
                logging.info(msg_str)

        elif action_type in ['move','copy']:

            for index in self.indices:
                df_item = df.loc[index]
                fp_fcs_current = os.path.normpath(df_item[target_col])
                fp_move = os.path.normpath(self.lookup_table.loc[df_item['MOVE_LOCATION'], 'fp_gdb'])
                dset_move = df_item['MOVE_LOCATION_DSET']
                fc_new_name = df_item['RENAME']
                notes = df_item['NOTES']

                # DETERMINE DSET
                rename_delete_protocol = False
                fp_components = fp_fcs_current.split(os.sep)
                for idx, comp in enumerate(fp_components):
                    if '.gdb' in comp:
                        fp_gdb_orig = os.sep.join(fp_components[:idx+1])
                        dset_orig = fp_components[idx + 1]
                        # annoying realitey - same gdb cannot have features with the same name
                        # even in diff dsets.;
                        if fp_gdb_orig == fp_move:
                            rename_delete_protocol = True
                        # get the original dataset as the default with no dset
                        # provided for move is use original in new gdb
                        if pd.isnull(dset_move):
                            # in this case, rename_delete_protocol will remain FALSE
                            dset_move = dset_orig

                        # Get Source STR
                        src_gdb_or_dir_str = '{}_gdb'.format(comp[:-4])

                        if src_gdb_or_dir_str in viable_gdbs:
                            standalone = False
                        else:
                            standalone = True
                        # Once gdb is found in path, then break
                        break
                    # translation - there was no gdb in fp_fcs_orig
                    elif idx == (len(fp_components) - 1):
                        # No gdb found == shapefile passed - use dir/folder
                        standalone = True
                if not standalone:
                    fname_csv = lookup_table.loc[src_gdb_or_dir_str, 'fname_csv']
                    fp_csv_source = os.path.join(inventory_dir, fname_csv)
                    df_str_source = lookup_table.loc[src_gdb_or_dir_str, 'df_str']
                else:
                    # clunky way of grabbing any inventory dir value
                    fname_csv = '{}_standalone_data_inventory.csv'.format(self.project_str)
                    fp_csv_source = os.path.join(inventory_dir, fname_csv)
                    df_str_source = 'df_{}_standalone'.format(self.project_str)

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

                fname_csv = lookup_table.loc[tgt_gdb_or_dir_str, 'fname_csv']
                fp_csv_target = os.path.join(inventory_dir, fname_csv)
                df_str_target = lookup_table.loc[tgt_gdb_or_dir_str, 'df_str']
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

                    df.at[index, 'DATA_LOCATION_MCMILLEN_JACOBS'] = fp_fcs_new.replace(os.sep, '//')
                    df.at[index, 'ACTION'] = ''
                    df.at[index, 'MOVE_LOCATION'] = ''
                    df.at[index, 'MOVE_LOCATION_DSET'] = ''
                    if update_label:
                        df = df.rename(index = {index:feat_name})
                    # TARGET DF UPDATES
                    # Assemble Series to append to Master DF
                    print('did we make it here above the append')

                    # To document whether fp_fcs_current = Staging, Previous, Original
                    col_name_original = df_item['COL_NAME_ARCHIVAL']
                    if not pd.isnull(col_name_original):
                        col_name_original = dict_col_name_orig[col_name_original]
                        df.at[index, col_name_original] = fp_fcs_current.replace(os.sep, '//')
                        d = {col_name_original: fp_fcs_current.replace(os.sep, '//'),
                            'FEATURE_DATASET':dset_move,
                            'DATA_LOCATION_MCMILLEN_JACOBS':fp_fcs_new.replace(os.sep, ''),
                            'NOTES_APPEND':notes}
                        ser_append = pd.Series(data = d,
                                     index = [col_name_original, 'FEATURE_DATASET',
                                            'DATA_LOCATION_MCMILLEN_JACOBS','NOTES_APPEND'],
                                     name = feat_name)
                    # If we don't want to document COL_NAME_ARCHIVAL.  i.e. mistakenly added
                    # to master, and now decide to move back to archival.
                    else:
                        d = {'FEATURE_DATASET':dset_move,
                            'DATA_LOCATION_MCMILLEN_JACOBS':fp_fcs_new.replace(os.sep, '//'),
                            'NOTES_APPEND':notes}
                        ser_append = pd.Series(data = d,
                                     index = ['FEATURE_DATASET',
                                            'DATA_LOCATION_MCMILLEN_JACOBS','NOTES_APPEND'],
                                     name = feat_name)

                    # append new row from Series
                    df_target = df_target.append(ser_append)
                    if update_label:
                        df_target = df_target.rename(index = {index:feat_name})
                    print('now lets set attribute')
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
        else:
            if action_type in  ['create_poly', 'create_line', 'create_point']:
                # For adding new item to maestro and take_action(action_type = create_<type>...)
                for index in self.indices:
                    df_item = df.loc[index]
                    tgt_gdb_or_dir_str = df_item['MOVE_LOCATION']
                    dir_gdb = lookup_table.loc[src_gdb_or_dir_str, fp_gdb]
                    dset = df_item['MOVE_LOCATION_DSET']
                    if not math.isnan(dset):
                        dir_gdb = os.path.join(dir_gdb, dset)
                    feat_type_dict = {'create_poly': 'POLYGON', 'create_line':'POLYLINE',
                                        'create_point':'POINT'}
                    feat_type = feat_type_dict[action_type]
                    fp_fcs = os.path.join(dir_gdb, index)
                    msg_str = '\nCreating {} FC: {} in location:\n{}'.format(feat_type, index, fp_fcs)
                    print(msg_str)
                    # flag_index
                    arcpy.CreateFeatureclass_management(dir_gdb, index, feat_type,
                                                        spatial_reference = self.prj_file,
                                                        has_m = 'No', has_z = 'No')
                    # NEW COL VALUES
                    df.at[index, target_col] = fp_fcs.replace(os.sep, '//')
                    df.at[index, 'ACTION'] = ''
                    df.at[index, 'MOVE_LOCATION'] = ''
                    df.at[index, 'MOVE_LOCATION_DSET'] = ''
                    setattr(self, df_str, df)

                    logging.info(msg_str)
            elif action_type in ['fc_to_fc_conv']:
                var_dict = kwargs['var_dict']
                fp_in = var_dict['feat_in']
                out_loc = var_dict['out_loc']
                feat_name = var_dict['fname_out']
                try:
                    dset = var_dict['out_dset']
                    out_loc = os.path.join(out_loc, dset)
                except KeyError:
                    pass

                msg_str = 'FC to FC conversion: \n'
                msg_str = '{}  FEAT_IN:   ---  {}\n'.format(msg_str, fp_in)
                msg_str = '{}  OUT_LOC:   ---  {}\n'.format(msg_str, out_loc)
                msg_str = '{}  FEAT_NAME: ---  {}\n'.format(msg_str, feat_name)
                if not dry_run:
                    arcpy.FeatureClassToFeatureClass_conversion(fp_in, out_loc, feat_name)
                    logging.info(msg_str)

            # documentation to add to table
            notes = kwargs['new_fc_notes']
            fp_fcs = os.path.join(out_loc, feat_name)
            d = {'DATE_CREATED':self.todays_date,
                'DATA_LOCATION_MCMILLEN_JACOBS':fp_fcs.replace(os.sep, '//'),
                'NOTES':notes}
            ser_append = pd.Series(data = d,
                         index = ['DATE_CREATED',
                                'DATA_LOCATION_MCMILLEN_JACOBS','NOTES'],
                         name = feat_name)

            # Get TARGET DF/CSV/STR
            fp_components = fp_fcs.split(os.sep)
            for idx, comp in enumerate(fp_components):
                if '.gdb' in comp:
                    # Get Source STR
                    tgt_gdb_or_dir_str = '{}_gdb'.format(comp[:-4])

                    if tgt_gdb_or_dir_str in viable_gdbs:
                        standalone = False
                    else:
                        standalone = True
                    # Once gdb is found in path, then break
                    break
                # translation - there was no gdb in fp_fcs_orig
                elif idx == (len(fp_components) - 1):
                    # No gdb found == shapefile passed - use dir/folder
                    standalone = True
            if not standalone:
                fname_csv = lookup_table.loc[tgt_gdb_or_dir_str, 'fname_csv']
                fp_csv_target = os.path.join(inventory_dir, fname_csv)
                df_str_target = lookup_table.loc[tgt_gdb_or_dir_str, 'df_str']
            else:
                # clunky way of grabbing any inventory dir value
                fname_csv = '{}_standalone_data_inventory.csv'.format(self.project_str)
                fp_csv_target = os.path.join(inventory_dir, fname_csv)
                df_str_target = 'df_{}_standalone'.format(self.project_str)

            # Only grabs TargetGDB once per gdb
            try:
                df_target = getattr(self, df_str_target)
            # if dataframe NOT already added via self.add_df
            except AttributeError:
                print('populating target')
                # note this also creates fp_csv_archive
                self.add_df(fp_csv_target, df_str_target, 'ITEM')
                df_target = getattr(self, df_str_target)

            df_target = df_target.append(ser_append)
            df = df.append(ser_append)
            setattr(self, df_str_target, df_target)
            setattr(self, df_str, df)
            if save_df:
                pd.DataFrame.to_csv(df, getattr(self, 'fp_csv'))
                pd.DataFrame.to_csv(df_target, fp_csv_target)


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
    def mark_duplicate_rows(self, df_str, target_col, ispath = False):
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
        if ispath:
            target_lst = [os.path.realpath(item) for item in target_lst]
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
    def replace_indices(self, df_str, **kwargs):
        '''
        For dataframes from csv with no value (math.nan) from pd.DataFrame.read_csv
        due to...no values in csv.  This version requires user to set indices
        using self.selection_idx.  Additionally, this version is simply for standalone
        shapefiles or feature classes (i.e. not within gdb) and takes name automatically
        from base filename.  ZRU 04/05/2021
        ARGS
        df_str          i.e. df_working
        '''
        df = getattr(self, df_str)
        try:
            kwargs['shapefile']
            orig_index = df.index.to_list()
            indices_iloc = self.indices_iloc
            fp_fcs = df.iloc[indices_iloc].DATA_LOCATION_MCMILLEN_JACOBS.to_list()
            print(fp_fcs)
            # flag_index
            # example of zip syntax for indices_iloc
            for idx, item in zip(indices_iloc, fp_fcs):
                path, ext = os.path.splitext(item)
                new_indice = os.path.split(path)[-1]
                print('replaceing with {}'.format(new_indice))
                orig_index[idx] = new_indice
            df.index = orig_index
            setattr(self, df_str, df)
        except KeyError:
            print('did it pass')
            pass
    def create_base_properties(self, df_str):
        '''
        adds base properties for dataframes such as fp_csv and fp_log
        PROPERTIES
        fp_csv_archive      the base archive which will be overwritten if one day
                            old.  This assumes Box will have a backup in the cloud.
                            fp_csv_archive_temp will be a temp archive in case daily
                            changes need to be flipped back in event of accident
        fp_csv_archive_temp As mentioned above, used for daily backup.  Will be deleted
                            later.
        fp_log_prop         file path to log file
        '''

        if df_str == 'df':
            fp_csv_prop_str = 'fp_csv'
            fp_csv_archive_prop_str = 'fp_csv_archive'
            fp_csv_archive_temp_prop_str = 'fp_csv_archive_temp'
            fp_log_prop_str = 'fp_log'
        else:
            df_base_str = df_str.replace('df_', '')
            fp_csv_prop_str = 'fp_csv_{}'.format(df_base_str)
            fp_csv_archive_prop_str = 'fp_csv_archive_{}'.format(df_base_str)
            fp_csv_archive_temp_prop_str = 'fp_csv_archive_temp_{}'.format(df_base_str)
            fp_log_prop_str = 'fp_log_{}'.format(df_base_str)

        fp_csv = getattr(self, fp_csv_prop_str)
        basepath = os.path.splitext(fp_csv)[0]
        setattr(self, fp_csv_archive_prop_str, '{}_archive.csv'.format(basepath))
        setattr(self, fp_csv_archive_temp_prop_str, '{}_archive_{}.csv'.format(basepath, self.todays_date))
        fp_log = '{}_logfile.log'.format(basepath)
        setattr(self, fp_log_prop_str, fp_log)

    def save_archive_csv(self, df_str):

        if df_str == 'df':
            # if df
            str_csv_archive_obj = 'fp_csv_archive'
            str_csv_archive_temp_obj = 'fp_csv_archive_temp'
        else:
            # strip away the df_
            df_base_str = df_str.replace('df_', '')
            str_csv_archive_obj = 'fp_csv_archive_{}'.format(df_base_str)
            str_csv_archive_temp_obj = 'fp_csv_archive_temp_{}'.format(df_base_str)

        # 2) path to csv archive
        fp_csv_archive = getattr(self, str_csv_archive_obj)
        fp_csv_archive_temp = getattr(self, str_csv_archive_temp_obj)

        # create archive if first time managing database
        if not os.path.exists(fp_csv_archive):
            # initiate archive file for day
            print('save an archive:\n{}'.format(fp_csv_archive))
            pd.DataFrame.to_csv(getattr(self, df_str), fp_csv_archive)

        if not os.path.exists(fp_csv_archive_temp):
            print('save a time stamped archive:\n{}'.format(fp_csv_archive_temp))
            # determine if temporary archive is necessary
            pd.DataFrame.to_csv(getattr(self, df_str, fp_csv_archive_temp))

        # # perhaps useful later for cleanup?
        # date_str = os.path.split(fp_csv_archive_temp)[-1][-12:-4]
        # date_obj = datetime.date(int(date_str[:4]), int(date_str[4:6]), int(date_str[6:]))

    def cast_columns(self, df_str):
        '''
        basic funciton to convert columns to specific datatypes
        '''
        df = getattr(self, df_str)
        col_names = df.columns
        if 'visible' in col_names:
            boolean_key = {'visible':{'TRUE':True,'FALSE':False} }
            df = df.replace(boolean_key)
        if 'duplicate' in col_names:
            df['duplicate'] = pd.to_numeric(df['duplicate'])
        setattr(self, df_str, df)

    def retain_visible(self, df_str_source, df_str_target, match_col_list, replace_col_target):
        '''
        Should transfer a value of 'retain' to rows in match_col_target (match_col_list[1])
        of target df where the source data of visible layers in mxds reside.
        For instance Project Action Layer in upperset.mxd visible = True, therefore
        the corresponding datasource fp/to/gdb/project_action_bdry2 will be
        set to a value of 'retain' in the replace_col_target. 202105

        df_str_target           string of dataframe to add values to based off other arguments
        df_str_source           string of dataframe to transfer values from
        match_col_list          columns to match from table to table [col_source_str, col_target_str]
                                i.e. fp_feat, DATA_LOCATION_MCMILLEN_JACOBS
        replace_col_target      column where we add tag / val
        '''
        # STRING to NUMBERIC!!
        # https://stackoverflow.com/questions/15891038/change-column-type-in-pandas
        df_source = getattr(self, df_str_source)
        df_str_working_target = '{}_matched'.format(df_str_target)
        try:
            # already working, add to working
            df_target = getattr(self, df_str_working_target)
            print('it existed')
        except AttributeError:
            # no action yet, add to original
            print('did not exist')
            df_target = getattr(self, df_str_target)
        match_col_source = match_col_list[0]
        match_col_target = match_col_list[1]
        df_working = df_source[df_source.visible == True]
        # previous method for removing duplicates BUT treated NAs as duplicate group candidate
        # df_working = df_working.drop_duplicates(subset = ['duplicate'], keep = 'first')
        # this solution worked
        df_working = df_working[~df_working['duplicate'].duplicated() | df_working['duplicate'].isna()]
        pd.DataFrame.to_csv(df_working, 'c:/Users/uhlmann/Documents/temp.csv')
        # should be list of file paths to fcs
        vals_match = df_working[match_col_source].to_list()
        target_indices = [df_target.index[df_target[match_col_target]==val] for val in vals_match]
        # add "retain" to field
        for indice in target_indices:
            df_target.at[indice, replace_col_target] = 'retain'

        setattr(self, df_str_working_target, df_target)

    def df_to_df_transfer(self, df_str_source, df_str_target, match_col_list, replace_col_list, target_val):
        '''
        More for manual transfers.
        df_str_target           string of dataframe to add values to based off other arguments
        df_str_source           string of dataframe to transfer values from
        match_col_list          columns to match from table to table [col_source_str, col_target_str]
        target_col_list        confusingly TARGET i.e. col we are searching for value in df_source and
                                col where we are replacing in target
        target_val              val to search for in replace_col
        '''

        df_source = getattr(self, df_str_source)
        df_str_working_target = '{}_matched'.format(df_str_target)
        try:
            # already working, add to working
            df_target = getattr(self, df_str_working_target)
            print('it existed')
        except AttributeError:
            # no action yet, add to original
            print('did not exist')
            df_target = getattr(self, df_str_target)
        match_col_source = match_col_list[0]
        match_col_target = match_col_list[1]
        replace_col_source = replace_col_list[0]
        replace_col_target = replace_col_list[1]
        # indices that match target_val in source
        source_indices = df_source.index[df_source[replace_col_source]==target_val]
        # file paths most likely
        vals_match = df_source.loc[source_indices][match_col_source].to_list()
        # indices in df_target matching source indices


        target_indices = [df_target.index[df_target[match_col_target]==val] for val in vals_match]

        for indice in target_indices:
            df_target.at[indice, replace_col_target] = target_val
        setattr(self, '{}_matched'.format(df_str_target), df_target)

class AgolAccess(metaData):
    '''
    Basic init for AGOL access
    '''

    def __init__(self, credentials, fp_csv = r'C:\Users\uhlmann\Box\GIS\Project_Based\Klamath_River_Renewal_MJA\GIS_Data\data_inventory_and_tracking\database_contents\item_descriptions.csv'):
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
        # FOUND NO difference between feature layer collection and feature layer.  All feature layers were
        # detected as both with mcmjac_gis.content.search(item_type = <collection or layer>)
        self.item_type_dict = {'shapefile': 'Shapefile', 'feature': 'Feature Layer Collection', 'feature2': 'Feature Layer'}
        group_id_dict = {'KRRP_Geospatial': 'a6384c0909384a43bfd91f5d9723912b',
                        'klamath_river_test': '01b12361c9e54386a955ba6e3279b09'}
        self.group_id_dict = group_id_dict

    def get_group(self, group_key):
        '''
        hardcoded. update if more groups become necessary.
        DELETE ZU 20210827
        '''
        group_id_dict = {'krrp_geospatial': 'a6384c0909384a43bfd91f5d9723912b',
                        'klamath_river_test': '01b12361c9e54386a955ba6e3279b09'}
        group_id = group_id_dict[group_key]
        krrp_geospatial = Group(getattr(self, 'mcmjac_gis'), group_id)
        setattr(self, group_key, krrp_geospatial)

    def identify_items_online(self, itemType=['feature'],
                                group_name ='KRRP_Geospatial', **kwargs):
        '''
        find items already online
        ARGS
        itemType:           list with matching keys (lower case) to item_type_dict
        group_name:         exact name as group in AGOL
        '''
        # List should be passed
        if isinstance(itemType, list):
            pass
        else:
            itemType = [itemType]

        # QUERY STRING
        # If Group (default KRRC_Geospatial), add to query str
        if group_name is not None:
            group_id = self.group_id_dict[group_name]
            query_str = 'owner: uhlmann@mcmjac.com AND group:{}'.format(group_id)
        else:
            query_str = 'owner: uhlmann@mcmjac.com'

        # GET ITEMS
        for item in itemType:
            itemType = self.item_type_dict[item]
            itemType_str = itemType.replace(' ', '_').lower()

            # TAGS  --> filter
            try:
                tag = kwargs['tag']
                items_filtered = [item for item in items if tag in item.tags]
                # format text for attribute to replace spaces with underSc
                tag_substr = 'tagged_{}'.format(tag)
            except KeyError:
                tag_substr = ''
                pass

            # Set Content_Str
            if group_name is None:
                content_str = 'user_content_{}{}'.format(itemType_str, tag_substr)
            else:
                content_str = 'user_content_{}_{}'.format(group_name, itemType_str, tag_substr)

            # GET CONTENT
            print(query_str)
            print(itemType)
            print(content_str)
            items = self.mcmjac_gis.content.search(query_str,
                                            item_type = itemType, max_items = 250)
            setattr(self, content_str, items)
            # filtered tags attribute

    def take_action_agol(self, df_str, action_type, user_content_str,
                            group = 'KRRP_Geospatial', **kwargs):
        '''
        perform applicable actions from action column. ZU 202102025.  Thus far
        only for remove.  will add others and perhaps a log for each run.
        #
        ARGS
        user_content_str        property from identify_objects_online method
                                ex. user_content_feature_layer_collection_krrp_geospatial
        action_type             thus far just 'remove' but need to add 'tags', publish
                                and 'share'
        group                   Group to use with multiple action types - Share,
                                share_status.  More suitable as a kwarg since
                                only applicable with a couple action types, but
                                seemed best. ZU 20210701
        kwargs                  update_action --> ONLY kwarg option:
                                this will remove action val (string specified)
                                as val in key/val pair of kwarg update_aaction

        '''
        df = getattr(self, df_str)
        ct = 1
        # ACCESS AGOL items
        user_content = getattr(self, user_content_str)
        if action_type == 'agol_status':
            titles = [content_item.title for content_item in user_content]
            for indice in self.indices:
                if indice in titles:
                    df.at[indice, 'AGOL_STATUS'] = True
                    # print('TITLE:{}TYPE:{}'.format(title, type(title)))
                else:
                    df.at[indice, 'AGOL_STATUS'] = False

                # if we want to remove vals in ACTION col
                try:
                    col_val = kwargs['update_action']
                    df = update_comma_sep_vals(df, title, 'ACTION', col_val)
                except:
                    pass
        if action_type == 'share_status':
            substr = group.replace('-','_').replace(' ','_').lower()
            group_str = 'user_content_feature_layer_collection_{}'.format(substr)
            user_content_group = getattr(self, group_str)
            list1 = copy.copy(self.indices)
            list2 = [item.title for item in user_content_group]
            set1 = set(list1)
            set2 = set(list2)
            df1_present_df2_absent = set1.difference(set2)
            # To add someday for content in Group NOT owned by uhlmann@mcmjac.com
            df2_present_df1_absent = set2.difference(set1)
            # SET all to True then REPLACE with False
            for indice in self.indices:
                df.at[indice, 'SHARED_GROUP'] = True
            # REPLACE with False
            for indice in list(df1_present_df2_absent):
                df.at[indice, 'SHARED_GROUP'] = False
        if action_type == 'publish_status':
            user_content_shp = getattr(self, 'user_content_shapefile')
            user_content_feat = getattr(self, 'user_content_feature_layer_collection')
            list1 = [item.title for item in user_content_shp]
            list2 = [item.title for item in user_content_feat]
            set1, set2 = set(list1), set(list2)
            not_published = list(set1.difference(set2))
            # SET all to True then REPLACE with False
            for indice in self.indices:
                df.at[indice, 'PUBLISHED'] = False
            # REPLACE with False
            for indice in not_published:
                df.at[indice, 'PUBLISHED'] = False

        if action_type == 'remove':
            for content_item in user_content:
                title = content_item.title
                if title in self.indices:
                    print('REMOVING: {}'.format(title))
                    content_item.delete()
                    # gets idx in df; assumes just ONE item with exact name -NOT > 1
                    # this is for useing ALTERNATE column - not INDEX
                    # idloc = (self.df_working.ITEM == title).idxmax()
                    # fancy method to value for action at idloc
                    # OFFLINE set status to offline
                    df.at[title, 'AGOL_STATUS'] = False

                # if we want to remove vals in ACTION col
                try:
                    col_val = kwargs['update_action']
                    df = update_comma_sep_vals(df, title, 'ACTION', col_val)
                except:
                    pass

        if action_type == 'publish':
            for content_item in user_content:
                title = content_item.title
                if title in self.indices:
                    print('PUBLISHING: {}'.format(title))
                    content_item.publish()
                else:
                    print('item title {} did not match queried result on agol --> did NOT publish'.format(title))
                # if we want to remove vals in ACTION col
                try:
                    col_val = kwargs['update_action']
                    df = update_comma_sep_vals(df, title, 'ACTION', col_val)
                except:
                    pass
        if action_type == 'share':
            # To account for any ITEMS from df that are NOT online as features
            indices_remaining = copy.copy(self.indices)
            # get group id for sharing
            try:
                getattr(self, 'krrp_geospatial')
            except AttributeError:
                self.get_group('krrp_geospatial')
            for content_item in user_content:
                title = content_item.title
                if title in self.indices:
                    print('SHARING: {}'.format(content_item))
                    content_item.share(groups = [self.krrp_geospatial], org = True)
                    df.at[title, 'SHARED_GROUP'] = True
                    indices_remaining.remove(title)
                else:
                    pass
                # if we want to remove vals in ACTION col
                try:
                    col_val = kwargs['update_action']
                    df = update_comma_sep_vals(df, indice, 'ACTION', col_val)
                except:
                    pass
            # Print out indices unaccounted for
            if len(indices_remaining)!=0:
                substr = '\n'.join(indices_remaining)
                print('\nINDICES NOT FOUND IN CONTENT:\n{}'.format(substr))
        if action_type == 'current_tags':
            for content_item in user_content:
                item_title = content_item.title
                item_tags = content_item.tags
                tags_str = ', '.join(item_tags)
                try:
                    df.at[item_title, 'TAGS_CURRENT'] = tags_str
                except KeyError:
                    print('Item {} is not present in DF'.format(item_title))
        if action_type == 'update_tags':
            content_items = [item for item in user_content if item.title in self.indices]
            for content_item in content_items:
                title = content_item.title
                try:
                    new_tags = df.loc[title, 'TAGS']
                    # Get list from string
                    new_tags = ductape_utilities.parse_csl(new_tags, False)
                    update_dict = {'tags':new_tags}
                    log_str = 'TAGS update for: {}'.format(title)
                    content_item.update(update_dict)
                except KeyError:
                    print('Item {} is not present in DF'.format(item_title))

        # keep count going for item_type
        ct += 1
        setattr(self, df_str, df)

    def update_comma_sep_vals(self, df, index, col_name, col_val):
        # UPDATE comma-sep list
        initial_vals = df.at[index, col_name]
        # basically parse comma separated While removing spaces
        updated_vals = [vals.strip(' ') for vals in initial_vals.split(',')]
        # remove tag
        try:
            updated_vals.remove(col_val)
        except ValueError:
            # most likely looped through once and already removed
            pass
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
        df.at[index, 'ACTION'] = updated_vals
        return(df)

    def add_agol_upload(self, df_str, target_col = 'AGOL_DIR', **kwargs):
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
        indices_loc = [idx for idx in self.indices_iloc if self.df.iloc[idx][target_col] not in ignore_upload]

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
        upload_folders = self.df.loc[titles]['AGOL_DIR'].values.tolist()
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
            properties_dict = {'type':'Shapefile',
                                'title':titles[idx],
                                'tags':tags[idx],
                                'snippet':snippets[idx]}
            print('ADDING TO AGOL: \n{}'.format(shp))
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

class DbaseManagement(metaData):
    '''
    cleaning up gdbs
    '''

    def __init__(self, fp_csv = r'C:\Users\uhlmann\Box\GIS\Project_Based\Klamath_River_Renewal_MJA\GIS_Data\data_inventory_and_tracking\database_contents\item_descriptions.csv'):
        super().__init__(fp_csv)

    def flag_gdb_dset(self, df_str, target_col, flag_val, new_col_name = 'protect'):
        '''
        identify base paths or datasets within gdbs (via full fp) to protect from
        ANY deletion. ZRU 3/31/2021

        ARGS
        df_str                  for csv added during add_df
x`        target_col              name of column with fp or gdb path
        flag_val               gdb or subdirectory or dset to flag
        new_col_name            default == 'protect'.  This will serve as flag for
                                categorically disqualifying row for deletion.
        '''

        df = getattr(self, df_str)
        target_list = df[target_col].tolist()
        target_list = [os.path.realpath(item) for item in target_list]
        # populate new col if it doesn't exist
        # it will exist if run multiple times with different flag_vals
        if new_col_name not in df.columns:
            df[new_col_name] = False
        # get col idx for assigning values
        col_idx = df.columns.get_loc(new_col_name)
        for idx, fp in enumerate(target_list):
            for component in fp.split(os.sep):
                if flag_val == component:
                    # figure out how to set with iloc
                    df.iloc[idx, col_idx] = True
                    # break will only apply to inner loops
                    break

        setattr(self, df_str, df)

    def symmetric_diff_basic(self, df_str_source, source_col, df_str_target, target_col, mark_remove = True):
        # get dataframes
        df_source = getattr(self, df_str_source)
        df_target = getattr(self, df_str_target)

        # find overlapping values for action
        set_source = set(df_source[source_col].to_list())
        set_target = set(df_target[target_col].to_list())
        target_vals = list(set_target - set_source)

        if mark_remove:
            new_col_name = 'remove'
        else:
            new_col_name = 'protect'

        #probably unnecessary, but in case funciton run multiple times
        if new_col_name not in df_target.columns:
            df_target[new_col_name] = False

        for idx in list(range(len(df_target))):
            if df_target.loc[idx, target_col] in target_vals:
                df_target.loc[idx, new_col_name] = True
        setattr(self, df_str_target, df_target)


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
