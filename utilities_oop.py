import copy
import os
import pandas as pd
import numpy as np
from pathlib import Path
from time import gmtime, strftime
import time
import math
import ntpath

class utilities(object):
    '''
    ARGS
    df_index_col            ITEM is default for use with Klamath.
    '''
    def __init__(self,  parent_dir, target_col):
        '''

        Args:
            parent_dir:
            target_col:
        '''
        self.parent_dir=parent_dir
        self.target_col=target_col
    def subdir_inventory(self, ftype_filters=['.gdb'],exclude_subdir = [], **kwargs):
        '''
        Updated 20240620 for general usage
        Args:
            parent_dir:             directory to inventory
            target_col:             for matching existing rows
            filter_by_ftype         boolean - not developed; hardcoded filebype filters in list in subdir_inventory_scan
            **kwargs:               new_inventory:    step 1 in standalone inventory
                                    update_inventory:  for adding to existing inventory

        Returns:
            saves csv or returns df

        '''
        from time import gmtime, strftime
        # fp_logfile = os.path.join(parent_dir, 'subdir_inventory_log.log')
        ftype_filters.extend([t.upper() for t in ftype_filters])
        try:
            kwargs['just_shp']
            ftype_filters.extend(['.cpg','.dbf','.idx','.shx'])
        except KeyError:
            pass
        setattr(self, 'ftype_filters', ftype_filters)
        if isinstance(exclude_subdir,list):
            setattr(self, 'exclude_subdir', exclude_subdir)
        elif isinstance(exclude_subdir, str):
            setattr(self, 'exclude_subdir', [exclude_subdir])
        try:
            new_csv = kwargs['new_inventory']
            df_subdir = self.subdir_inventory_create()
            df_subdir = df_subdir.set_index(self.target_col)
            if not os.path.exists(new_csv):
                df_subdir.to_csv(new_csv)
            else:
                print('csv already exists; did not save')
            return(df_subdir)
        except KeyError:
            pass
        try:
            updated_csv = kwargs['update_inventory']
            df_orig = pd.read_csv(updated_csv, index_col = self.target_col)
            df_subdir = self.subdir_inventory_create()
            # run through above function
            df_subdir = df_subdir.set_index(self.target_col)
            print('FUCK', df_subdir)
            df_concat = pd.concat([df_orig, df_subdir])
            # In the case that updating a folder that has already been processed with this function
            # this will retain the first row, and remove the new inventory
            df_concat = df_concat[~df_concat.index.duplicated(keep='first')]
            df_concat.to_csv(updated_csv)
        except KeyError:
            pass


    def subdir_inventory_create(self):
        '''
        Updated 20240620 for general usage (non .shp)

        Args:
            parent_dir:             directory to inventory
            target_col:             for matching existing rows
            fp_logfile:             string path to logfile
            filter_by_ftype         boolean - not developed; hardcoded filebype filters in list in subdir_inventory_scan
        Returns:
            df_subdir               dataframe inventory
        '''
        # need to hardcode basically. be better as aclass and methods
        self.parent_dir_depth = len(os.path.normpath(self.parent_dir).split(os.sep))
        fname, fp, subdir_name, filetype, base_subdir, time_modified, file_size =  self.subdir_inventory_scan(self.parent_dir)
        col_list = ['ITEM', 'BASE_SUBDIR', 'FINAL_SUBDIR', 'FILETYPE','FILESIZE','TIME_MODIFIED',self.target_col]
        cols = np.column_stack([fname, base_subdir, subdir_name, filetype, file_size, time_modified, fp])
        df_subdir = pd.DataFrame(cols, columns=col_list)
        return(df_subdir)
    def subdir_inventory_scan(self, parent_dir):
        '''
        Inventory directories and subdirectories for ALL files.  ZU 20240620.
        Created for Tacoma Hatchery for Jodi Burns
        C:\Box\MCM Projects\City of Tacoma\24-068_Cowlitz Trout Hatchery Remodel\4.0 Data Collection

        Args:
           parent_dir:             directory to inventory
            target_col:             for matching existing rows
            fp_logfile:             string path to logfile
            ftype_filters        list; file extentsion to SKIP - default = ['.gdb']
            parent_dir_depth        depth of directory i.e. path/to/this/dir = 4

        Returns:
            feat_name:          list of feature names (shapfefiles)
            feat_path:          list of path/to/shapefile
            subdir_name         final subdirectory where file is located
            filetype            filetype i.e. .xml, .pdf, etc.
            base_subdir_list    first directory down from parent dir (or parent dir if no subdir)

        '''
        # https://stackoverflow.com/questions/49664518/python-2-7-using-scandir-to-traverse-all-sub-directories-and-return-list
        # https://stackoverflow.com/questions/30214531/basics-of-recursion-in-python
        feat_path,feat_name,filetype,subdir_name, base_subdir_list, file_size, time_modified = [],[],[],[],[],[],[]
        subdir_list =[]
        # to use for top subparent dir list
        for f in os.scandir(parent_dir):
            if f.is_file():
                file_ext = os.path.splitext(f)[-1]
                # FIND subdir by triggering (or not) exception below
                # base_subdir = directory name one deeper than parent
                try:
                    # try triggering exception - need idx + 1 because f.path inncludes filename
                    os.path.normpath(f.path).split(os.sep)[self.parent_dir_depth + 1]
                    base_subdir = os.path.normpath(f.path).split(os.sep)[self.parent_dir_depth]
                except IndexError:
                    # in root of parent_dir
                    base_subdir = os.path.normpath(parent_dir).split(os.sep)[-1]
                if file_ext not in self.ftype_filters:
                    feat_name.append(f.name)
                    feat_path.append(f.path)
                    filetype.append(file_ext)
                    subdir_name.append(Path(f.path).parent.name)
                    base_subdir_list.append(base_subdir)
                    time_modified.append(strftime(r'%Y-%m-%d', time.gmtime(os.path.getmtime(f.path))))
                    # 1000/1024 because Kibibyte not KiLibyte - https://superuser.com/questions/1528837/file-explorer-size-property-less-than-file-size-in-properties
                    # divide by 1000 to go bytes to kibibyte
                    size_math = Path(f.path).stat().st_size * (1000 / 1024) / 1000
                    file_size.append(math.ceil(size_math))
                else:
                    pass
                    # logging.info('SKIPPED THIS FILE due to file type filter: {}'.format(f.path))
            # Find directory NOT .zip (needs work - ZU 202406200
            elif (f.is_dir()) & (f.name[-4:] == '.zip'):
                # base_subdir = directory name one deeper than parent
                try:
                    # try triggering exception - need idx + 1 because f.path inncludes filename
                    os.path.normpath(f.path).split(os.sep)[self.parent_dir_depth + 1]
                    base_subdir = os.path.normpath(f.path).split(os.sep)[self.parent_dir_depth]
                except IndexError:
                    # in root of parent_dir
                    base_subdir = os.path.normpath(self.parent_dir).split(os.sep)[-1]
                feat_name.append('{}.zip'.format(f.name))
                feat_path.append('{}.zip'.format(f.path))
                subdir_name.append(Path(f.path).parent.name)
                filetype.append(None)
                base_subdir_list.append(base_subdir)
                time_modified.append(strftime(r'%Y-%m-%d', time.gmtime(os.path.getmtime(f.path))))
                file_size.append(math.floor(os.path.getsize(f.path / 1000)))
            elif (f.is_dir()) & (os.path.normpath(f.path) in self.exclude_subdir):
                pass
            # keeps running if another folder encountered
            elif f.name[-4:] != r'.gdb':
                t0,t1,t2,t3,t4,t5,t6 = self.subdir_inventory_scan(f.path)
                feat_name.extend(t0)
                feat_path.extend(t1)
                subdir_name.extend(t2)
                filetype.extend(t3)
                base_subdir_list.extend(t4)
                time_modified.extend(t5)
                file_size.extend(t6)
        return(feat_name, feat_path, subdir_name, filetype, base_subdir_list,time_modified,file_size)

    def aggregate_rows(self, csv_in, csv_out, group_by_field, agg_field, **kwargs):
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

        Returns:

        '''
        df = pd.read_csv(csv_in)

        def join_list(v):
            vn = v.to_list()
            vn = list(set(vn))
            vn = ', '.join(vn)
            return (vn)

        groupby_source = df.groupby(group_by_field).agg({agg_field: join_list})
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
        groupby_source.to_csv(csv_out)
