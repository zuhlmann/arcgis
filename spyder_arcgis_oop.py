# ZRU 7/13/20
# To run this we need to be in arcgispro-py3 environment w/ GIS package:
# go to C:\\Program Files\\ArcGIS\\Pro\\bin\\Python\\Scripts and do: Start proenv.bat
# python2 to python3 compatability: https://pro.arcgis.com/en/pro-app/arcpy/get-started/python-migration-for-arcgis-pro.htm
# coding: utf-8

from __future__ import print_function, unicode_literals, absolute_import
import os, sys

from xarray.util.generate_ops import inplace

sys.path = [p for p in sys.path if '86' not in p]
from arcgis.gis import GIS
from arcgis.gis import Group
import glob
import copy
import pandas as pd
import numpy as np
import utilities
import datetime
import math
import xml.etree.ElementTree as ET
import arcpy
import logging
# note this protocol from here because debug was not writing to file
# https://stackoverflow.com/questions/31169540/python-logging-not-saving-to-file
from imp import reload
reload(logging)


class commonUtils(object):
    '''
    ARGS
    df_index_col            ITEM is default for use with Klamath.
    '''
    def __init__(self):
        pass
    def dbase_init(self,  prj_file, subproject_str, fp_csv_lookup, use_item_desc = False,
                df_str = 'df', df_index_col = 'ITEM'):
        '''
               KEYWORD ARGS:
               fill in now that reworked
               '''
        lookup_table = pd.read_csv(fp_csv_lookup, index_col='gdb_str', dtype='str', encoding="utf-8")
        setattr(self, 'lookup_table', lookup_table)
        # If item_desc kw, then use klamath maestro
        # eventually make submaestroe
        if use_item_desc:
            fp_csv = r'C:\Box\MCMGIS\Project_Based\Klamath_River_Renewal_MJA\GIS_Data\data_inventory_and_tracking\database_contents\item_descriptions.csv'
        else:
            fp_csv = lookup_table[lookup_table.subproject == subproject_str].fp_maestro_csv.values[0]
        df = pd.read_csv(fp_csv, index_col=df_index_col, na_values='NA', dtype='str', encoding="utf-8")
        setattr(self, 'subproject_str', subproject_str)
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
    def fcs_to_shp_agol_prep(self, df_str, target_col = 'DATA_LOCATION_MCMILLEN'):
        '''
        Created long time ago.  Edited for different workflow - i.e. pass indices
        for one here to fcs to fcs then zip in separate funcion which calls zipping utilities
        NEEDS TO incorporate offline_base ZU!! aug 2022

        ARGS:
        df_str              df for example
        target_col          col name for  col with file path to fcs for conversion
        '''
        arcpy.env.addOutputsToMap = False
        df = getattr(self, df_str)
        ct = 0
        for indice in self.indices:
            inDir = df.loc[indice, 'AGOL_DIR']
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

    def zip_shp_agol_prep(self, df_str, **kwargs):
        '''
        Created long time ago.  Edited for different workflow - i.e. pass indices
        for one fell swoop within function as opposed to calling within for loop.
        Also, convert fcs to shp AND zip in one fell swoop.  ZU 5/21/21

        ARGS:
        base_dir_shp:           path/to/dir/with/agol_Uploads/2020_10_05
        exclude_files:          take from self.indices --> string of shapefile name
                                to exclude from zipping (already zipped)
        '''

        df = getattr(self, df_str)
        yyyymmdd = datetime.datetime.today().strftime('%B %d %Y')

        inDir = list(set(self.df.loc[self.indices,'AGOL_DIR'].to_list()))
        for id in inDir:
            outDir = '{}_zip'.format(id)
            # ensure shp_dir does not already exist
            if not os.path.exists(outDir):
                os.mkdir(outDir)

            # 3) ZIP all Files at once
            try:
                # exclude files if already zipped
                exclude_files = kwargs['exclude_files']
                utilities.zipShapefilesInDir(id, outDir, exclude_files = exclude_files)
            except KeyError:
                utilities.zipShapefilesInDir(id, outDir)

    def zip_shp_agol_prep2(self, tc = 'DATA_LOCATION_MCMILLEN'):
        '''
        To zip all the indices.  If zipped exist already, they will be ignored.
        20220610
        '''
        for index in self.indices:
            fp_in = self.df.loc[index, tc]
            dir_out = self.df.loc[index, 'AGOL_DIR']
            shp_dir = os.path.join(dir_out, 'shp')
            zip_dir = os.path.join(dir_out, 'zip')
            for d in [shp_dir, zip_dir]:
                if not os.path.exists(d):
                    os.mkdir(d)
                else:
                    pass
            print('FC to FC: {}'.format(fp_in))
            arcpy.FeatureClassToFeatureClass_conversion(fp_in, shp_dir, index)
        # zip
        incl_files = copy.copy(self.indices)
        exist_file = [f[:-4] for f in os.listdir(shp_dir) if '.shp' in f]
        excl_files = list(set(exist_file) - set(incl_files))
        if len(excl_files)>0:
            utilities.zipShapefilesInDir(shp_dir, zip_dir, exclude_files = excl_files)
        else:
            utilities.zipShapefilesInDir(shp_dir, zip_dir)
    def zip_shp_dir(self, shp_dir, zip_dir, **kwargs):
        '''
        Manually pass shape and zip dir for decomposed version of above.  Need to tackle this shit.
        ZU 20230224
        Args:
            shp_dir:        path/to/shp/dir
            zip_dir:        path/to/zip/dir
            **kwargs        renamed_files - use case for data_share_inv if renaming from indices.
                            not awesome protocol

        Returns:

        '''

        try:
            incl_files = kwargs['renamed_files']
        except KeyError:
            incl_files = copy.copy(self.indices)
        exist_file = [f[:-4] for f in os.listdir(zip_dir)]
        excl_files = list(set(exist_file) - set(incl_files))
        if len(excl_files) > 0:
            print('here ', excl_files)
            utilities.zipShapefilesInDir(shp_dir, zip_dir, exclude_files=excl_files)
        else:
            utilities.zipShapefilesInDir(shp_dir, zip_dir)
            print('there')

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
            prop_str_indices = 'indices'
            prop_str_indices_iloc = 'indices_iloc'
        else:
            df_base_str = df_str.replace('df_','')
            prop_str_indices = '{}_indices'.format(df_base_str)
            prop_str_indices_iloc = '{}_indices_iloc'.format(df_base_str)
        try:
            target_tag = kwargs['target_tag']
            # list will be passed for multiple target tags
            if not isinstance(target_tag, list):
                target_tag = [target_tag]
            # pull tags column from df (list)
            parsed_list = self.parse_comma_sep_list('TAGS',oop=df_str)
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

            parsed_list = self.parse_comma_sep_list(fld,oop=df_str)

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
            setattr(self, prop_str_indices, df.iloc[iloc_action].index.tolist())
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
                setattr(self, prop_str_indices, df.iloc[indices].index.tolist())
                setattr(self, prop_str_indices_iloc, indices)
            # If indices were index_column vals (stirng)
            except ValueError:
                try:
                    setattr(self, prop_str_indices, df.iloc[indices].index.tolist())
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


    def parse_comma_sep_list(self, col_to_parse, **kwargs):
        '''
        takes string from tags column and parse into list of strings
        kwargs:         must be: oop or df.  oop=df_str, dframe= pandas dataframe
        '''
        try:
            df_str=kwargs['oop']
            df = getattr(self, df_str)
        except KeyError:
            pass
        try:
            df = kwargs['dframe']
        except KeyError:
            pass
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

    def write_xml(self, df_str, offline = True, **kwargs):

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

        if df_str == 'df':
            prop_str_fp_logfile = 'fp_log'
            prop_str_indices = 'indices'
            prop_str_indices_iloc = 'indices_iloc'
        else:
            df_base_str = df_str.replace('df_','')
            prop_str_fp_logfile = 'fp_log_{}'.format(df_base_str)
            prop_str_fp_csv = 'fp_csv_{}'.format(df_base_str)
            prop_str_indices = '{}_indices'.format(df_base_str)
            prop_str_indices_iloc = '{}_indices_iloc'.format(df_base_str)

        lookup_table = copy.copy(self.lookup_table)
        # if gdb not in viable subproject, then add to poo poo platter
        offline_csv = lookup_table[lookup_table.subproject == self.subproject_str].offline_lookup_table[0]
        olt = pd.read_csv(offline_csv, index_col = 'gdb_str')

        fp_logfile = getattr(self, prop_str_fp_logfile)

        # logging.basicConfig(filename = fp_logfile, level = logging.DEBUG)

        # Save call string to logfile
        banner = '    {}    '.format('-'*50)
        fct_call_str = 'Performing function write_xml'
        date_str = datetime.datetime.today().strftime('%D %H:%M')
        msg_str = '\n{}\n{}\n{}\n{}\n'.format(banner, date_str, banner, fct_call_str)
        # logging.info(msg_str)

        # key/val and key lists for add and subtract purpose list respectively
        add_new_purp_list = self.parse_comma_sep_list('ADD_LINES_PURP', oop=df_str)
        subtract_new_purp_list = self.parse_comma_sep_list('REMOVE_LINES_PURP',oop=df_str)

        indices = getattr(self, prop_str_indices)
        indices_iloc = getattr(self, prop_str_indices_iloc)
        for indice, indice_iloc in zip(indices, indices_iloc):
            fp_fcs = os.path.normpath(df.loc[indice]['DATA_LOCATION_MCMILLEN'])
            if os.path.splitext(fp_fcs)[-1]=='.shp':
                glob_string = '{}*.xml'.format(fp_fcs)
                # shapefile has xml
                try:
                    xml_created = False
                    fp_xml = glob.glob(glob_string)[0]
                # shapefile has no xml; will undergo same protocol as feature class in gdb
                except IndexError:
                    xml_created = True
                    fp_xml = arcpy.CreateScratchName('.xml', workspace=arcpy.env.scratchFolder)
                    # copy xml of feature class -- next up - update it
                    tgt_item_md = arcpy.metadata.Metadata(fp_fcs)
                    tgt_item_md.saveAsXML(fp_xml, 'EXACT_COPY')

            else:
                xml_created = True
                fp_fcs = os.path.normpath(df.loc[indice]['DATA_LOCATION_MCMILLEN'])
                fp_components = fp_fcs.split(os.sep)
                gdb_str = [v.replace('.','_') for v in fp_components if '.gdb' in v][0]
                offline_base = olt.loc[gdb_str, 'offline']
                online_base = olt.loc[gdb_str, 'online']
                if offline:
                    # https: // gfycat.com / honestanchoredesok
                    fp_fcs= fp_fcs.replace(online_base, offline_base)
                # For some reason, if fp does not exist then no error gets thrown
                # during xml process.  Debugging stinks then - ZU 20220914
                if not os.path.exists(fp_fcs):
                    msg_str_fp = 'PATH DOES NOT EXIST: \n{}'.format(fp_fcs)
                else:
                    pass

                tgt_item_md = arcpy.metadata.Metadata(fp_fcs)
                fp_xml = arcpy.CreateScratchName('.xml', workspace = arcpy.env.scratchFolder)
                # copy xml of feature class -- next up - update it
                tgt_item_md.saveAsXML(fp_xml, 'EXACT_COPY')

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
                fp_xml_template = r'C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\prj_files\xml_template_source.xml'
                print('\n{} contained no Item Desc - \nTemplate used instead: \n{}\n'.format(indice, fp_xml_template))
                tree = ET.parse(fp_xml_template)
                # root is the root ELEMENT of a tree
                root = tree.getroot()
                dataIdInfo = root.find('dataIdInfo')


            purp = dataIdInfo.find('idPurp')
            abstract = dataIdInfo.find('idAbs')
            credits = dataIdInfo.find('idCredit')

            # AGOL needs different path sep than PC. Change these columns
            # to AGOL format lower down
            file_path_columns = ['DATA_LOCATION_MCMILLEN',
                                'DATA_LOCATION_MCM_ORIGINAL',
                                'DATA_LOCATION_MCM_STAGING', 'AGOL_DIR']

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
                purp_item, purp_value = [], []
                for item in new_purp_items:
                    purp_item.append(item)
                    # value to add to Item Desc
                    val = df.loc[indice][item]
                    # if column contains a file path, format for agol
                    if item in file_path_columns:
                        # format file path to agol 2x forward slash
                        val = utilities.fix_fp(val, 'agol')
                    # Replace offline path with online path
                    if item == ('DATA_LOCATION_MCMILLEN'):
                        val = os.path.normpath(val)
                        try:
                            val = val.replace(offline_base, online_base)
                            print('WORKING : {}'.format(val))
                        except UnboundLocalError:
                            # no solution for offline_base / online_base for standalone shapefiles
                            pass
                    purp_value.append(val)

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

            if update_purp:
                element_text_list = [purpose_new]
                element_list = [purp]
                element_title = ['idPurp']

                if 'msg_str_fp' in locals():
                    msg_str = '{}\n\n{}'.format(msg_str_fp, msg_str)
                else:
                    pass

                # logging.info(msg_str)

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
                            # nan float thing
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
                elif math.isnan(abstract_new):
                    # nmn float thing
                    pass
            except KeyError:
                # no ABSTRACT col in csv
                pass
            # CREDITS
            # standard credits --> set col value to 'standard' in csv
            credits_stamp = 'Zachary Uhlmann\nMcMillen Corp\nuhlmann@mcmillencorp.com'
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

                elif math.isnan(credits_new):
                    #nan float thing
                    pass
            except KeyError:
                # No CREDITS col in csv
                pass

            # for standalone xmp in shapefile --> this is all you need
            tree.write(fp_xml)
            # if added/subtracted purp then lines removed
            setattr(self, df_str, df)

            # now remove all the lines
            df.at[indice, 'ADD_LINES_PURP'] = np.nan
            df.at[indice, 'REMOVE_LINES_PURP']=np.nan
            df.at[indice, 'ABSTRACT'] = np.nan
            df.at[indice, 'CREDITS'] = np.nan

            # additional step for fcs in gdb
            if xml_created:
                # copy new metadata
                src_template_md = arcpy.metadata.Metadata(fp_xml)
                # apply to fcs (tgt)
                tgt_item_md.copy(src_template_md)
                tgt_item_md.save()



    def quickie_inventory(self, df_str, target_col = 'DATA_LOCATION_MCMILLEN',
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
        credits_stamp = 'Zachary Uhlmann\nMcMillen Corp\nuhlmann@mcmillencorp.com'
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
            # to append DATA_LOCATION_MCMILLEN key/pair to Item Description
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
        df = pd.read_csv(fp_csv, index_col = index_field, na_values = 'NA')
        setattr(self, df_str, df)

        # save path to csv
        df_base_str = df_str.replace('df_', '')
        fp_csv_prop_str = 'fp_csv_{}'.format(df_base_str)
        setattr(self, fp_csv_prop_str, fp_csv)

        self.create_base_properties(df_str)

    def take_action(self, df_str, action_type,
                    target_col = 'DATA_LOCATION_MCMILLEN',
                    dry_run = False, replace_action = '', save_df = False,
                    **kwargs):
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


        arcpy.env.addOutputsToMap = False
        # load dataframe
        df = getattr(self, df_str)

        # archive before deleting - this saves an archive csv

        if df_str == 'df':
            prop_str_fp_logfile = 'fp_log'
            prop_str_indices = 'indices'
        else:
            df_base_str = df_str.replace('df_','')
            prop_str_fp_logfile = 'fp_log_{}'.format(df_base_str)
            prop_str_indices = '{}_indices'.format(df_base_str)

        fp_logfile = getattr(self, prop_str_fp_logfile)

        logging.basicConfig(filename = fp_logfile, level = logging.DEBUG)

        # Save call string to logfile
        banner = '    {}    '.format('-'*50)
        call_str = 'take_action({}, {}, target_col = {}):\n'.format(df_str, action_type, target_col)
        fct_call_str = 'Performing function called as:\n{}'.format(call_str)
        date_str = datetime.datetime.today().strftime('%D %H:%M')
        msg_str = '\n{}\n{}\n{}\n{}'.format(banner, date_str, banner, fct_call_str)
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

        csv = lookup_table_project[lookup_table_project.subproject == self.subproject_str].offline_lookup_table.values[0]
        olt = pd.read_csv(csv, index_col = 'gdb_str')
        indices = getattr(self, prop_str_indices)
        if action_type == 'delete':
            logging.info('DELETING FEATURES:')
            for index in indices:
                fp_fcs_current = os.path.normpath(df.loc[index][target_col])
                fp_components = fp_fcs_current.split(os.sep)
                if arcpy.Exists(fp_fcs_current):
                    logging.info(fp_fcs_current)
                    try:
                        if not dry_run:
                            arcpy.Delete_management(fp_fcs_current)
                        df.drop(index, inplace = True)
                        setattr(self, df_str, df)

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
                            inventory_dir = lookup_table.loc[src_gdb_or_dir_str, 'inventory_dir']
                            fp_csv_source = os.path.join(inventory_dir, fname_csv)
                            df_str_source = lookup_table.loc[src_gdb_or_dir_str, 'df_str']
                        else:
                            # clunky way of grabbing any inventory dir value
                            fp_csv_source = lookup_table[lookup_table.subproject == self.subproject_str].standalone_csv.values[0]
                            df_str_source = 'df_{}_standalone'.format(project_str)

                        # Only grabs TargetGDB once per gdb
                        try:
                            df_source = getattr(self, df_str_source)
                        # if dataframe NOT already added via self.add_df
                        except AttributeError:
                            print('populating source')
                            # note this also creates fp_csv_archive
                            self.add_df(fp_csv_source, df_str_source, 'ITEM')
                            df_source = getattr(self, df_str_source)
                        df_source.drop(index, inplace = True)
                        setattr(self, df_str_source, df_source)

                    except Exception as e:
                        logging.info(e)

                    # Save to DF
                    if save_df:
                        pd.DataFrame.to_csv(df, getattr(self, 'fp_csv'))
                        pd.DataFrame.to_csv(df_source, fp_csv_source)

                else:
                    logging.info('feature with ACTION == delete does not exist\n:{}'.format(index))

        elif action_type in ['rename']:
            for index in indices:
                print('did we make it here?')
                df_item = df.loc[index]
                fp_fcs_current = os.path.normpath(df_item[target_col])
                # create new filename components
                fc_new_name = df_item['RENAME']

                fp_components = fp_fcs_current.split(os.sep)
                # all but original file name
                fp_base = os.sep.join(fp_components[:-1])
                # full path to new fcs
                fp_fcs_new = os.path.join(fp_base, fc_new_name)

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
                    inventory_dir = lookup_table.loc[src_gdb_or_dir_str, 'inventory_dir']
                    fp_csv_source = os.path.join(inventory_dir, fname_csv)
                    df_str_source = lookup_table.loc[src_gdb_or_dir_str, 'df_str']
                else:
                    # clunky way of grabbing any inventory dir value
                    fp_csv_source = lookup_table[lookup_table.subproject == self.subproject_str].standalone_csv.values[0]
                    df_str_source = 'df_{}_standalone'.format(project_str)

                # Only grabs TargetGDB once per gdb
                try:
                    df_source = getattr(self, df_str_source)
                # if dataframe NOT already added via self.add_df
                except AttributeError:
                    print('populating source')
                    # note this also creates fp_csv_archive
                    self.add_df(fp_csv_source, df_str_source, 'ITEM')
                    df_source = getattr(self, df_str_source)

                if not dry_run:
                    msg_str = '\nRENAMING: {}\nTO:        {}'.format(fp_fcs_current, fp_fcs_new)
                    arcpy.Rename_management(fp_fcs_current, fp_fcs_new)
                    # Now fp is renamed, so change alias on NEW fcs
                    arcpy.AlterAliasName(fp_fcs_new, fc_new_name)

                # To document whether fp_fcs_current = Staging, Previous, Original
                col_name_original = df_item['COL_NAME_ARCHIVAL']
                merge_cols = df_item['MERGE_COLUMNS']
                if not pd.isnull(col_name_original):
                    col_name_original = dict_col_name_orig[col_name_original]
                    d = {col_name_original: fp_fcs_current,
                         'DATA_LOCATION_MCMILLEN': fp_fcs_new}
                else:
                    d = {'DATA_LOCATION_MCMILLEN': fp_fcs_new}

                # UPDATE DF
                df.loc[index, list(d.keys())] = list(d.values())
                # RENAME label
                df = df.rename(index = {index:fc_new_name})
                setattr(self, df_str, df)

                # columns to transfer from maestro to source
                if not pd.isnull(merge_cols):
                    keys = [c.strip() for c in merge_cols.split(',')]
                    vals = df_source.loc[index, keys]
                    d.update(dict(zip(keys, vals)))

                df_source.loc[index, list(d.keys())] = list(d.values())
                df_source = df_source.rename(index = {index:fc_new_name})

                # Save to DF
                if save_df:
                    pd.DataFrame.to_csv(df, getattr(self, 'fp_csv'))
                    pd.DataFrame.to_csv(df_source, fp_csv_source)

                logging.info(msg_str)

        elif action_type in ['move']:

            for index in indices:
                df_item = df.loc[index]
                fp_fcs_current = os.path.normpath(df_item[target_col])
                dset_move = df_item['MOVE_LOCATION_DSET']
                fc_new_name = df_item['RENAME']

                if not pd.isnull(fc_new_name):
                    rename = True
                else:
                    rename = False

                # DETERMINE DSET
                rename_delete_protocol = False
                fp_components = fp_fcs_current.split(os.sep)

                fp_move = olt.loc[df_item['MOVE_LOCATION'], 'online']


                for idx, comp in enumerate(fp_components):
                    if '.gdb' in comp:
                        fp_gdb_orig = os.sep.join(fp_components[:idx+1])
                        dset_orig = fp_components[idx + 1]
                        # same gdb cannot have features with the same name even in diff dsets.;
                        if (fp_gdb_orig == fp_move) and not rename:
                            rename_delete_protocol = True

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
                    inventory_dir = lookup_table.loc[src_gdb_or_dir_str, 'inventory_dir']
                    fp_csv_source = os.path.join(inventory_dir, fname_csv)
                    print('FP CSV SOURSE:  {}'.format(fp_csv_source))
                    df_str_source = lookup_table.loc[src_gdb_or_dir_str, 'df_str']
                else:
                    # clunky way of grabbing any inventory dir value
                    fp_csv_source = lookup_table[lookup_table.subproject == self.subproject_str].standalone_csv.values[0]
                    df_str_source = 'df_{}_standalone'.format(project_str)


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

                # src and tgt same, then only need one non maestro df
                if src_gdb_or_dir_str == tgt_gdb_or_dir_str:
                    src_tgt_same = True
                else:
                    src_tgt_same = False

                if not src_tgt_same:
                    inventory_dir = lookup_table.loc[tgt_gdb_or_dir_str, 'inventory_dir']
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

                # for featureclasstofeatureclass
                if pd.isnull(dset_move):
                    dset_move = ''

                fp_dset = os.path.join(fp_move, dset_move)
                # check to make sure output dset exists before proceeding
                if not arcpy.Exists(fp_dset):
                    arcpy.CreateFeatureDataset_management(fp_move, dset_move, self.prj_file)
                # print('fp new: \n{}'.format(fp_dset))
                # if rename specified
                if rename:
                    feat_name = copy.copy(fc_new_name)
                else:
                    feat_name = copy.copy(index)
                    feat_name = feat_name.replace(' ','_')
                    feat_name = feat_name.replace('&','_')
                    feat_name = feat_name.replace('.shp','')
                fp_fcs_new=os.path.join(fp_dset, feat_name)

                try:
                    if not dry_run:
                        # Should only trigger if move not copy (i.e. move into same gdb)
                        if rename_delete_protocol:
                            print('Rename Protocol GO!!!')
                            fp_fcs_current_comp = fp_fcs_current.split(os.sep)
                            fc_current_renamed = fp_fcs_current_comp[-1] + '_1'
                            fp_fcs_renamed = os.path.sep.join(fp_fcs_current_comp[:-1] + [fc_current_renamed])
                            debug_idx = 1
                            msg_substr = copy.copy(fp_fcs_current)
                            msg_substr2 = copy.copy(os.path.join(fp_dset, feat_name))
                            arcpy.Rename_management(fp_fcs_current, fc_current_renamed)
                            debug_idx = 2
                            arcpy.FeatureClassToFeatureClass_conversion(fp_fcs_renamed, fp_dset, feat_name)
                            debug_idx = 3
                            arcpy.Delete_management(fp_fcs_renamed)
                        else:
                            msg_substr = copy.copy(fp_fcs_current)
                            msg_substr2 = copy.copy(os.path.join(fp_dset, feat_name))
                            arcpy.FeatureClassToFeatureClass_conversion(fp_fcs_current, fp_dset, feat_name)
                            debug_idx = 4
                            # delete if file is moved
                            if action_type == 'move':
                                print('Delete Protocol GO!!!')
                                arcpy.Delete_management(fp_fcs_current)
                                debug_idx = 6
                                setattr(self, df_str_source, df_source)

                    # TARGET DF UPDATES
                    # Assemble Series to append to Master DF

                    # To document whether fp_fcs_current = Staging, Previous, Original
                    col_name_original = df_item['COL_NAME_ARCHIVAL']
                    merge_cols = df_item['MERGE_COLUMNS']
                    print('MERGE COLUMNS: ', merge_cols)
                    if not pd.isnull(col_name_original):
                        col_name_original = dict_col_name_orig[col_name_original]
                        df.at[index, col_name_original] = fp_fcs_current
                        d = {col_name_original: fp_fcs_current,
                             'FEATURE_DATASET':dset_move,
                             'DATA_LOCATION_MCMILLEN':fp_fcs_new}
                    else:
                        d = {'FEATURE_DATASET':dset_move,
                             'DATA_LOCATION_MCMILLEN':fp_fcs_new}

                    df.loc[index, list(d.keys())] = list(d.values())
                    df = df.rename(index = {index:feat_name})

                    # columns to transfer from source to target
                    if not pd.isnull(merge_cols):
                        keys = [c.strip() for c in merge_cols.split(',')]
                        vals = df_source.loc[index, keys]
                        d.update(dict(zip(keys,vals)))

                    # append new row from Series
                    debug_idx = 7

                    try:
                        df_source.drop(index, inplace = True)
                    except KeyError:
                        pass

                    if src_tgt_same:
                        df_target = copy.copy(df_source)

                    # first drop index in case multiple times running due to error
                    try:
                        print('1205')
                        df_target.drop(index, inplace=True)
                    except KeyError:
                        pass

                    df_target.loc[index, list(d.keys())] = list(d.values())

                    if rename:
                        # Replace indice with new feat name
                        print('1217')
                        idt = [i for i, index_val in enumerate(indices) if index_val == index]
                        idt = idt[0]
                        print('index = {}'.format(idt))
                        indices[idt]=feat_name
                        setattr(self, prop_str_indices, indices)
                    debug_idx = 8

                    if not dry_run:
                        msg_str = '\nMOVING:  {}\nTO:      {}'.format(msg_substr, msg_substr2)
                        logging.info(msg_str)

                    # SAVE TO TARGET_DF every Iter in case Exception
                    setattr(self, df_str, df)
                    setattr(self, df_str_source, df_source)
                    if not src_tgt_same:
                        setattr(self, df_str_target, df_target)

                    if save_df:
                        pd.DataFrame.to_csv(df, getattr(self, 'fp_csv'))
                        pd.DataFrame.to_csv(df_source, fp_csv_source)
                        if not src_tgt_same:
                            pd.DataFrame.to_csv(df_target, fp_csv_target)

                except Exception as e:
                    if not dry_run:
                        logging.info(debug_idx)
                        msg_str = '\nUNABLE TO MOVE:  {}\nARCPY DEBUG: {}'.format(msg_substr, debug_idx)
                        logging.info(msg_str)
                        logging.info(e)
                    debug_idx = 0
                    fp_fcs_new = os.path.join(fp_move, dset_move, feat_name)
                    print('feat name to copy {}'.format(feat_name))
                    # full path with featureclass name

        elif action_type in ['copy_no_replace', 'copy_replace']:
            # Get indices where duplicates occur
            dup_idx = list(set(df[df.index.duplicated(keep=False)].index))
            if len(dup_idx):
                logging.info(f"DUPLICATES ON THESE INDICES {dup_idx}")
                # Stop running if duplicate indices
                return
            for index in indices:
                df_item = df.loc[index]
                fp_fcs_current = os.path.normpath(df_item[target_col])
                dset_move = df_item['MOVE_LOCATION_DSET']
                fc_new_name = df_item['RENAME']

                if not pd.isnull(fc_new_name):
                    rename = True
                else:
                    rename = False

                fp_components = fp_fcs_current.split(os.sep)
                fp_move = olt.loc[df_item['MOVE_LOCATION'], 'online']

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
                    inventory_dir = lookup_table.loc[src_gdb_or_dir_str, 'inventory_dir']
                    fp_csv_source = os.path.join(inventory_dir, fname_csv)
                    print('FP CSV SOURCE:  {}'.format(fp_csv_source))

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

                inventory_dir = lookup_table.loc[tgt_gdb_or_dir_str, 'inventory_dir']
                fname_csv = lookup_table.loc[tgt_gdb_or_dir_str, 'fname_csv']
                fp_csv_target = os.path.join(inventory_dir, fname_csv)
                print('CSV TARGET:    --->',  fp_csv_target)
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

                # for featureclasstofeatureclass
                if pd.isnull(dset_move):
                    dset_move = ''

                fp_dset = os.path.join(fp_move, dset_move)
                # check to make sure output dset exists before proceeding
                if not arcpy.Exists(fp_dset):
                    arcpy.CreateFeatureDataset_management(fp_move, dset_move, self.prj_file)
                # print('fp new: \n{}'.format(fp_dset))
                # if rename specified
                if rename:
                    feat_name = copy.copy(fc_new_name)
                else:
                    feat_name = copy.copy(index)
                    feat_name = feat_name.replace(' ','_')
                    feat_name = feat_name.replace('&','_')
                    feat_name = feat_name.replace('.shp','')

                # full path with featureclass name
                print('feat name to copy {}'.format(feat_name))
                fp_fcs_new = os.path.join(fp_move, dset_move, feat_name)
                debug_idx = 0
                try:
                    if not dry_run:
                        msg_substr = copy.copy(fp_fcs_current)
                        msg_substr2 = copy.copy(os.path.join(fp_dset, feat_name))
                        try:
                            wc = kwargs['where_clause']
                            arcpy.FeatureClassToFeatureClass_conversion(fp_fcs_current, fp_dset, feat_name, where_clause = wc)
                        except KeyError:
                            arcpy.FeatureClassToFeatureClass_conversion(fp_fcs_current, fp_dset, feat_name)
                        debug_idx = 4

                    col_name_original = df_item['COL_NAME_ARCHIVAL']
                    debug_idx = 41
                    if not pd.isnull(col_name_original):
                        col_name_original = dict_col_name_orig[col_name_original]
                        df.at[index, col_name_original] = fp_fcs_current
                        d = {col_name_original: fp_fcs_current,
                             'FEATURE_DATASET': dset_move,
                             'DATA_LOCATION_MCMILLEN': fp_fcs_new}
                    # If we don't want to document COL_NAME_ARCHIVAL.  i.e. mistakenly added
                    # to master, and now decide to move back to archival.
                    else:
                        d = {'FEATURE_DATASET': dset_move,
                             'DATA_LOCATION_MCMILLEN': fp_fcs_new}
                    # columns to transfer from source to target
                    merge_cols = df_item['MERGE_COLUMNS']
                    debug_idx = 42
                    if not pd.isnull(merge_cols):
                        print('MERGE COLUMNS: ', merge_cols)
                        keys = [c.strip() for c in merge_cols.split(',')]
                        vals = df.loc[index, keys]
                        d.update(dict(zip(keys, vals)))
                    debug_idx =43
                    ser_append = pd.Series(data=d,
                                           index=list(d.keys()),
                                           name=feat_name)

                    # append new row from Series
                    debug_idx = 7
                    # first drop index in case multiple times running due to error
                    try:
                        print('1205')
                        df_target.drop(feat_name, inplace=True)
                    except KeyError:
                        pass

                    df_target = pd.concat([df_target, ser_append.to_frame().T])
                    debug_idx = 8
                    if action_type == 'copy_replace':
                        # similar in function to updating dictionary, but instead, updating row in df if new vals
                        df_join = pd.DataFrame(d, index=[index])
                        # saves name to csv column above index
                        df_join.index.name = copy.copy(df.index.name)
                        setattr(self, 'debug_df_join', df_join)
                        setattr(self,'debug_df', df)
                        col_order_orig = df.columns.to_list()
                        idx_order_orig = df.index.to_list()
                        df = df_join.combine_first(df)
                        debug_idx = 81
                        df = df.reindex(idx_order_orig)
                        debug_idx = 82
                        # or else gets reordered alphabetically
                        df = df.reindex(columns=col_order_orig)
                        print('debugging Z')
                    else:
                        df = pd.concat([df, ser_append.to_frame().T])

                    if rename:
                        # Replace indice with new feat name
                        print('1217 - renaming')
                        idt = [i for i, index_val in enumerate(indices) if index_val == index]
                        idt = idt[0]
                        print('index = {}'.format(idt))
                        indices[idt] = feat_name
                        setattr(self, prop_str_indices, indices)
                        if action_type == 'copy_replace':
                            df.rename(index={index:feat_name}, inplace=True)
                        else:
                            self.indices_iloc[idt] = df.index.get_loc(feat_name)
                        print('we did it')
                    debug_idx = 9

                    if not dry_run:
                        msg_str = '\nCOPYING:  {}\nTO:      {}'.format(msg_substr, msg_substr2)
                        logging.info(msg_str)

                    # SAVE TO TARGET_DF every Iter in case Exception
                    setattr(self, df_str_target, df_target)
                    setattr(self, df_str, df)

                    if save_df:
                        pd.DataFrame.to_csv(df, getattr(self, 'fp_csv'))
                        pd.DataFrame.to_csv(df_target, fp_csv_target)

                except Exception as e:
                    if not dry_run:
                        logging.info(debug_idx)
                        msg_str = '\nUNABLE TO COPY:  {}\nARCPY DEBUG: {}'.format(msg_substr, debug_idx)
                        logging.info(msg_str)
                        logging.info(e)

        if action_type in ['create_poly', 'create_line', 'create_point']:
            # For adding new item to maestro and take_action(action_type = create_<type>...)
            for index in self.indices:
                print('HERE')
                df_item = df.loc[index]
                dset_move = df_item['MOVE_LOCATION_DSET']
                fp_move = olt.loc[df_item['MOVE_LOCATION'], 'online']

                # NO DSET passed
                if pd.isnull(dset_move):
                    dset_move = ''

                fp_dset = os.path.join(fp_move, dset_move)
                # check to make sure output dset exists before proceeding
                if not arcpy.Exists(fp_dset):
                    arcpy.CreateFeatureDataset_management(fp_move, dset_move, self.prj_file)

                feat_type_dict = {'create_poly': 'POLYGON', 'create_line': 'POLYLINE',
                                  'create_point': 'POINT'}
                feat_type = feat_type_dict[action_type]
                fp_fcs_new = os.path.join(fp_move, index)

                feat_name = copy.copy(index)
                msg_str = '\nCreating {} FC: {} in location:\n{}'.format(feat_type, feat_name, fp_fcs_new)
                # flag_index
                if not dry_run:
                    arcpy.CreateFeatureclass_management(fp_dset, feat_name, feat_type,
                                                        spatial_reference=self.prj_file,
                                                        has_m='No', has_z='No')

                d = {'ITEM': feat_name, 'DATE_CREATED': [self.todays_date],
                     'DATA_LOCATION_MCMILLEN': [fp_fcs_new.replace(os.sep, '//')]}

                df_append = pd.DataFrame(d)
                df_append = df_append.set_index('ITEM')

                # Get TARGET DF/CSV/STR
                fp_components = fp_fcs_new.split(os.sep)
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
                    inventory_dir = lookup_table.loc[tgt_gdb_or_dir_str, 'inventory_dir']
                    fp_csv_target = os.path.join(inventory_dir, fname_csv)
                    df_str_target = lookup_table.loc[tgt_gdb_or_dir_str, 'df_str']
                else:
                    fp_csv_target = lookup_table[lookup_table.subproject == self.subproject_str].standalone_csv.values[0]
                    df_str_target = 'df_{}_standalone'.format(self.subproject_str)

                # Only grabs TargetGDB once per gdb
                try:
                    df_target = getattr(self, df_str_target)
                # if dataframe NOT already added via self.add_df
                except AttributeError:
                    print('populating target')
                    # note this also creates fp_csv_archive
                    self.add_df(fp_csv_target, df_str_target, 'ITEM')
                    df_target = getattr(self, df_str_target)

                # Since adding new row, it's append
                df_target = pd.concat([df_target, ser_append.to_frame().T])

                # since updating existing NOT append
                print(df)
                print('\n')
                print(df_append)
                df.update(df_append)
                print('AFTERWARDS/n')
                print(df)
                setattr(self, df_str_target, df_target)
                setattr(self, df_str, df)

                if save_df:
                    pd.DataFrame.to_csv(df, getattr(self, 'fp_csv'))
                    pd.DataFrame.to_csv(df_target, fp_csv_target)


        elif action_type in ['fc_to_fc_conv']:
            var_dict = kwargs['var_dict']
            fp_fcs_current = var_dict['feat_in']
            index = indices[0]
            df_item = df.loc[index]

            fp_move = olt.loc[df_item['MOVE_LOCATION'], 'online']

            dset = df_item['MOVE_LOCATION_DSET']
            # NO DSET passed
            if pd.isnull(dset):
                pass
            else:
                fp_move = os.path.join(fp_move, dset)

            msg_str = 'FC to FC conversion: \n'
            msg_str = '{}  FEAT_IN:   ---  {}\n'.format(msg_str, fp_fcs_current)
            feat_name = copy.copy(index)
            fp_fcs_new = os.path.join(fp_move, feat_name)
            msg_str = '{}  FEAT_OUT: ---  {}\n'.format(msg_str, fp_fcs_new)
            if not dry_run:
                arcpy.FeatureClassToFeatureClass_conversion(fp_fcs_current, fp_move, feat_name)

            # documentation to add to table
            logging.info(msg_str)

                # Dict will be UPDATED below if kwarg specified
            d = {'ITEM':feat_name, 'DATE_CREATED':[self.todays_date],
                'DATA_LOCATION_MCMILLEN':[fp_fcs_new.replace(os.sep, '//')]}

            df_append = pd.DataFrame(d)
            df_append = df_append.set_index('ITEM')

            # Get TARGET DF/CSV/STR
            fp_components = fp_fcs_new.split(os.sep)
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
                inventory_dir = lookup_table.loc[tgt_gdb_or_dir_str, 'inventory_dir']
                fp_csv_target = os.path.join(inventory_dir, fname_csv)
                df_str_target = lookup_table.loc[tgt_gdb_or_dir_str, 'df_str']
            else:
                fp_csv_target = lookup_table[lookup_table.subproject == self.subproject_str].standalone_csv.values[0]
                df_str_target = 'df_{}_standalone'.format(self.subproject_str)

            # Only grabs TargetGDB once per gdb
            try:
                df_target = getattr(self, df_str_target)
            # if dataframe NOT already added via self.add_df
            except AttributeError:
                print('populating target')
                # note this also creates fp_csv_archive
                self.add_df(fp_csv_target, df_str_target, 'ITEM')
                df_target = getattr(self, df_str_target)

            # Since adding new row, it's append
            df_target = pd.concat([df_target, ser_append.to_frame().T])
            # since updating existing NOT append
            print(df)
            print('\n')
            print(df_append)
            df.update(df_append)
            print('AFTERWARDS/n')
            print(df)
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
            fp_fcs = df.iloc[indices_iloc].DATA_LOCATION_MCMILLEN.to_list()
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
            fp_log_prop_str = 'fp_log'
        else:
            df_base_str = df_str.replace('df_', '')
            fp_csv_prop_str = 'fp_csv_{}'.format(df_base_str)
            fp_csv_archive_prop_str = 'fp_csv_archive_{}'.format(df_base_str)
            fp_log_prop_str = 'fp_log_{}'.format(df_base_str)

        fp_csv = getattr(self, fp_csv_prop_str)
        basepath = os.path.splitext(fp_csv)[0]
        setattr(self, fp_csv_archive_prop_str, '{}_archive.csv'.format(basepath))
        fp_log = '{}_logfile.log'.format(basepath)
        setattr(self, fp_log_prop_str, fp_log)
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
                                i.e. fp_feat, DATA_LOCATION_MCMILLEN
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
        if not df_source.index.name==replace_col_source:
            idx_target = df_source[df_source[match_col_source]==target_val][replace_col_source]
        else:
            idx_target = df_source[[df_source[match_col_source]==target_val]].index
        if not df_target.index.name == replace_col_target:
            idx_name = df_target.index.name
            df_target.set_index(replace_col_target, inplace=True)
            df_target.at[idx_target, match_col_target]=target_val
            df_target.set_index(idx_name, inplace=True)
        else:
            df_target.at[idx_target, match_col_target]=target_val

        setattr(self, '{}_matched'.format(df_str_target), df_target)

    def df_to_df_transfer_v2(self, df_src, df_tgt, flag_col_src, flag_val, key_src,
                             key_tgt, merge_cols_dict, concat=False):
        '''
        More for manual transfers.
        flag_col_src            name of column to transfer to ID rows and flag_col_tgt i.e. action
        flag_val                val for loc in src df to loc and transfer to tgt
        key_src                name of column to receive vals from flag_col_src
        key_tgt                name of column to receive vals from flag_col_src
        merge_cols_dict         dict of col names to replace or add vals from src to tgt.
                                Replicate k:v if the column names match between df_src and df_tgt
        concat                  If want to add non intersecting rows from src to tgt in addition to
                                the whole other protocol
        '''
        if df_src.index.name!=key_src:
            df_src = df_src.set_index(key_src)

        reset_idx=False
        if df_tgt.index.name != key_tgt:
            idx_name = copy.copy(df_tgt.index.name)
            df_tgt.reset_index(inplace=True)
            df_tgt.set_index(key_tgt, inplace=True)
            reset_idx=True
        if isinstance(flag_val, list):
            df_src_subset = df_src[df_src[flag_col_src].isin(flag_val)]
        else:
            df_src_subset = df_src[df_src[flag_col_src] == flag_val]

        merge_idx = list(set(df_tgt.index).intersection(df_src_subset.index))
        for col_src, col_tgt in merge_cols_dict.items():
            df_tgt.loc[merge_idx, col_tgt] = df_src_subset.loc[merge_idx, col_src]
        if concat:
            # find rows that were not originally in tgt
            concat_idx = list(set(df_src_subset.index) - set(df_tgt.loc[merge_idx].index))
            # first remap select src columns to tgt columns from dict
            # subet to ommitted rows and src_cols
            cols_append=list(set(df_tgt.columns).intersection(set(df_src.columns)))
            # if src col names to key - append and find key
            cols_append.extend(list(merge_cols_dict.keys()))
            cols_append = list(set(cols_append))
            # key the few col names contained in dict
            df_src_subset = df_src_subset.loc[concat_idx, cols_append]
            df_src_subset.rename(columns=merge_cols_dict, inplace=True)
            df_tgt = pd.concat([df_tgt, df_src_subset])
        if reset_idx:
            df_tgt.reset_index(inplace=True)
            df_tgt.set_index(idx_name, inplace=True)

        return(df_tgt)

    def data_sent_tracking(self, fp_csv_tracking, base_dir, action, tracking_dict):
        '''
        Initially created for a JB request in 20220209.  Updated now - 20230224. ZU

        Args:
            fp_csv_tracking:        similiar to item_desc but an ongoing list for this purpose
            base_dir:               path/to/base_dir/<shp and zip> nested there
            action:                 only one so far
            tracking_dict:          to populate csv

        Returns:

        '''
        fp_list = self.df.loc[self.indices, 'DATA_LOCATION_MCMILLEN']
        notes = tracking_dict['notes']
        tags = tracking_dict['tags']
        rec_comp = tracking_dict['recipient_company']
        rec_name = tracking_dict['recipient_name']
        project = tracking_dict['project']

        # prep shape dir
        arcpy.env.addOutputsToMap = False

        write_df = True
        if action == 'copy_to_gdb':
            items=[]
            if base_dir[-4:]=='.gdb':
                if os.path.exists(base_dir):
                    pass
                else:
                    bp, gdb_name = os.path.split(base_dir)
                    arcpy.CreateFileGDB_management(bp, gdb_name)
                for fp, fn in zip(fp_list, self.indices):
                    fc_new_name = self.df.loc[fn,'RENAME_SHARE']
                    if not pd.isnull(fc_new_name):
                        fname = fc_new_name
                    else:
                        fname=copy.copy(fn)
                    items.append(fname)
                    arcpy.FeatureClassToFeatureClass_conversion(fp, base_dir, fname)
            else:
                write_df = False
                print('Used copy_to_gdb action but did not pass path to gdb for base_dir parameter')

        if action == 'convert_zip':
            shp_dir = os.path.join(base_dir, 'shp')
            items=[]
            if not os.path.exists(shp_dir):
                os.mkdir(shp_dir)
            for fp, fn in zip(fp_list, self.indices):
                fc_new_name = self.df.loc[fn,'RENAME_SHARE']
                if not pd.isnull(fc_new_name):
                    fname = fc_new_name
                else:
                    fname = copy.copy(fn)
                arcpy.FeatureClassToFeatureClass_conversion(fp, shp_dir, fname)
                items.append(fname)
            zip_dir = os.path.join(base_dir,'zip')
            if not pd.isnull(fc_new_name):
                self.zip_shp_dir(shp_dir, zip_dir, renamed_files=items)
            else:
                self.zip_shp_dir(shp_dir, zip_dir)
        if write_df:
            df_tracking = pd.read_csv(fp_csv_tracking)
            c1 = [notes] * len(self.indices)
            c2 = [tags] * len(self.indices)
            c3 = [rec_comp] * len(self.indices)
            c4 = [rec_name] * len(self.indices)
            c5 = [project] * len(self.indices)
            c6 = items
            if action=='copy_to_gdb':
                c7 = [os.path.join(base_dir, '{}.shp'.format(i)) for i in self.indices]
            elif action=='convert_zip':
                c7 = [os.path.join(shp_dir, '{}.shp'.format(i)) for i in self.indices]
            c8 = fp_list
            c9 = [self.todays_date]* len(self.indices)

            df_new_rows = pd.DataFrame(np.column_stack([c1,c2,c3,c4,c5, c6,c7,c8, c9]),
                                       columns = ['NOTES', 'TAGS', 'RECIPIENT_COMPANY',
                                                  'RECIPIENT_NAME', 'PROJECT',
                                                  'ITEM', 'DATA_LOCATION_SHARED',
                                                  'DATA_LOCATION_MCMILLEN',
                                                  'DATE'])
            df_tracking = df_tracking.append(df_new_rows)
            pd.DataFrame.to_csv(df_tracking, fp_csv_tracking)

    def parse_csString_utils(self, csString, **kwargs):
        '''
        Parse Comma-Sep Strings utilities.  Add to kwargs for  more scenarios.
        Args:
            csString:           Comma Separated String
            **kwargs:           kwargs[remove] = pass value to remove from csString
        Returns:
            csString_updated    updated csString i.e. with tgt_val removed

        '''
        try:
            tgt_val = kwargs['remove_item']
            # if no comma sep string i.
            if ~pd.isnull(tgt_val):
                csString_updated = [v.strip() for v in csString.split(',') if v.strip() != tgt_val]
                csString_updated = ','.join(csString_updated)
                return(csString_updated)
            else:
                return(csString)
        except KeyError:
            return(csString)

class proProject(commonUtils):
    '''
    INSERT / FLESH OUT
    '''
    def __init__(self):
        print('something')
    def proProject_init(self, fp_pathlist_aprx):
        setattr(self, 'fp_pl_aprx', fp_pathlist_aprx)
        pl_aprx =pd.read_excel(fp_pathlist_aprx, index_col='subproject')
        setattr(self, 'pl_aprx', pl_aprx)
    def add_aprx(self,subproject, target_col = r'DATA_LOCATION_MCMILLEN', add_lyR_inv = True,**kwargs):
        fp_aprx=self.pl_aprx.loc[subproject,'fp_aprx']
        setattr(self, 'fp_{}'.format(subproject), fp_aprx)
        aprx = arcpy.mp.ArcGISProject(fp_aprx)
        aprx_str = 'aprx_{}'.format(subproject)
        setattr(self, aprx_str, aprx)
        if add_lyR_inv:
            try:
                kwargs['lyR_maestro']
                fp_lyR_inv = self.pl_aprx.loc[subproject, 'fp_lyR_aprx']
                df_lyR_str = f"df_{subproject}_lyR_maestro"
                fp_lyR_str = f"fp_{subproject}_lyR_maestro"
            except KeyError:
                fp_lyR_inv = self.pl_aprx.loc[subproject, 'fp_lyR_inv']
                df_lyR_str = f"df_{subproject}_lyR"
                fp_lyR_str = f"fp_{subproject}_lyR"

            df_lyR_inv = pd.read_csv(fp_lyR_inv, index_col=target_col)
            setattr(self, df_lyR_str, df_lyR_inv)
            setattr(self, fp_lyR_str, fp_lyR_inv)
    def add_maps(self, subproject):
        '''
        fetches aprx maps and layouts from init attributes
        Args:
            aprx_str:       <aprx name>_aprx

        Returns:
        '''
        aprx = getattr(self, f"aprx_{subproject}")
        m =  aprx.listMaps()
        map_str = f"{subproject}_maps"
        setattr(self, map_str, m)
    def add_layouts(self, aprx_str):
        '''
        fetches aprx maps and layouts from init attributes
        NEVER USED
        Args:
            aprx_str:       <aprx name>_aprx

        Returns:
        '''
        aprx = getattr(self, aprx_str)
        l =  aprx.listLayouts()
        map_str = aprx_str.replace('aprx','layouts')
        setattr(self, layout_str, l)

    def format_lyR_inv_datasource_standard(self, subproject, df_str, prop_str_indices, source_new='DATA_LOCATION_MCM_RESOURCE'):

        # A) Gather Connetion Info
        fp_csv = self.pl_aprx.loc[subproject, 'fp_df_reSource']
        indices = getattr(self, prop_str_indices)
        try:
            df = getattr(self, df_str)
        except AttributeError:
            self.add_df(fp_csv, df_str, 'DATA_LOCATION_MCMILLEN')
            df = getattr(self, df_str)

        # Use orig (path/to/fc i.e. DATA_LOCATION_MCMILLEN
        for idx in indices:
            # idx_lyR = os.path.normpath(df_gdb_inv.loc[idx, source_orig])
            # fp_new = os.path.normpath(df_gdb_inv.loc[idx, source_new])
            fp_new = os.path.normpath(df.loc[idx, source_new])
            if not df.loc[idx, 'IS_RASTER']:
                if fp_new[-4:] == '.shp':
                    dbase_connection, fname = os.path.split(fp_new)
                    df.at[idx, 'workspace_factory'] = 'Shape File'
                else:
                    dbase_connection = '{}.gdb'.format(fp_new.split('.gdb')[0])
                    df.at[idx, 'workspace_factory'] = 'FileGDB'
                    fp_comps = fp_new.split(os.sep)
                    fname, dset = fp_comps[-1], fp_comps[-2]
                    if 'gdb' not in dset:
                        df.at[idx, 'feature_dataset']=dset
                df.at[idx, 'dataset'] = fname
                df.at[idx, 'dbase_connection'] = dbase_connection
            else:
                fp_comps = fp_new.split('.gdb')
                if len(fp_comps)==2:
                    dbase_connection = '{}.gdb'.format(fp_comps[0])
                    df.at[idx, 'workspace_factory'] = 'Raster'
                    fp_comps = fp_new.split(os.sep)
                    fname, dset = fp_comps[-1], fp_comps[-2]
                    if 'gdb' not in dset:
                        df.at[idx, 'feature_dataset'] = dset
                else:
                    df.at[idx, 'workspace_factory'] = 'Raster'
                    fp_comps = os.path.split(fp_new)
                    dbase_connection = fp_comps[0]
                    fname=fp_comps[-1]
                df.at[idx, 'dataset'] = fname
                df.at[idx, 'dbase_connection'] = dbase_connection
        setattr(self, df_str, df)

    def re_source_lyR_maestro(self, subproject, prop_str_indices, fp_log_prop_str, tc='DATA_LOCATION_MCMILLEN',**kwargs):

        fp_logfile = getattr(self, fp_log_prop_str)
        logging.basicConfig(filename=fp_logfile, level=logging.DEBUG)
        # Save call string to logfile
        banner = '    {}    '.format('-' * 50)
        date_str = datetime.datetime.today().strftime('%D %H:%M')
        msg_str = '\n{}\n{}\n{}\nRESOURCING'.format(banner, date_str, banner)
        logging.info(msg_str)

        df_lyR_map_str=f"df_{subproject}_map_lyR"
        df_lyR_aprx_str=f"df_{subproject}_aprx_lyR"
        df_lyR_all_str=f"df_{subproject}_all_lyR"
        df_map_matrix_str=f"df_{subproject}_map_matrix"
        df_reSource_str=f"df_{subproject}_reSource"
        fp_lyR_inv_map = self.pl_aprx.loc[subproject, 'fp_lyR_map']
        fp_lyR_inv_aprx = self.pl_aprx.loc[subproject, 'fp_lyR_aprx']
        fp_lyR_inv_all = self.pl_aprx.loc[subproject, 'fp_lyR_all']
        fp_map_matrix = self.pl_aprx.loc[subproject, 'fp_map_matrix']
        fp_reSource = self.pl_aprx.loc[subproject, 'fp_df_reSource']

        try:
            getattr(self, df_lyR_map_str)
        except AttributeError:
            self.add_df(fp_lyR_inv_map, df_lyR_map_str, [tc, 'APRX'])
        try:
            getattr(self, df_lyR_aprx_str)
        except AttributeError:
            self.add_df(fp_lyR_inv_aprx, df_lyR_aprx_str,tc)
        try:
            getattr(self, df_lyR_all_str)
        except AttributeError:
            self.add_df(fp_lyR_inv_all, df_lyR_all_str,[tc,'APRX','MAP_NAME'])
        try:
            getattr(self, df_map_matrix_str)
        except AttributeError:
            self.add_df(fp_map_matrix, df_map_matrix_str, tc)
        try:
            getattr(self, df_reSource_str)
        except AttributeError:
            self.add_df(fp_reSource, df_reSource_str, tc)

        df_lyR_inv_aprx=getattr(self, df_lyR_aprx_str)
        df_lyR_inv_map=getattr(self, df_lyR_map_str)
        df_lyR_inv_map.reset_index().set_index([tc, 'APRX'], inplace=True)
        df_lyR_inv_all=getattr(self, df_lyR_all_str)
        df_lyR_inv_all.reset_index().set_index([tc,'APRX','MAP_NAME'],inplace=True)
        df_map_matrix=getattr(self, df_map_matrix_str)
        df_reSource = getattr(self, df_reSource_str)

        # Initiate map removal accounting if needed
        if r'MAP_NAME_UPDATED' not in df_lyR_inv_map.columns:
            df_lyR_inv_map['MAP_NAME_UPDATED']=df_lyR_inv_map['MAP_NAME']
        if r'APRX_UPDATED' not in df_lyR_inv_aprx.columns:
            df_lyR_inv_aprx['APRX_UPDATED']=df_lyR_inv_aprx['APRX']

        indices = getattr(self, prop_str_indices)

        # INIT LOGFILE
        self.init_logfile(subproject)
        map_temp, layer_temp=[],[]

        # Returns rows in index and columns with any True valeus
        included_indices = list(set(indices).intersection(set(df_map_matrix.index)))
        excluded_indices = list(set(indices)-set(df_map_matrix.index))
        try:
            df_map_matrix_subset = df_map_matrix.loc[indices]
            t1 = ', '.join(included_indices)
            t2 = ', '.join(excluded_indices)
            msg_str='\nINCLUDING: {}\nNOT PRESENT IN {}: {}'.format(t1,subproject, t2)
            logging.info(msg_str)
            no_layers_aprx=False
        except KeyError:
            msg_str = '\nNONE of the indices were present in {}'.format(subproject)
            logging.info(msg_str)
            no_layers_aprx=True
        if not no_layers_aprx:
            map_objects = getattr(self, f"{subproject}_maps")

            # Remove maps not in Use i.e. not in present in indices
            idx_cols=[c for c in df_map_matrix_subset.columns if 'CHANGE' in df_map_matrix_subset[c].values]
            map_objects_subset = [mo for mo in map_objects if mo.name in idx_cols]
            aprx_indices=[]
            for m in map_objects_subset:
                # Pulls layers with TRUE in each map column from matrix
                tgt_layers = df_map_matrix_subset[df_map_matrix_subset[m.name]=='CHANGE'].index
                layers = m.listLayers()
                for lyr in layers:
                    try:
                        if lyr.dataSource in tgt_layers:
                            # dataSource and in tgt_layer
                            resource = True
                        else:
                            resource = False
                    except AttributeError:
                        # does not have dataSource attribute (i.e. map server or...something)
                        resource = False
                    if resource:
                        try:
                            idx = copy.copy(os.path.normpath(lyr.dataSource))
                            wsf = df_reSource.loc[idx, 'workspace_factory']
                            dbase_connection = df_reSource.loc[idx, 'dbase_connection']
                            dataset = df_reSource.loc[idx, 'dataset']
                            feature_dataset = df_reSource.loc[idx, 'feature_dataset']

                            lyr_cim = lyr.getDefinition('V3')
                            # https://community.esri.com/t5/python-questions/updating-the-data-source-of-a-feature-class-in-a/m-p/1116155#M62964
                            dc = arcpy.cim.CreateCIMObjectFromClassName('CIMStandardDataConnection', 'V3')
                            dc.workspaceConnectionString = f"DATABASE={dbase_connection}"
                            dc.workspaceFactory = wsf
                            dc.dataset = dataset
                            # check for feature dataset
                            if not pd.isnull(feature_dataset):
                                dc.featureDataset = feature_dataset
                            # Different object structure with Raster
                            if wsf=='Raster':
                                lyr_cim.dataConnection = dc
                            elif wsf in ('Shapefile', 'FileGDB'):
                                lyr_cim.featureTable.dataConnection = dc
                            lyr.setDefinition(lyr_cim)

                            # new_path = df_lyR_inv.loc[idx,'DATA_LOCATION_MCM_RESOURCE']
                            idx_all=(idx, subproject, m.name)
                            df_lyR_inv_all.loc[idx_all,'RESOURCED_COMPLETE']=True
                            setattr(self, df_lyR_all_str, df_lyR_inv_all)
                            # Once successful, remove map name of resource layer from list
                            idx_map = (idx, subproject)
                            csString = df_lyR_inv_map.loc[(idx_map), 'MAP_NAME_UPDATED']
                            csString_updated = self.parse_csString_utils(csString, remove_item = m.name)
                            df_lyR_inv_map.loc[idx_map, 'MAP_NAME_UPDATED'] = csString_updated
                            setattr(self, df_lyR_map_str, df_lyR_inv_map)

                            df_map_matrix.loc[idx,m.name]='FIXED'
                            setattr(self, f"df_{subproject}_map_matrix", df_map_matrix)

                            aprx_indices.append(idx)

                            self.logger.info('SUCCESS\nMAP: {} \nLAYER {}'.format(m.name, idx))
                            self.logger.info('CONNECTION PROPERTIES: {}'.format(lyr.connectionProperties['connection_info']['database']))
                        except KeyError as e:
                            self.logger.info('EXCEPTION {}'.format(e))
                            map_temp.append(m.name)
                            layer_temp.append(idx)
                    else:
                        pass
            for idx in aprx_indices:
                csString = df_lyR_inv_aprx.loc[idx, 'APRX_UPDATED']
                csString_updated = self.parse_csString_utils(csString, remove_item=subproject)
                df_lyR_inv_aprx.loc[idx, 'APRX_UPDATED'] = csString_updated
                setattr(self, df_lyR_aprx_str, df_lyR_inv_aprx)
            aprx = getattr(self, f"aprx_{subproject}")
            aprx.save()

    def init_logfile(self, subproject):
        logger = logging.getLogger(subproject)
        fp_logfile = self.pl_aprx.loc[subproject, 'fp_logfile']
        logging.basicConfig(filename=fp_logfile, level=logging.DEBUG)
        banner = '    {}    '.format('-' * 50)
        call_str = 're_source_lyR_maestro {}:\n'.format(subproject)
        fct_call_str = 'Performing function called as:\n{}'.format(call_str)
        date_str = datetime.datetime.today().strftime('%D %H:%M')
        msg_str = '\n{}\n{}\n{}\n{}'.format(banner, date_str, banner, fct_call_str)
        logging.info(msg_str)
        setattr(self, 'logger', logger)
    def aprx_map_inv(self, aprx_path):
        '''
        Inventory of single aprx from aprx path
        20241021
        Args:
            aprx_path:      path/to/aprs
            csv_out:        path to lyR inventory
        Returns:

        '''
        aprx = arcpy.mp.ArcGISProject(aprx_path)
        map_objects = aprx.listMaps()
        src_list, map_list,broken, raster,layer_name_list = [],[],[],[],[]
        for m in map_objects:
            layers = m.listLayers()
            for lyr in layers:
                if lyr.visible and lyr.supports('DATASOURCE'):
                    broken.append(lyr.isBroken)
                    if lyr.isFeatureLayer:
                        raster.append(False)
                    elif lyr.isRasterLayer:
                        raster.append(True)
                    else:
                        raster.append(False)
                    src = lyr.dataSource
                    src_list.append(src)
                    layer_name_list.append(lyr.name)
                    map_list.append(m.name)
        del map_objects
        del aprx

        item = [os.path.split(fp)[-1] for fp in src_list]
        cols=['ITEM', 'DATA_LOCATION_MCMILLEN', 'LAYER_NAME','MAP_NAME','IS_RASTER','IS_BROKEN']
        vals = np.column_stack([item, src_list, layer_name_list, map_list, raster, broken])
        df = pd.DataFrame(vals, columns=cols)
        return(df)

    def aprx_map_inv2(self, csv_in, csv_out):
        '''
        20241021
        Compiling single inv from multiple aprx paths via aprx inv
        Need a True/False FLAG field to subset rows to inventory
        Args:
            csv_in:         path/to/aprx inventory (if exists for bulk; i.e. Tolt)
            csv_out:        path to lyR inventory
        Returns:

        '''
        df = getattr(self, 'pl_aprx')
        df = df[df.FLAG]
        src_list, map_list, broken, raster = [], [], [], []
        for idx in df.index:
            aprx_path = df.loc[idx, 'fp_aprx']
            if 'df_concat' not in locals():
                df_concat = self.aprx_map_inv(aprx_path)
                df_concat['APRX']=len(df_concat)*[idx]
            else:
                t = self.aprx_map_inv(aprx_path)
                t['APRX']=len(t)*[idx]
                df_concat=pd.concat([df_concat, t])
        df_concat.to_csv(csv_out)
    def expand_rows(self, subproject, csv_out, update=False):
        '''
        Outputs a True False matrix flagging which map utilizes which layer.
        For use in making re-sourceing more efficient.  Parses comma separated
        string column map_name ["map1", "map2", "mapn"] from lyR_inv as primary input.
        20241015
        Args:
            subproject:       yeah
            csv_out:        for mapping grid dataframe
            update:         set to True if map matrix already populated and CHANGED values have been updated with
                            resourcing.  Will retain those values and only create new rows for added rows
                            i.e. if layout imported like PSP_3 to PSP_2

        Returns:

        '''
        df_lyR_inv=pd.read_csv(self.pl_aprx.loc[subproject, 'fp_lyR_inv'], index_col='DATA_LOCATION_MCMILLEN')

        maps = df_lyR_inv.MAP_NAME
        maps_unique=[y.strip() for x in maps for y in x.split(',')]
        maps_unique=list(set(maps_unique))
        layers = df_lyR_inv.index
        vals = np.full([len(layers), len(maps_unique)], r'-----')
        df_maps_join = pd.DataFrame(vals, columns = maps_unique)
        index = pd.Index(layers)
        df_maps_join = df_maps_join.set_index(index)
        for idx in df_lyR_inv.index:
            map_list = df_lyR_inv.loc[idx, 'MAP_NAME']
            map_list = [mn.strip() for mn in map_list.split(',')]
            for mn in map_list:
                df_maps_join.at[idx, mn]='CHANGE'
        df_maps_join.to_csv(csv_out, index=True, index_label='DATA_LOCATION_MCMILLEN')

    def join_list(self, v):
        vn = v.to_list()
        vn = list(set(vn))
        vn = ', '.join(vn)
        return (vn)
    def aggregate_rows(self, df, group_by_field, agg_field,**kwargs):
        '''
        Groupby a field (group_by_field), aggregate all unique values in another field (agg_field)
        as a new field with values being unique values as string with commas separating values.
        20240904
        Args:
            csv_in:             path/to/csv source
            csv_out:            path/to/csv_out; can be same as csv_in
            group_by_field:     field to groupby
            agg_field:          field to create unique value comma-separated string
            kwargs:             count = include field with number of values for agg_field in csv_out
                                carry_field = list of field(s) to keep - can include agg field

        Returns:

        '''
        # The method .agg({agg_field: <function>}) will perform <function> over the agg_field
        # i.e. join_list aggregated over map_name column
        groupby_source = df.groupby(group_by_field).agg({agg_field: self.join_list})
        # pulls groupby_field out of index and replaces with numbers (iloc)
        groupby_source = groupby_source.reset_index()

        try:
            # use if group_by_field is a file path and you want filename
            kwargs['extract_filename']
            fnames = [os.path.splitext(ntpath.basename(fp))[0] for fp in groupby_source[group_by_field]]
            groupby_source[group_by_field] = fnames
        except KeyError:
            pass
        try:
            kwargs['count']
            for idx in groupby_source.index:
                t = groupby_source.loc[idx, agg_field]
                t = t.split(',')
                groupby_source.loc[idx, 'NUMBER_OCCURRENCES']= len(t)
        except KeyError:
            pass
        groupby_source = groupby_source.set_index(group_by_field)
        try:
            keep_fld = kwargs['carry_fields']
            keep_fld.append(group_by_field)
            df_join = df.drop_duplicates([group_by_field]).reset_index()
            # Don't bring in Agg Field i.e. map_name
            df_join = df_join[[c for c in df_join.columns if c in keep_fld]]
            # cols_rename = {f"{c}_y":c for c in df.columns if c!=group_by_field}
            groupby_source = groupby_source.merge(df_join, on=group_by_field, how='left')
            # groupby_source = groupby_source.rename(columns=cols_rename)
        except KeyError:
            pass
        return(groupby_source)
    def concatenate_aggregate(self, csv_in, csv_out, split_field, group_by_field, agg_field, **kwargs):
        '''
        Used for multiple aprx ReSourcing wherein need to groupby map_names in each aprx.
        Layer X may be used in 4 different APRXs.  In this case, there will be 4 Layer X
        or DATA_SOURCE rows, one for each aprx and a map_name 'map1,map2,mapn' string for each
        20241016
        Args:
            csv_in:         lyR_in_csv to aggregate
            csv_out:        path/to/final/csv
            split_field:    for instance groupby map_name but per aprx.  so split by aprx and
                            comma sep string map_names for each aprx.
            group_by_field  field to groupby i.e. DATA_SOURCE
            agg_field       field to generate comma separated string of values i.e. map_name
            kwargs:         carry_field = list of field(s) to keep - can include agg field
        Returns:

        '''
        df = pd.read_csv(csv_in)
        split_vals = list(set(df[split_field].to_list()))
        for v in split_vals:
            df_temp = df[df[split_field]==v]
            try:
                keep_fld = kwargs['carry_fields']
                df_temp_agg = self.aggregate_rows(df_temp, group_by_field, agg_field, carry_fields = keep_fld)
            except KeyError:
                df_temp_agg = self.aggregate_rows(df_temp, group_by_field, agg_field)
            df_temp_agg[split_field]=v
            # is_raster = df_temp.drop_duplicates(subset=[group_by_field])
            # is_raster=is_raster['IS_RASTER']
            # df_temp_agg['IS_RASTER']=is_raster.to_list()
            if 'df_concat' not in locals():
                df_concat = copy.copy(df_temp_agg)
            else:
                df_concat = pd.concat([df_concat, df_temp_agg])
        df_concat.to_csv(csv_out)

    def aprx_broken_source_inv2(self, subproject, **kwargs):
        '''
        Step 2 in fixing dumb ESRI path when moved.
        After running step 2, manually create columns and val for .replace
        Then run this to save csv with correct source column
        Args:
            csv_out:        path/to/broken_source_inv

        Returns:

        '''
        try:
            kwargs['lyR_maestro']
            fp_csv_lyR = self.pl_aprx.loc[subproject, 'fp_lyR_maestro']
        except KeyError:
            fp_csv_lyR = self.pl_aprx.loc[subproject, 'fp_lyR_inv']
        df = pd.read_csv(fp_csv_lyR, index_col='DATA_LOCATION_MCMILLEN')
        prop_str_indices = '{}_lyR_indices'.format(subproject)
        indices = getattr(self, prop_str_indices)
        for idx in indices:
            orig=copy.copy(idx)
            t=df.loc[idx,'target']
            r=df.loc[idx,'replace']
            corrected=orig.replace(t,r)
            df.loc[idx,'DATA_LOCATION_MCM_RESOURCE']=corrected
        df.to_csv(fp_csv_lyR)

    def dict_key_utility(self, vals_to_key, the_dict):
        '''
        20241105
        Args:
            vals_to_key:            List of values to key from dictionary
            the_dict:                   dictionary to key original list

        Returns:
            keyed_list              If key, then rekeyed, if none, then original val
        '''
        keyed_list=[]
        for orig in vals_to_key:
            try:
                keyed = the_dict[orig]
            except KeyError:
                keyed = copy.copy(orig)
            keyed_list.append(keyed)
        return(keyed_list)
    def flag_csString_val(self, df_str, col_to_parse, tgt_val, col_to_flag):
        '''
        Adds  True False vals to column where comma sep list val is present
        Args:
            df_str:
            col_to_parse:       column to parse in df
            tgt_val:            i.e. PSP_2024
            col_to_flag:        which col to insert flag

        Returns:

        '''
        df = getattr(self, df_str)
        # creates a list of lists
        csString_orig_list=self.parse_comma_sep_list(col_to_parse,oop=df_str)
        if col_to_flag not in df.columns:
            df[col_to_flag]=False
        for idx_int, idx in enumerate(df.index):
            if tgt_val in csString_orig_list[idx_int]:
                df.at[idx, col_to_flag]=True
            else:
                pass
        return(df)
    def custom_merge(self, df_str_src, df_str_tgt, tc_src, tc_tgt, cols_update,
                     concat_omitted=False, overwrite_var=False, **kwargs):
        '''
        Update df from another df, specifically df_lyR_aprx to update maestro
        Useful to populate ALL layers from lyr_aprx to maestro
        ZU 20250416
        Args:
            df_str_src:         self explanatory i.e. df_lyr_APRX
            df_str_tgt:         self explanatory i.e. df_maestro
            tc_src:             target col
            tc_tgt:             target col
            cols_update:        list of cols
            overwrite_var:       False if only update NA, True if update all overlapping (see docs .update)
            concat_ommitted:    if
            **kw['subset']:     any lengh dict with key:val = col_name:value
        Returns:
            df_tgt:             updated df_tgt
        '''
        df_src=getattr(self, df_str_src)
        df_tgt=getattr(self, df_str_tgt)
        if df_src.index.name!=tc_src:
            df_src.reset_index().set_index(tc_src, inplace=True)
        if df_tgt.index.name!=tc_tgt:
            df_tgt.reset_index().set_index(tc_tgt, inplace=True)
        # If subsettig by target value in df_src
        try:
            d = kwargs['subset']
            for k,v in zip(*d.items()):
                if 'subset' not in locals():
                    subset=df_src[df_src[key]==val]
                else:
                    subset = pd.concat(subset, df_src[df_src[key]==val])
            df_src=copy.copy(subset)
        except KeyError:
            pass
        committed_idx=list(set(df_tgt.index).intersection(df_src.index))
        omitted_idx=list(set(df_src.index)-set(df_tgt.index))
        df_omitted = df_src.loc[omitted_idx, cols_update]

        # Update cols on intersected if value for columns
        df_committed = df_src.loc[committed_idx, cols_update]
        df_tgt.update(df_committed, overwrite=overwrite_var)
        if concat_omitted:
            df_omitted.reset_index(inplace=True)
            df_tgt.reset_index(inplace=True)
            df_tgt=pd.concat([df_tgt, df_omitted])
        setattr(self, df_str_tgt, df_tgt)
class AgolAccess(commonUtils):
    '''
    Basic init for AGOL access
    '''

    def __init__(self, prj_file, subproject_str, fp_csv_agol):
        '''
        need to add credentials like a key thing.  hardcoded currently
        '''
        super().__init__(prj_file, subproject_str)
        u_name = 'uhlmann_mcm'
        p_word = 'Mmleciln138!'
        setattr(self, 'mcm_gis',  GIS(username = u_name, password = p_word))
        print('Connected to {} as {}'.format(self.mcm_gis.properties.portalHostname, self.mcm_gis.users.me.username))
        # dictionary that can be expanded upon
        # FOUND NO difference between feature layer collection and feature layer.  All feature layers were
        # detected as both with mcm_gis.content.search(item_type = <collection or layer>)
        self.item_type_dict = {'shapefile': 'Shapefile',
                                'feature_layer': 'Feature Layer',
                                'webmap': 'Web Map',
                                'vector_tile': 'Vector Tile Service',
                                'web_map':'Web Map'}
        group_id_dict = {'KRRP_Geospatial': 'a6384c0909384a43bfd91f5d9723912b',
                        'mcmjac_everyone': 'b61fb4a0c0a944ebb3dd1558d4887e7f',
                        'sacramento_canal':'eb6b401c468448a39c0aa522461ad3f8',
                         'SFT_FERC_Relicensing_McMillen':'cda69f86424c42b3b79e777f53a00bfa'}
        wkid_dict = {'CA_sp2':6416,
                        'webmercator': 3857}
        self.group_id_dict = group_id_dict
        df_agol = pd.read_csv(fp_csv_agol, index_col = 'ITEM')
        setattr(self, 'df_agol', df_agol)
        setattr(self, 'fp_csv_agol', fp_csv_agol)

    def get_group(self, group_key):
        '''
        hardcoded. update if more groups become necessary.
        DELETE ZU 20210827
        '''
        group_id = self.group_id_dict[group_key]
        group_obj = Group(getattr(self, 'mcm_gis'), group_id)
        setattr(self, group_key, group_obj)

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
        print(itemType)
        # QUERY STRING
        # If Group (default KRRC_Geospatial), add to query str
        if group_name is not None:
            group_id = self.group_id_dict[group_name]
            query_str = 'owner: uhlmann_mcm AND group:{}'.format(group_id)
        else:
            query_str = 'owner: uhlmann_mcm'
        try:
            title = kwargs['title']
            query_str = '{} AND title: {}'.format(query_str, title)
        except KeyError:
            pass

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
            setattr(self,'content_string',content_str)
            items = self.mcm_gis.content.search(query_str,
                                            item_type = itemType, max_items = 250)
            setattr(self, content_str, items)
            # filtered tags attribute

    def take_action_agol(self, df_agol_str, action_type, user_content_str,
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
        df_agol = getattr(self, df_agol_str)
        ct = 1
        # ACCESS AGOL items
        user_content = getattr(self, user_content_str)
        if action_type == 'added_item':
            # Ensure shapefile not feature
            if not 'shapefile' in user_content_str:
                print('user content needs to be shapefile\nNOT RUNNING method')
            else:
                titles = [content_item.title for content_item in user_content]
                for indice in self.indices:
                    if indice in titles:
                        df_agol.at[indice, 'ADDED_AGOL'] = True
                        # print('TITLE:{}TYPE:{}'.format(title, type(title)))
                    else:
                        df_agol.at[indice, 'ADDED_AGOL'] = False

                    # if we want to remove vals in ACTION col
                    try:
                        col_val = kwargs['update_action']
                        df = update_comma_sep_vals(df, title, 'ACTION', col_val)
                    except:
                        pass
        if action_type == 'share_status':
            group_str = 'user_content_{}_feature_layer'.format(group)
            # Get group content
            try:
                user_content_group = getattr(self, group_str)
            except AttributeError:
                self.identify_items_online(['feature'])
                user_content_group = getattr(self, group_str)
            list1 = copy.copy(self.indices)
            list2 = [item.title for item in user_content_group]
            set1 = set(list1)
            set2 = set(list2)
            df1_present_df2_absent = set1.difference(set2)
            # SET all to True then REPLACE with False
            for indice in self.indices:
                df_agol.at[indice, 'SHARED'] = True
            # REPLACE with False
            for indice in list(df1_present_df2_absent):
                df_agol.at[indice, 'SHARED'] = False
        if action_type == 'publish_status':
            user_content_shp = getattr(self, 'user_content_shapefile')
            user_content_feat = getattr(self, 'user_content_feature_layer')
            list1 = [item.title for item in user_content_shp]
            list2 = [item.title for item in user_content_feat]
            set1, set2 = set(list1), set(list2)
            not_published = list(set1.difference(set2))
            # SET all to True then REPLACE with False
            for indice in self.indices:
                df_agol.at[indice, 'PUBLISHED'] = True
            # REPLACE with False
            for indice in not_published:
                df_agol.at[indice, 'PUBLISHED'] = False

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
                    df_agol.at[title, 'PUBLISHED'] = False

                # if we want to remove vals in ACTION col
                try:
                    col_val = kwargs['update_action']
                    df_agol = update_comma_sep_vals(df_agol, title, 'ACTION', col_val)
                except:
                    pass
        if action_type == 'add_data':
            for indice, indice_iloc in zip(self.indices, self.agol_indices_iloc):
                agol_dir = self.df_agol.loc[indice, 'AGOL_DIR']
                zip_dir = os.path.join(agol_dir,'zip')
                shp = os.path.join(zip_dir, '{}.zip'.format(indice))

                # TAGS
                tags_df = self.parse_comma_sep_list('TAGS',oop='df_agol')
                # subset tags in index
                tags = tags_df[indice_iloc]
                snippet = self.df_agol.loc[indice,'SNIPPET']

                print(tags)
                properties_dict = {'type':'Shapefile',
                                    'title':indice,
                                    'tags':tags,
                                    'snippet':snippet}
                print('ADDING TO AGOL: \n{}'.format(shp))
                fc_item = self. mcm_gis.content.add(properties_dict, data = shp)
                # fc_item.share(groups = 'a6384c0909384a43bfd91f5d9723912b')
                print('iloc = {} \\n fc_item {} '.format(indice_iloc, fc_item))

        if action_type == 'publish':
            for content_item in user_content:
                title = content_item.title
                if title in self.indices:
                    try:
                        wkid = kwargs['wkid']
                        # wkid = self.df_agol.loc[title, 'WKID']
                        d =   {"name":title, "description":"Published in API with wkid specified","maxRecordCount":5000,
                                "targetSR":{"wkid":wkid}}
                        # d =   {"name":title, "description":"Published in API with wkid specified","maxRecordCount":5000,
                        print('PUBLISHING: {}'.format(title))
                        #         "copyrightText":"new copyright","targetSR":{"wkid":6416}}
                        content_item.publish(publish_parameters=d)
                    except KeyError:
                        d =   {"name":title,"maxRecordCount":5000}
                        print('PUBLISHING: {}'.format(title))
                        #         "copyrightText":"new copyright","targetSR":{"wkid":6416}}
                        content_item.publish(publish_parameters=d)
                else:
                    pass
                    # print('item title {} did not match queried result on agol --> did NOT publish'.format(title))
                # if we want to remove vals in ACTION col
                try:
                    col_val = kwargs['update_action']
                    df_agol = update_comma_sep_vals(df_agol, title, 'ACTION', col_val)
                except:
                    pass
        if action_type == 'share':
            # To account for any ITEMS from df that are NOT online as features
            indices_remaining = copy.copy(self.indices)
            # get group id for sharing
            try:
                group_obj = getattr(self, group)
            except AttributeError:
                self.get_group(group)
                group_obj = getattr(self, group)
            for content_item in user_content:
                title = content_item.title
                if title in self.indices:
                    print('SHARING: {}'.format(content_item))
                    content_item.share(groups = [group_obj], org = True)
                    df_agol.at[title, 'SHARED'] = True
                    indices_remaining.remove(title)
                else:
                    pass
                # if we want to remove vals in ACTION col
                try:
                    col_val = kwargs['update_action']
                    df_agol = update_comma_sep_vals(df_agol, indice, 'ACTION', col_val)
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
                    df_agol.at[item_title, 'TAGS_CURRENT'] = tags_str
                except KeyError:
                    print('Item {} is not present in DF'.format(item_title))
        if action_type in ['update_tags']:
            content_items = [item for item in user_content if item.title in self.indices]
            for content_item in content_items:
                title = content_item.title
                try:
                    new_tags = df_agol.loc[title, 'TAGS']
                    # Get list from string
                    new_tags = ductape_utilities.parse_csl(new_tags, False)
                    print(new_tags)
                    update_dict = {'tags':new_tags}
                    content_item.update(update_dict)
                except KeyError:
                    print('Item {} is not present in DF'.format(item_title))
        if action_type in ['new_snippets']:
            # Replace with entirely new snippet
            content_items = [item for item in user_content if item.title in self.indices]
            for content_item in content_items:
                title = content_item.title
                try:
                    new_snippet = df_agol.loc[title, 'SNIPPET']
                    orig_snippet = content_item.snippet

                    update_dict = {'snippet':new_snippet}
                    content_item.update(update_dict)
                except KeyError:
                    print('Item {} is not present in DF'.format(item_title))
        if action_type in ['append_snippets']:
            # For appending SOURCE  and SOURCE_ORIGINAL key pair after publishing
            # and manually populating snippet field in agol_inventory
            #The original snippet is pulled from
            # the Id Purp in xml shapefile and I replaced this with customish,
            # manually copied/created snippet + SOURCE info.
            # ZU 20220928
            content_items = [item for item in user_content if item.title in self.indices]
            for content_item in content_items:
                title = content_item.title
                try:
                    new_snippet = df_agol.loc[title, 'SNIPPET']
                    orig_snippet = content_item.snippet
                    try:
                        sub = orig_snippet.split('\n')
                        for s in sub:
                            if (s[0:6] =='SOURCE') & ('CONTACT' not in s):
                                new_snippet = '{}\n{}'.format(new_snippet, s)
                            else:
                                pass
                    except AttributeError:
                        pass
                    update_dict = {'snippet':new_snippet}
                    content_item.update(update_dict)
                except KeyError:
                    print('Item {} is not present in DF'.format(item_title))
        if action_type in ['update_group_categories']:
            # Create a JSON array with categories from dataframe to pass to
            # assign_to_items method
            # ZU 20220626
            matched = [c for c in user_content if c.title in self.indices]
            dict_final = []
            for it in matched:
                title = it.title
                cats = self.df_agol.loc[title, 'CATEGORIES']
                try:
                    cats = cats.split(',')

                    cats = [c.replace(' ','') for c in cats]
                    cats_full = ['/Categories/{}'.format(c) for c in cats]
                    id = it.itemid
                    dc = {id:{'categories':cats_full}}
                    if 'dict_final' not in locals():
                        dict_final = [dc]
                    else:
                        dict_final.append(dc)
                    # Should exist if running this function, but check
                    try:
                        group_item = getattr(self, 'krrp_geospatial')
                    except AttributeError:
                        print('run getgroup with krrp_geospatial first')
                    # pass JSON Array to assign_to_items method
                    # FYI to access help  >>>help(group_item.assign...) Could not find online documentation
                    group_item.categories.assign_to_items(items=dict_final)
                except AttributeError:
                    print('{} Has no categories to set'.format(title.upper()))
        # keep count going for item_type
        ct += 1
        setattr(self, df_agol_str, df_agol)

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
            tags = self.parse_comma_sep_list('TAGS',oop=df_str)
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
            fc_item = self. mcm_gis.content.add(properties_dict, data = shp)
            # fc_item.share(groups = 'a6384c0909384a43bfd91f5d9723912b')
            print('ct = {} \\n fc_item {} '.format(idx, fc_item))

    def create_df_agol(self, it_vals_key = ['web_map', 'vector_tile'],
                        prop_name = 'df_agol_raw'):
        '''
        Needs work.  Currently just creats a new df based on it_vals_key.
        Refer to gh item_type_dict for more options. 20220627
        ARGS
        it_vals_key         list of item type keys to get item types for search
        prop_name           setattr(prop_name, df_agol_raw)
        '''
        df_agol = getattr(self, 'df_agol')
        it_vals = [self.item_type_dict[it] for it in it_vals_key]

        group_id = self.group_id_dict['KRRP_Geospatial']
        query_str = 'owner: uhlmann@mcmjac.com AND group:{}'.format(group_id)

        for idx, it in enumerate(it_vals):
            items = self.mcm_gis.content.search(query_str,
                                            item_type = it, max_items = 500)
            n = [i.title for i in items]
            nv = [i.numViews for i in items]
            tg = [i.tags for i in items]
            sn = [i.snippet for i in items]
            dsc = [i.description for i in items]
            it = [it_vals_key[idx]] * len(items)
            if not it == 'Shapefile':
                shp = [False] * len(items)
                pb = [True] * len(items)
            else:
                shp = [True] * len(items)
                pb = [False] * len(items)
            df_temp = df = pd.DataFrame(np.column_stack([n, nv, tg, sn, dsc, shp, pb, it]),
                                columns = ['ITEM', 'NUM_VIEWS', 'TAGS', 'SNIPPET',
                                            'DESCRIPTION', 'SHAPEFILE', 'PUBLISHED',
                                            'ITEM_TYPE'])
            if 'df_agol_raw' in locals():
                df_agol_raw = df_agol_raw.append(df_temp)
            else:
                df_agol_raw = copy.copy(df_temp)
        df_agol_raw = df_agol_raw.set_index('ITEM')
        setattr(self, 'df_agol_raw', df_agol_raw)
