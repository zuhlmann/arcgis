import os
import pandas as pd
import math
import sys
try:
    sys.path = [p for p in sys.path if '86' not in p]
    import arcpy
except ModuleNotFoundError:
    print('Running utilities without Arcpy')
import numpy as np
import datetime
import time
import glob
import copy
# from compare_data import *

def show_table(display_preference):
    '''
    ARGS:
    display_preference:  desc or path. string
    '''
    from tabulate import tabulate
    paths_table = """C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/data_inventory_and_tracking/path_list.csv"""
    # use index_col = 0 for show_table.  So .iloc values will accompany table
    df = pd.read_csv(paths_table, index_col = 0)
    df.index.name = 'index'
    # somehow need to be accessed this way
    display_list = ['alias']
    display_list.append(display_preference)
    df2 = df[display_list]
    table = tabulate(df2, headers = 'keys', colalign = ["left",  "left"], tablefmt = "github")
    # display table with options for filepaths
    print('')
    print(table)
def get_path(idx, path_type):
    '''
    args:
    idx         integer for iloc or string of alias
    '''
    paths_table = """C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/data_inventory_and_tracking/path_list.csv"""
    df = pd.read_csv(paths_table, index_col = 1)
    # if passing index with iloc
    col_dict = {'gdb':'path_gdb',
                'csv':'path_csv'}
    col_name = col_dict[path_type]
    if isinstance(idx, int):
        path_out = df.iloc[idx][col_name]
    # if passing string of alias
    else:
        path_out = df.loc[idx][col_name]
    return(path_out)

def update_path_dict(idx_list, path_type, paths_table):

    kv_scratch_gdb = kwargs['pro_project_dict']['gdb']
    path_gdb_dict.update(kv_scratch_gdb)
    df = pd.read_csv(paths_table, index_col = 1)
    # if passing index with iloc
    col_dict = {'gdb':'path_gdb',
                'csv':'path_csv'}
    col_name = col_dict[path_type]
    for idx in idx_list:
        path_out = df.loc[idx][col_name]


def add_table_entry(alias, desc, fp):
    '''
    can add table entry by passing three required args
    ARGS
    alias       string. alias should be 'fp_<descriptive name>'
    desc        description of feature class
    fp          file path to dataset
    '''
    paths_table = """C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/data_inventory_and_tracking/path_list.csv"""
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
    '''
    remove table entry by passing alias
    ARGS
    alias       string. alias
    '''
    paths_table = """C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/data_inventory_and_tracking/path_list.csv"""
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
    paths_table = """C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/data_inventory_and_tracking/path_list.csv"""
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

def list_unique_fields(fp_feat, field, data_storage, **kwargs):
    '''
    ZRU 6/1/20
    ARGS:
    fp_feat         file path to feature (string).  could prob be feature layer too
    field           N = 1 or more field names from attribute table.  List of strings
                    Individual string will also be handled if just one field
    data_storage    string.  options: 'in_memory', 'feature_layere', 'none'
    kwargs          currently, specify 'name' Keywork = Value pair when specifying
                    data_storage value not 'none'
    '''
    import arcpy
    import pandas as pd

    # turn FIELD into list if not a list
    if isinstance(field, list):
        pass
    else:
        field = [field]
    # try except and kwargs should be removed.  Apparently da.searchcursor only
    # accepts feature classes or tables - not feature layers.  False statment??
    if data_storage == 'in_memory':
        feat = 'in_memory\\{}'.format(kwargs['name'])
        arcpy.MakeFeatureLayer_management(fp_feat, feat)
    elif data_storage == 'feature_layer':
        feat = kwargs['name']
        arcpy.MakeFeatureLayer_management(fp_feat, feat)
    elif data_storage == 'none':
        feat = fp_feat

    with arcpy.da.SearchCursor(feat, field) as cursor:
        rows = [row for row in cursor]
        vals = zip(*rows)
        for idx, field in enumerate(field):
            if 'dict' not in locals():
                dict = {field : vals[idx]}
            else:
                dict[field] = vals[idx]
        df = pd.DataFrame(dict)
    return(df)
def where_clause_create_p1(field,  vals, **kwargs):
    '''
    ZRU 6/11/2020
    should be expanded.  Follow comments at the end to combine multiple lists
    field       currently just accepts single string
    vals         list of strings or ints.  Make sure to pass int as a list even if single item
    kwargs      currently just val pair 'operator' = [pick val in operator_dict]
    RETURNS
    where_clause_components     list of string or strings
    '''

    if isinstance(vals[0], str):
        where_clause_components  =  ["({field} = '{val}')".format(field=field, val=val)
                                            for val in vals]
    else:
        try:
            # get operator type from kwarg operator = operator
            operator = kwargs['operator']
            operator_dict = {'equal':'=', 'gt':'>', 'lt':'<'}
            operator = operator_dict[operator]
            where_clause_components = ["({field} {operator} {val})".format(field=field, operator = operator, val=vals)
                                                                            for val in vals]
        except KeyError:
            print('operator string not valid.  gt = > lt = < equal = =')
            # Note: nest in list for consistency when stringing together multiple calls
    return(where_clause_components)
    # 1) take output and run below line to combine with OR conditional.  Change
    # to AND if need be
    # where_clause_location = ' OR '.join(where_clause_location)
    # 2) Try adding this in future to ensure field delimeter instead of if else statment
    # field_delim = arcpy.AddFieldDelimiters(fp, field)
    # # check here and here to find code and learn unicode background:
    # # https://gis.stackexchange.com/questions/153444/using-select-layer-by-attribute-in-arcpy
    # # https://pro.arcgis.com/en/pro-app/help/data/geodatabases/overview/a-quick-tour-of-unicode.htm

def custom_select(fp_or_feat, field, target_vals):
    '''
    used to get indices for selecting features.  getting objectid from dataframe
    easier than running multiple arcpy and CopyFeature_management functions.
    ZRU 6/2/2020
    Needs to be generalized.
    ARGS:
    fp_or_feat              seems to work with either lyr object or file path
    field                   currently only takes one field as str
    target_vals             list of vals
    RETURNS:
    df                      dataframe which will be used to extract indices/objectid
    '''
    with arcpy.da.SearchCursor(fp_or_feat, ['OBJECTID', field]) as cursor:
        # This row[0] will access teh object to grab the field.  If n fields > 1, n idx >1
        objectid, source_val = [], []
        for row in cursor:
            objectid.append(row[0])
            source_val.append(row[1])
    df = pd.DataFrame(np.column_stack([objectid, source_val]), columns = ['OBJECTID', 'val'],  index = objectid)
    df = df[df.val.isin(target_vals)]
    return(df)
def feature_table_as_csv(fp_in, fp_csv, field_names):
    '''
    feed it field names in a list of strings and returns csv of attributes
    table. Updated ZRU 10/9/2020
    ARGS:
    fp_in       yeah
    fp_csv      the csv path for table
    field_name  field names - list of strings
    '''
    # hack
    field_names_objid = ['OBJECTID']
    for item in field_names:
        field_names_objid.append(item)
    with arcpy.da.SearchCursor(fp_in, field_names_objid) as cursor:
        # rows creates a list of tuples where len of each tuple = number of field names + 1 (objectid)
        # zip transects pos 1,2...n for number of fields + 1 yielding a list of size n = n rows
        # for each of the fields + objectid
        rows = [row for row in cursor]
        field_tuple = zip(*rows)
        df = pd.DataFrame(np.column_stack(field_tuple), columns = field_names_objid)
        pd.DataFrame.to_csv(df, fp_csv)
def add_path_multiIndex(df, layer, loc_idx, new_path, append):
    '''
    Fix hacky if/else to be vararg or something better.  Also should be a class
    ZRU 5/14/2020
    ARGS:
    df          dataframe
    layer       layer name string
    loc_idx     either 1 or 2 (int) to be formatted to "loc1" or "loc2"
    new_path    path to be addes
    append      True or False.  False will print dataframe
    '''
    try:
        isinstance(loc_idx, int)
    except:
        print('loc varible must be an integer, either 1 or 2')

    level_idx = 'loc{}'.format(loc_idx)
    try:
        if append == True:
            df.loc[(layer, level_idx), 'Original_Location'] = new_path
            return df
        else:
            print(df.loc[(layer, level_idx), 'Original_Location'])
    except KeyError:
        print('layer key does not exist i.e. FERC Boundary.  Check spelling')

def update_field(fp_fcs, field, incr = 1, sequential = True, fp_csv = 'path/to/csv', **kwargs):
    '''
    Fixed up to include add list of text to new field as option 2.
    the default is adding sequential numbers (for page_num) ZU 20210304
    ARGUMENTS
    fp_fcs              file path to feat class
    field               field for da.searchCursor AND if adding text, set sequential
                        to FALSE and pass a path to csv.  Field will need to match
                        on csv and for attribute field in fc
    incr                option to change
    sequential          Set to False to use the csv updating protocol
    fp_csv              pass this if adding text field to fp_fcs
    '''

    existing_fields = [f.name for f in arcpy.ListFields(fp_fcs)]
    if sequential:
        if field not in existing_fields:
            arcpy.AddField_management(fp_fcs, field, 'SHORT')
            print(r'----Adding field {} ----'.format(field))

        field = [field]
        with arcpy.da.UpdateCursor(fp_fcs, field) as cursor:
            ct = 1
            for row in cursor:
                row[0] = ct
                cursor.updateRow(row)
                ct += incr
        del cursor
    else:
        df = pd.read_csv(fp_csv)
        val_list = df[field].to_list()
        # CHECK IF FIELD EXISTS BEFORE CREATING
        # Arc will replace spaces with _
        field = field.replace(' ','_').replace('.','')
        print(field)
        print(existing_fields)
        if field not in existing_fields:
            try:
                data_type = kwargs['data_type']
                arcpy.AddField_management(fp_fcs, field, data_type)
            except KeyError:
                arcpy.AddField_management(fp_fcs, field, 'TEXT', field_length = 254)
            print(r'----Adding field {} ----'.format(field))
        else:
            pass
        field = [field]
        with arcpy.da.UpdateCursor(fp_fcs, field) as cursor:
            print('----Updating Cursor ---')
            ct = 1
            for row, val in zip(cursor, val_list):
                try:
                    data_type = kwargs['data_type']
                    if data_type in ['SHORT', 'LONG']:
                        val = int(val)
                    elif data_type in ['FLOAT', 'DOUBLE']:
                        val = float(val)
                except:
                    pass
                print(r'{}. Original Val: {} ---- New Val: {}'.format(ct, row[0], val))
                row[0] = val
                ct+=1
                cursor.updateRow(row)
        del cursor

def copy_with_fields(in_fc, out_fc, keep_fields, where=''):
    """
    Previously located in arcpy_script_tools_uhlmann/field_mapping_fc_to_fc
    ZU 20211019
    Required:
        in_fc -- input feature class
        out_fc -- output feature class
        keep_fields -- names of fields to keep in output

    Optional:
        where -- optional where clause to filter records
    """
    fmap = arcpy.FieldMappings()
    fmap.addTable(in_fc)

    # get all fields
    fields = {f.name: f for f in arcpy.ListFields(in_fc)}

    # clean up field map
    for fname, fld in fields.items():
        if fld.type not in ('OID', 'Geometry') and 'shape' not in fname.lower():
            if fname not in keep_fields:
                fmap.removeFieldMap(fmap.findFieldMapIndex(fname))

    # copy features
    path, name = os.path.split(out_fc)
    arcpy.conversion.FeatureClassToFeatureClass(in_fc, path, name, where, fmap)

def buffer_and_create_feat(fp_line, fp_out, buff_dist, line_end_type = 'ROUND', dissolve_option = 'NONE'):
    '''
    ZRU 6/24/2020
    buffer and output file
    ARGS:
    '''
    # Attrocious hack to account for my lack of fixing file path slash issue with windows and python
    # try except to handle both .shp and feat classes from gdb
    try:
        feat = fp_line.split('/')[-1].split('\\')[-1].split('.')[-2]
    except IndexError:
        feat = fp_line.split('/')[-1].split('\\')[-1]
    arcpy.MakeFeatureLayer_management(fp_line, feat)
    fp_temp = os.path.join(get_path('fp_scratch'), 'temp_buff')
    arcpy.Buffer_analysis(feat, fp_temp, buff_dist, 'FULL', line_end_type, dissolve_option)
    # arcpy.Union_management()
    # os.path.remove

def field_mappings(fp_target, fp_append, mapping_csv, fp_out, unmapped):
    '''
    I mostly hate FieldMappings because we have to hack around for customization.
    In this instance in order to include BOTH the mapped fields that needed name
    changes essentially AND the target fp's unmatched fields I had to attempt
    the if unmapped: portion.  If probs arise it seems to be from if else elif
    in this area.  might need to accept and translate more types
    ARGS:
    fp_target           file path of target fc
    fp_append           file path of append fc
    mapping_csv         .csv file with field names and such (check description)
                        csv has these fields: 1) target 2) append 3) mapping
                        4) new_field_name.  1 is the target field name.
                        2 the append field name 3 if append field is to be mapped
                        this field will have target field which to map corresponding
                        append field 4 new field name for mapped field. IF not
                        mapping - then set value to 'discard'.
    fp_out              file path out
    unmapped            Boolean.  if True then include unmapped fields from target.
                        this will add ALL fields from target and set those vals
                        in fp_append to NULL since presumably those values do not
                        exist if they were not mapped.  This option retains mapped
                        fields as well.
    '''
    df = pd.read_csv(mapping_csv)
    # create notnull mask
    temp1 = df['append'].notnull()
    temp2 = df['mapping']!='discard'
    notnull = temp1 & temp2
    target_fields = df['mapping'][notnull].tolist()
    append_fields = df['append'][notnull].tolist()
    new_field_names = df['new_field_name'][notnull].tolist()

    # if we want to include unmapped fields from target
    if unmapped:
        # get all target fields and cast from list to set
        arcpy.MakeFeatureLayer_management(fp_append, 'append_lyr')
        fp_append = 'append_lyr'
        fields = arcpy.ListFields(fp_target)
        # unsure if encodiing is necessary
        target_names_unmapped_all = [field.name.encode('utf-8') for field in fields]
        target_type_unmapped_all = [field.type for field in fields]
        # create dataframe for selecting type
        df = pd.DataFrame(np.column_stack([target_names_unmapped_all, target_type_unmapped_all]), columns = ['field_name', 'field_type'])
        target_names_unmapped_set = set(target_names_unmapped_all)
        target_set = set(target_fields)
        # remove mapped target values
        target_names_unmapped_set.difference_update(target_set)
        target_names_unmapped_list = list(target_names_unmapped_set)
        target_types_unmapped = df[df['field_name'].isin(target_names_unmapped_list)].field_type.tolist()
        target_names_unmapped = df[df['field_name'].isin(target_names_unmapped_list)].field_name.tolist()

        # add fields to append fc
        # https://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy-classes/field.htm
        # The field object's type property does not match completely
        #  with the choices listed for the Add Field tool's field_type parameter.
        dict_ToField = {'Integer':'LONG', 'String':'TEXT', 'SmallInteger':'SHORT'}
        for name_add, type_add in zip(target_names_unmapped, target_types_unmapped):
            print('in the for loop')
            # because of wierd disconnect betw addField and FieldMappings type F these types
            if type_add in ['OID', 'GUID', 'Geometry']:
                pass
            # now that we are types AddField can handle
            elif name_add in ['Shape']:
                pass
            # now add all unmapped (which were screened) fields to mapping lists
            else:
                try:
                    type_add = dict_ToField[type_add]
                    print('did we key anything')
                except KeyError:
                    pass
                print('name: {} type {}'.format(name_add, type_add))
                arcpy.AddField_management(fp_append, name_add, type_add)
                target_fields.append(name_add)
                append_fields.append(name_add)
                new_field_names.append(name_add)
    # begin mapping
    fms = arcpy.FieldMappings()
    for field_target, field_append, new_name in zip(target_fields, append_fields, new_field_names):
        fm = arcpy.FieldMap()
        print(field_target, type(field_target))
        print(field_append, type(field_append))
        print(fp_append)
        fm.addInputField(fp_target, field_target)
        fm.addInputField(fp_append, field_append)
        output_name = fm.outputField
        output_name.name = new_name
        fm.outputField = output_name
        fms.addFieldMap(fm)
    arcpy.Merge_management([fp_target, fp_append], fp_out, fms)

def parse_dir(obj, **kwargs):
    '''
    matchses substrings to dir(obj) from python interactive
    document and add to: ZRU 5/26/2020
    '''
    # if dir used on list:
    if isinstance(obj, list):
        methods = obj
        print('here')
        pass
    # if dir is used on locals then a dictionary is returned
    elif isinstance(obj, dict):
        methods = obj.keys()
        print('dict')

    try:
        ex_symb = kwargs['exclude_symbols']
        indices_match, methods_match = [], []
        for idx, m in (enumerate(methods)):
            if s in m:
                for s in ex_symb:
                    break
            # will execute ONLY if no break:
            #http://psung.blogspot.com/2007/12/for-else-in-python.html
            else:
                indices_match.append(idx)
                methods_match.append(m)
    except KeyError:
        pass

    try:
        substr = kwargs['substring']
        indices_match = [idx for idx, method in enumerate(methods) if substr in method]
        methods_match = [methods[idx] for idx in indices_match]
    except KeyError:
        pass
    return(indices_match, methods_match)

def zipShapefilesInDir(inDir, outDir, **kwarg):
    '''
    Should be part of class when reorganizing.  Used and canabilized from
    spyder_arcgis.py to shapefile a gdb, zip and add to AGOL Content.  This
    takes a folder full of shapefiles and outputs individual zipfiles with
    <shapefile title>.zip folder containing zipped contents per shapefile
    Note: Use compare_data.parse_gdb_dsets to unpack shapefiles from gdb,
    then feed to this function. Note two functions use each other
    (zipShapefilesInDir and zipShapeFile).
    From here: https://community.esri.com/thread/28985
    ZRU 7/23/2020
    ARGS:
    inDir:      path/to/directory with shapfiles
    outDir:     path/to/zipdir parent where folders.zip will be added (one per
                shapefile)

    '''
    import zipfile
    import glob

    # Check that input directory exists
    if not os.path.exists(inDir):
        print("Input directory {} does not exist!".format(inDir))
        return False

    # Check that output directory exists
    if not os.path.exists(outDir):
        # Create it if it does not
        print('Creating output directory {}'.format(outDir))
        os.mkdir(outDir)

    print("Zipping shapefile(s)in folder {} to output folder {}".format(inDir, outDir))

    try:
        # Seems more for Problematic files that break function with Exception
        # unrelated to the file's existence 5/21/21
        exclude_files = kwarg['exclude_files']
        if isinstance(exclude_files, str):
            exclude_files = [exclude_files]
        # will be file name with .shp
        all_files_shp = glob.glob(os.path.join(inDir, "*.shp"))
        # will be base file name w/out .shp
        all_files_basename = [os.path.splitext(os.path.basename(shp))[0] for shp in all_files_shp]
        # basenames of shapefiles to attack and zip
        filtered_basenames = list(set(all_files_basename) - set(exclude_files))
        filtered_basenames.sort()
        # Creates filepath for filtered shapefiles
        fp_shapefiles = [os.path.join(inDir, '{}.shp'.format(basename)) for basename in filtered_basenames]
    except KeyError:
        fp_shapefiles = [fp_shp for fp_shp in glob.glob(os.path.join(inDir, "*.shp"))]
    # Loop through shapefiles in input directory
    for inShp in fp_shapefiles:
        # Build the filename of the output zip file
        # os.basename will give file basename. os.path.splitext splits file name and extension ZRU
        subfolder_zip = os.path.splitext(os.path.basename(inShp))[0] + ".zip"
        outZip = os.path.join(outDir, subfolder_zip)
        # skip if zipfile exists already
        if os.path.exists(outZip):
            print('This folder exists: {}\nIt will be NOT be zipped'.format(subfolder_zip))
        # if shp not yet zipped, zip it.
        else:
            zipShapefile(inShp, outZip)


def zipShapefile(inShapefile, newZipFN):
    '''
    Should be part of class when reorganizing.  Used and canabilized from
    spyder_arcgis.py to shapefile a gdb, zip and add to AGOL Content.  This
    takes a folder full of shapefiles and outputs individual zipfiles with
    <shapefile title>.zip folder containing zipped contents per shapefile
    Note: Use compare_data.parse_gdb_dsets to unpack shapefiles from gdb,
    then feed to this function.  Note two functions use each other
    (zipShapefilesInDir and zipShapeFile).
    From here: https://community.esri.com/thread/28985
    ZRU 7/23/2020
    ARGS:
    inDir:      path/to/directory with shapfiles
    outDir:     path/to/zipdir parent where folders.zip will be added (one per
                shapefile)
    '''

    import zipfile
    import glob
    import time

    print('Starting to Zip '+ inShapefile +' to '+ newZipFN)
    start = time.time()

    # Check that input shapefile exists
    if not (os.path.exists(inShapefile)):
        print(inShapefile + ' Does Not Exist')
        return False

    # Delete output zipfile if it already exists
    if (os.path.exists(newZipFN)):
        print('Deleting '+newZipFN)
        os.remove(newZipFN)

    # Output zipfile still exists, exit
    if (os.path.exists(newZipFN)):
        print('Unable to Delete'+newZipFN)
        return False

    # Open zip file object
    zipobj = zipfile.ZipFile(newZipFN,'w')

    # Loop through shapefile components
    for infile in glob.glob( inShapefile.lower().replace(".shp",".*")):
        # Skip .zip file extension
        if os.path.splitext(infile)[1].lower() != ".zip":
            print("Zipping {}".format(infile))
            # Zip the shapefile component
            zipobj.write(infile, os.path.basename(infile), zipfile.ZIP_DEFLATED)
    end = time.time()
    print('elapsed time: {} seconds'.format(round(end-start,1)))
    # Close the zip file object
    zipobj.close()
    return True

def get_extents(fc_in, fp_out, **kwarg):
    '''
    Wrapper for some arcpy extent grabbers.  But can find max min extent for
    feat or feat class with multiple features.  Vectors.
    ZRU 7/24/2020 - used for getting extents in bathymetry OpenTopo downloads

    ARGS:
    fc_in       string. file path to feature.  Can call directly from python
                console in arcmap with loaded feat_lyr
    fp_out      sting. path to csv to save dataframe
    kwarg       expand = number of feet or whatever unit to buffer extent on
                all four sides
    '''
    import arcpy
    import numpy as np
    maxx, maxy, minx, miny = [],[],[],[]
    for row in arcpy.da.SearchCursor(fc_in, ["SHAPE@"]):
        maxx.append(row[0].extent.XMax)
        maxy.append(row[0].extent.YMax)
        minx.append(row[0].extent.XMin)
        miny.append(row[0].extent.YMin)
    maxx, maxy, minx, miny = max(maxx), max(maxy), min(minx), min(miny)
    try:
        expand_scalar = kwarg['expand']
        maxx, maxy = maxx + expand_scalar, maxy + expand_scalar
        minx, miny = minx - expand_scalar, miny - expand_scalar
    except KeyError:
        pass
    df = pd.DataFrame(np.column_stack([maxx, maxy, minx, miny]), columns = ['maxx', 'maxy', 'minx', 'miny'],  index = ['JC_Boyle'])
    pd.DataFrame.to_csv(df, fp_out)

def get_overlap(ds1, ds2, **kwarg):
    '''
    Used initially for sedimentation analysis in July 2020.  But simply finds
    min bounding extents of two geotiffs, then based on kwargs outputs extents
    to file and/or returns clipped numpy arrays of rasters.  Before reusing
    switch to rasterio as gdal is pain in butt.
    ARGS:
    ds1:        dataset opened with gdal
    ds2:        dataset opened with gdal
    KWARGS:
    reservoir_name:     String. This option will save extents to text file using the res
                        name in file path
    output_args:        Boolean. returns clipped numpy arrays for ds1 and ds2
    '''
    import gdal

    # from here: https://gis.stackexchange.com/questions/16834/how-to-add-different-sized-rasters-in-gdal-so-the-result-is-only-in-the-intersec
    gt1 = ds1.GetGeoTransform()
    gt2 = ds2.GetGeoTransform()
    # note geotransform yields list with 6 items (https://gdal.org/user/raster_data_model.html):
    # [easting, x-transform, y-transform, northing, x-transform, y-transform]
    # translation: [west_bdry, step easting, step northing, north boundar, step easting, step northing]

    # r1 has left, top, right, bottom of dataset's bounds in geospatial coordinates.
    # note Raster<X,Y>Size = ncells
    # west, north, east, south
    r1 = [gt1[0], gt1[3], gt1[0] + (gt1[1] * ds1.RasterXSize), gt1[3] + (gt1[5] * ds1.RasterYSize)]

    # Do the same for dataset 2 ...
    r2 = [gt2[0], gt2[3], gt2[0] + (gt2[1] * ds2.RasterXSize), gt2[3] + (gt2[5] * ds2.RasterYSize)]
    intersection = [max(r1[0], r2[0]), min(r1[1], r2[1]), min(r1[2], r2[2]), max(r1[3], r2[3])]
    xsize1, ysize1 = ds1.RasterXSize, ds1.RasterXSize
    # x_offset1 = [math.ceil(intersection[0] - r2[0]), math.floor(intersection[2] - r2[0])]
    x_offset1 = [intersection[0] - r1[0], intersection[2] - r1[0]]
    x_buff1 = x_offset1[1] - x_offset1[0]
    x_offset2 = [intersection[0] - r2[0], intersection[2] - r2[0]]
    x_buff2 = x_offset2[1] - x_offset2[0]
    # the offsets are from west to east easting vals.  For some reason buffer is used
    # for the second subset position. It's the distance from the first easting
    # to the second eastng.  Ditto for y_offset but from north to south
    y_offset1 = [r1[1] - intersection[1], r1[1] - intersection[3]]
    y_buff1 = y_offset1[1] - y_offset1[0]
    y_offset2 = [r2[1] - intersection[1], r2[1] - intersection[3]]
    y_buff2 = y_offset2[1] - y_offset2[0]
    print('x_extents: ', ds2.RasterXSize + intersection[0])
    print('y_extents: ', ds2.RasterYSize - intersection[1])
    print('intersection: ', intersection)
    print('gt1: ', gt1)
    print('gt2: ', gt2)
    print('xoffset: {} x_buff: {}'.format(math.ceil(x_offset1[0]), math.floor(x_buff1)))
    print('yoffset: {} y_buff: {}'.format(math.ceil(y_offset1[0]), math.floor(y_buff1)))
    print('xoffset2: {} x_buff: {}'.format(math.ceil(x_offset2[0]), math.floor(x_buff2)))
    print('yoffset2: {} y_buff: {}'.format(math.ceil(y_offset2[0]), math.floor(y_buff2)))

    # if you want to return intersections include this
    try:
        reservoir_name = kwarg['reservoir_name']
        with open('D:/box_offline/bathymetry_project/bathymetry_project/overlap_extents_{}.txt'.format(reservoir_name), 'w') as text_file:
            text_file.write('intersection: {}'.format(intersection))
    except KeyError:
        pass
    try:
        kwarg['output_args']
        arr1 = ds1.ReadAsArray(math.ceil(x_offset1[0]), math.ceil(y_offset1[0]), math.floor(x_buff1), math.floor(y_buff1))
        arr2 = ds2.ReadAsArray(math.ceil(x_offset2[0]), math.ceil(y_offset2[0]), math.floor(x_buff2), math.floor(y_buff2))
        return(arr1, arr2)
    except KeyError:
        pass
def export_ddp(fp_mxd, fp_pdf, range_str, **kwargs):
    '''
    20201022  perhaps futile attempt to print maps from CL.  Wrapper for this
    function essentially https://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy-mapping/datadrivenpages-class.htm
    ARGS:
    fp_mxd      self-explanatory
    fp_pdf      self-explanatory
    range_str   either 'ALL' or 'RANGE'
    kwargs      one option = 'multiple_files' for kw with THREE value options =
                'PDF_SINGLE_FILE', 'PDF_MULTIPLE_FILE_PAGE_NAME',
                 'PDF_MULTIPLE_FILE_PAGE_INDEX'
    '''
    mxd_doc = arcpy.mapping.MapDocument(fp_mxd)

    # Determine if document has dataDrivenPages enabled and/or multi page doc
    try:
        ddp = mxd_doc.dataDrivenPages
    # No DDP capabailities, export simple pdf
        create_mxd = True
    except AttributeError:
        create_mxd = False
    if create_mxd:
        if range_str == 'RANGE':
            try:
                pages = kwargs['RANGE']
            except KeyError:
                print('pass a range string.  DID NOT EXPORT MAP')
            try:
                multiple_files = kwargs['multiple_files']
                ddp.exportToPDF(fp_pdf, 'RANGE', pages, multiple_files)
            except:
                ddp.exportToPDF(fp_pdf, 'RANGE', pages)
        else:
            try:
                multiple_files = kwargs['multiple_files']
                ddp.exportToPDF(fp_pdf, 'ALL', multiple_files)
            except KeyError:
                ddp.exportToPDF(fp_pdf, 'ALL')
    # export normal map doc, not DDP
    else:
        arcpy.mapping.ExportToPDF(mxd_doc, fp_pdf)

def export_pdf(fp_csv, dir_out, action_val):
    '''
    ZU 20220901.  Outputting batches of old mxd's for Swancove Pool.
    columns from csv are obvious from col names.  Create these columns:
    mxd_name (index col), fig_name, fp_mxd, action
    ARGS
    fp_csv          path/to/mxd_inv.csv
    dir_out         path/to/pdf locations
    action_val      flag to mark what to export from inventory
    '''
    df = pd.read_csv(fp_csv, index_col = 'mxd_name')
    df_select = df[df.action == action_val]
    for index in df_select.index:
        fig_name = df_select.loc[index, 'fig_name']
        fp_mxd = df_select.loc[index, 'fp_mxd']
        pdf_out = os.path.join(dir_out, '{}.pdf'.format(fig_name))
        mxd = arcpy.mapping.MapDocument(fp_mxd)
        print('Exporting: {}\n To:        {}'.format(index, pdf_out))
        arcpy.mapping.ExportToPDF(mxd, pdf_out)

def mxd_inventory(fp_mxd, figure_name, dir_out):
    '''
    typical half-ass zach function to output logfile essentially.  Except this
    log file is the inventory for file layers in mxd file.  Takes file path
    to mxd and directory to save text file to. ZRU 20201025

    ARGS
    fp_mxd          file path to mxd to take inventory of
    figure_name     name of figure created by mxd
    dir_out          folder to save inventory text file to
    '''
    mxd = arcpy.mapping.MapDocument(fp_mxd)
    lyr_inventory = []
    for lyr in arcpy.mapping.ListLayers(mxd):
        # supports(DATASOURCE) is a convenient method to determine if layer
        # has value for that attribute essentially
        # visibile obviously if checked on map
        if (lyr.supports("DATASOURCE")) & (lyr.visible):
        # if lyr.supports("DATASOURCE"):
            lyr_inventory.append(lyr)
        else:
            pass
    # basename of mxd without extension
    fname_out = os.path.basename(fp_mxd).split('.')[0]
    # name of inventory
    fname_out = fname_out + '_layer_inventory.txt'
    # full path to inventory text file
    fp_out = os.path.join(dir_out, fname_out)
    lyr_string = []
    for idx, lyr in enumerate(lyr_inventory):
        lyr_name = lyr.name
        lyr_path = lyr.dataSource
        lyr_string.append('{0}.\nLAYER NAME: {1}\nDATA SOURCE: {2}\n'.format(idx + 1, lyr_name, lyr_path))
    lyr_string_all = '\n'.join(lyr_string)
    mxd_basename = os.path.basename(fp_mxd)
    todays_date = datetime.datetime.today().strftime('%B %d %Y')
    intro =('Figure Name: {}\n'
            'Map Document: {}\n'
            'Date: {}\n'
            'LAYER NAME = layer name in Table of Contents in map document (mxd)\n'
            'DATA SOURCE  = path to data on McMillen-Jacobs file system').format(figure_name, mxd_basename, todays_date)

    txt = '{}\n\n{}'.format(intro, lyr_string_all)
    with open(fp_out, 'w') as out_file:
        out_file.write(txt)
def mxd_inventory_csv(fp_base, fname_csv, **kwargs):
    '''
    wrap both these functions into a obj oriented class

    ARGS
    fp_base          file path to mxd to take inventory of
    kwarg               thus far just select_mxds which will narrow down fp_base
                        to just specific mxds.  List
    '''
    try:
        mxd_list = kwargs['select_mxds']
        if not isinstance(mxd_list, list):
            mxd_list = [mxd_list]
    except KeyError:
        mxd_list = [item for item in os.listdir(fp_base) if '.mxd' in item]
    fp_mxd_list = [os.path.join(fp_base, fname_mxd) for fname_mxd in mxd_list]
    # fp_mxd_list = [fp_mxd.replace('\\', '/') for fp_mxd in fp_mxd_list]
    lyr_list = []
    lyr_name = []
    lyr_source = []
    mxd_name = []
    visible = []
    min_scale, max_scale, def_query, transparency, labels = [],[],[],[],[]
    for idx, fp_mxd in enumerate(fp_mxd_list):
        print(fp_mxd)
        mxd = arcpy.mapping.MapDocument(fp_mxd)
        mxd_name_temp = mxd_list[idx]
        print('Inentorying: {}'.format(os.path.split(fp_mxd)[-1]))
        for lyr in arcpy.mapping.ListLayers(mxd):
            # supports(DATASOURCE) is a convenient method to determine if layer
            # has value for that attribute essentially
            # visibile obviously if checked on map
            # if (lyr.supports("DATASOURCE")) & (lyr.visible):
            if lyr.supports("DATASOURCE"):
                lyr_name.append(lyr.name)
                lyr_source.append(lyr.dataSource)
                mxd_name.append(mxd_name_temp)
                if lyr.visible:
                    visible.append('TRUE')
                else:
                    visible.append('FALSE')
                try:
                    min_scale.append(getattr(lyr, 'minScale'))
                except NameError:
                    min_scale.append('NA')
                try:
                    max_scale.append(getattr(lyr, 'maxScale'))
                except NameError:
                    max_scale.append('NA')
                try:
                    transparency.append(getattr(lyr, 'transparency'))
                except NameError:
                    transparency.append('NA')
                try:
                    def_query.append(getattr(lyr, 'definitionQuery'))
                except NameError:
                    #name errors occur with .tifs (thus far)
                    def_query.append('NA')
                try:
                    labels.append(getattr(lyr, 'showLabels'))
                except NameError:
                    labels.append('NA')
            else:
                pass

        # plane old mxd name
    df = pd.DataFrame(np.column_stack([mxd_name, lyr_name, visible, lyr_source,
                                min_scale, max_scale, def_query, transparency, labels]),
                    columns = ['map_name', 'layer_name', 'visible', 'layer_source',
                                'min_scale','max_scale','def_query','transparency','show_label'])
    if os.path.splitext(fname_csv)[-1] == '':
        fname_csv = '{}.csv'.format(fname_csv)
    elif os.path.splitext(fname_csv)[-1] == '.csv':
        pass
    fp_out = os.path.join(fp_base, fname_csv)
    pd.DataFrame.to_csv(df, fp_out)

    # ADD 3/10/2021
    # lyr.minScale, lyr.maxScale, lyr.definitionQuery, lyr.transparency, showLable

def write_folder_contents(fp, **kwargs):
    '''
    simple readme that lists all items and files in fp argument.  Filename will
    be README_<folder_name>_<date>.txt.  Will indicate date in file
    ARGS
    fp          file path for folder to README
    '''
    folder_name = os.path.split(fp)[-1]
    fname_readme = 'README_{}.txt'.format(folder_name)
    fp_out = os.path.join(fp, fname_readme)
    files = os.listdir(fp)
    files_fp = [os.path.join(fp, f) for f in files]
    files_fp.sort(key=os.path.getctime)
    files_fp.reverse()
    try:
        kwargs['shp']
        files_fp = [f for f in files_fp if '.shp' in f]
        files_fp = [f for f in files_fp if '.lock' not in f]
        files_fp = [f for f in files_fp if '.xml' not in f]
    except KeyError:
        pass
    files_formatted = [os.path.split(fp)[-1] for fp in files_fp]
    basic_str = '\n'.join(files_formatted)
    todays_date = datetime.datetime.today().strftime('%B %d %Y')
    signature = 'Created By Zach Uhlmann on {}'.format(todays_date)
    file_name = 'README_{}'.format(folder_name)
    basic_str = file_name + '\n' + signature + '\n\nContents\n' + basic_str
    with open(fp_out, 'w') as out_file:
        out_file.write(basic_str)
def enum_fp_list(fp_base, return_full_path, **kwargs):
    '''
    will this print

    ARGS:
    fp_base             file path to listdir
    return_full_path    True or False
    kwargs              filter_ftype (option1) = whatever file type endswith i.e. str.endswith(filter_ftype)
    '''

    lst = os.listdir(fp_base)
    idx = 0
    try:
        filter_ftype = kwargs['filter_ftype']
        print('Files that end with: {}'.format(filter_ftype))
        if return_full_path:
            full_path_list = []
            for item in lst:
                if item.endswith(filter_ftype):
                    str = '{}. {}'.format(idx, item)
                    print(str)
                    full_path_list.append(os.path.join(fp_base, item))
                    idx += 1
        else:
            for item in lst:
                if item.endswith(filter_ftype):
                    str = '{}. {}'.format(idx, item)
                    print(str)
                    idx += 1
    except:
        if return_full_path:
            full_path_list = []
            for item in lst:
                str = '{}. {}'.format(idx, item)
                print(str)
                full_path_list.append(os.path.join(fp_base, item))
                idx += 1
        else:
            for item in lst:
                str = '{}. {}'.format(idx, item)
                print(str)
                idx += 1
    try:
        return(full_path_list)
    except NameError:
        pass

def create_df_inventory(fp_base, fp_csv, version = 1):
    '''
    utility to create a list of mxds and pdfs to keep track of multiple maps
    in a project.  This will be drawn upon to create an inventory list
    ZU 20201213
    fp_base             directory containing mxds
    fp_out              where to save inventory
    fp_inventory        full name of file path including .csv for inventory
    '''
    mxd_list = [fname for fname in os.listdir(fp_base) if 'mxd' in fname]
    pdf_append = '_version_{}.pdf'.format(version)
    fname_pdf = [os.path.splitext(fname_mxd)[0] + pdf_append for fname_mxd in mxd_list]
    df = pd.DataFrame(np.column_stack(
                        [mxd_list, fname_pdf, [fp_base] * len(fname_pdf)]),
                        columns = ['mxd_filename', 'pdf_filename', 'base_dir'])
    pd.DataFrame.to_csv(df, fp_csv)
def return_mxd_obj(fp_mxd):
    '''
    helpful methods and such to add to mapping doc
    arcpy.mapping.ListDataFrames
    '''
    mxd = arcpy.mapping.MapDocument(fp_mxd)
    return(mxd)
def test_run(string_print):
    print('FUUUUUUCKKKK {}'.format(string_print))
def parse_item_desc(sub_item_list, target_key, target_val, add = True):
    '''
    Quick utility used for adding and updating Item Description metadata via
    xml files.  Note this is used to pass a single target key and target val
        ZRU 11/15/2020
    ARGS:
    sub_item_list = pass list from idPurp of xml for shapefiles.  The list will be
                    the item_desc_str.splitlines() which splits at /n - essentially
                    splitting each key:val pair into one item in list i.e.
                    ['DATA_LOCATION_MCMILLEN_JACOBS: <file path',
                    'DATE_ADDED_AGOL: 20201115']
    target_key     target key i.e. DATA_LOCATION_MCMILLEN_JACOBS,
                                                DATE_ADDED_AGOL
    target_val     vals to pair with each target.
    RETURNS
    New Item Description list with strings per sub item
    '''
    # initiate as false
    replaced_sub_item = False
    idx_offset = 0
    print('we called this righrt?')
    for idx, sub_item in enumerate(sub_item_list):
        # if empty sub_items shrunk the list, idx will be notched back one at a time
        idx_adjusted = idx - idx_offset
        try:
            # if empty string need to remove
            if sub_item != '':
                temp_idx = sub_item.index(':')
                # get exact sub_item_key i.e. SOURCE_CONTACT_MCMILEN
                sub_item_key = sub_item[:temp_idx]
                # if already present, then replace and return new list
                if target_key == sub_item_key:
                    # if ADDING purp lines
                    if add:
                        sub_item_list[idx_adjusted] = '{}: {}'.format(target_key, target_val)
                        replaced_sub_item = True
                    # if REMOVING purp items
                    else:
                        sub_item_list.remove(sub_item_list[idx_adjusted])
            # if empty string in sub items, remove
            else:
                idx_adjusted = idx - idx_offset
                sub_item_list = [item for idx2, item in enumerate(sub_item_list) if idx_adjusted != idx2]
                idx_offset += 1
        # non-AECOM standard summary.  skip lines without :
        except ValueError:
            pass
    # if no matched sub items were found, then simply add to list
    if add:
        if not replaced_sub_item:
            sub_item_list.append('{}: {}'.format(target_key, target_val))
        # if no matches are found, then return original list
    return(sub_item_list)

def create_poly_from_pts(table_in, fp_out, offsets, **kwargs):
    '''
    Takes points and offsets by specified e,w,s,n into polygon feat class
    ZRU 20201116

    table_in        point feature from arc.  can be adapted for csv
    fp_out          full path name to gdb or with .shp
    offsets         list in [w,e,n,s] units of projection system
    '''
    w, e, n, s = offsets[0], offsets[1], offsets[2], offsets[3]
    poly = []
    try:
        num_pts = kwargs['num_pts']
    except KeyError:
        num_pts = None
    with arcpy.da.SearchCursor(table_in, ['SHAPE@XY']) as cursor:
        for row in cursor:
            x = row[0][0]
            y = row[0][1]
            ul = arcpy.Point(x - w, y + n)
            ur = arcpy.Point(x + e, y + n)
            ll = arcpy.Point(x - w, y - s)
            lr = arcpy.Point(x + e, y - s)
            extent = arcpy.Array([ul,ur,lr,ll])
            poly.append(arcpy.Polygon(extent))
    arcpy.CopyFeatures_management(poly[:num_pts], fp_out)

# def figure_units_to_scale(width_fig, len_fig, width_map, offsets):
#     ew = (width_map * 12) / width_map
#     ns = ew * (len_fig / width_fig)
#     try:
#         offsets = kwargs['unequal_offsets']
#         w, e, n, s = offsets[0], offsets[1], offsets[2], offsets[3]
#         w = w * ew
#         e = e * ew
#         n = n * ns
#         s = s * ns
#     except KeyError:
#         w = w * 0.5
#         e = e * 0.5
#         n = n * 0.5
#         s = s * 0.5
#     offsets = [w, e, n, s]
#     return(offfsets)

def clean_fp(fp_in, **kwargs):
    '''
    takes full paths of files and removes spaces and replaces characters base
    on kwargs.  Also option to change extentsion
    ARGS
    fp_in           file path in
    kwarg['replace_w_underscore']      character wanting to replace i.e. '.' == '_'
    kwarg['replace_space']              finds spaces and replaces with value
    kwargs['ext_new']       replaces old extension with this value
    '''
    # yields list w len(fp_components) == 2.  [fp without extentsion, .<ext>]
    fp_components = os.path.splitext(fp_in)
    fp_no_ext = fp_components[0]
    ext_orig = fp_components[1]
    # kwargs if want to remove vals from file name
    # replace specified value with an underscore
    try:
        val_orig = kwargs['replace_w_underscore']
        fp_no_ext = fp_no_ext.replace(val_orig, '_')
    except:
        pass
    # replace space with new value
    try:
        val_new = kwargs['replace_space']
        fp_no_ext = fp_no_ext.replace(' ', val_new)
    except:
        pass
    # change extension
    try:
        ext_new = kwargs['ext_new']
        fp_new = '{}.{}'.format(fp_no_ext, ext_new)
    except:
        print('NO NEW EXTENSION was specified')
        fp_new = os.path.normpath(os.path.join(fp_no_ext, ext_orig))
    return(fp_new)

def merge_basic(fp_csv, indices, dir_out, name_out, in_memory=True):
    '''
    utility to buffer multile features and line out to merge.
    Add field mappings stripping capabilities
    ZRU 12/04/2020.  To help with creating and merging buffers. Add ability to buffer
    input to temp lyr and then merge
    !!IMPORTANT:  Strings for buffer units from csv must be EXACTLY as:
     Centimeters, Decimal degrees, Decimeters, Feet, Inches, Kilometers, Meters,
     Miles, Millimeters, Nautical Miles, Yards - to name a few.
     ex) 100 Feet not 100 feet or 100 ft
    fp_csv:         Type = String i.e. 'path/to/file.csv'
                    path/to/csv with datasets
    indices:        Type = List i.e. [1,4,5]
                    indice of feats you want to merge.  indice begins counting at zero!
    dir_out:        Type = String
                    directory to save data i.e. path/to/working.gdb
    name_out:       Type = String
                    name of FEATURE to save out
    in_memory:      Type = Boolean
                    default is True.  If set to false individual buffered features
                    will be output to dir_out (argument passed)
    '''

    # this reads the csv into a dataframe
    df = pd.read_csv(fp_csv)
    # set workspace
    workspace = arcpy.env.workspace
    print('you are in this workspace: If failing, change to workspace of inputs using:\narcpy.env.workspace = path/to/workspace')
    # will use later...
    workspace_trunc = '/'.join(workspace.split('/')[-3:])
    # make sure indices are passed as list = [0,1,2] for example
    if isinstance(indices, list):
        print('list')
        if isinstance(indices[0], int):
            pass
        else:
            sys.exit()
    elif isinstance(indices, int):
        print('int')
        indices = int(indices)
    else:
        print('neither')
        sys.exit()

    # grab feature names from dataframe
    feats_to_merge = [df.iloc[idx].feature_name for idx in indices]

    # create buffer string - ex) '105 Feet'
    buffer_strings = []
    name_field = []
    buffer_unit = []
    for idx in indices:
        buffer_val = df.iloc[idx].buffer_val
        buffer_unit = df.iloc[idx].buffer_unit
        buffer_strings.append('{} {}'.format(buffer_val, buffer_unit))
        name_field.append(df.iloc[idx].name_field)

    # Set fp out for buffered feats - in_memory is default
    if in_memory:
        feats_buffered = ['in_memory//{}'.format(feat) for feat in feats_to_merge]
    else:
        feats_buffered = [os.path.join(dir_out, feat) for feat in feats_to_merge]

    # create buffered features
    # added count after the zip in for loop once extra iterator derived vals needed. UGLY
    start = time.time()
    ct = 0
    for feat, feat_buff, buff_str in zip(feats_to_merge, feats_buffered, buffer_strings):
        print('feat: {}\nfeat_buff: {}\nbuff_str: {}'.format(feat, feat_buff, buff_str))
        # if it exists AND we did the in_memory_route
        if (in_memory) & (arcpy.Exists(feat_buff)):
            arcpy.Delete_management(feat_buff)
        arcpy.Buffer_analysis(feat, feat_buff, buff_str, dissolve_option = 'ALL')
        # get buffer size field name and add to feature table
        # ex) buff_size_Feet
        temp = buff_str.split(' ')
        buff_val = temp[0]
        buff_units = temp[1].lower()
        buff_size_field = 'buff_size_{}'.format(buff_units)
        arcpy.AddField_management(feat_buff, 'feature_name', 'TEXT', field_length = 50)
        arcpy.AddField_management(feat_buff, buff_size_field, 'FLOAT')
        arcpy.AddField_management(feat_buff, 'filepath_source', 'TEXT', field_length = 254)
        name_val = name_field[ct]
        # short filepath for attribute table reference.  relative to 3 dirs back
        filepath_source = os.path.join(workspace_trunc, feat)
        # what is the buffer unit
        with arcpy.da.UpdateCursor(feat_buff, ['feature_name', buff_size_field, 'filepath_source']) as cursor:
            for row in cursor:
                row[0] = name_val
                row[1] = buff_val
                row[2] = filepath_source
                cursor.updateRow(row)
        ct += 1
    fp_out = os.path.join(dir_out, name_out)
    arcpy.Merge_management(feats_buffered, fp_out)
    end = time.time()
    print('Tool took {} seconds'.format(end-start))

def copy_all_feats(fp_in, fp_out):
    # full path of all shapefiles in fp_in
    all_files_shp = glob.glob(os.path.join(fp_in, "*.shp"))
    # feature names
    feat_name = [os.path.splitext(os.path.split(fp_shp)[-1])[0] for fp_shp in all_files_shp]
    for fp_shp, feat_name in zip(all_files_shp, feat_name):
        # print('ZIPPING: {}\nTO: {}\nAS: {}'.format(fp_shp,fp_out, feat_name))
        arcpy.FeatureClassToFeatureClass_conversion(fp_shp, fp_out, feat_name)

# def update_labels(rows_idx_start):
#     # main dirs
#     fp_labels = os.path.join(get_path(8), 'labelset_creation_MPs')
#     fp_working = get_path(18)
#     # hardcoded for now
#     fp_csv = os.path.join(fp_labels, 'labelset_inventory_90Des_ga.csv')
#     # master feat class
#     fp_labels_feat = os.path.join(fp_working, '//working.gdb//labels//labels_low_90des_ga')
#     todays_date = datetime.datetime.today().strftime('%B %d %Y')
#     fp_backup = os.path.join(fp_labels, 'labelset_backup_{}.csv'.format(todays_date)
#     df_orig = pd.read_csv(fp_csv)
#     col_names = df_orig.column_names.tolist()
#     ct = 0
#     with arpy.da.UpdateCursor(fp_labels_feat, col_names) as cursor:
#         if ct >= rows_idx_start:
#             for idx, name in enumerate(col_names):
#                 # This row[0] will access teh object to grab the field.  If n fields > 1, n idx >1
#                 if ct == 0:
#                     val = df_orig.iloc[ct][name].tolist()
#                 row[idx] = val[ct]
#             cursor.updateRow(row)
#             pd.DataFrame.to_csv(df, os.path.join(fp_out, '{}_{}.csv'.format(feat_name, field)))
#         else:
#             pass

def sql_str(val_list, field, out_dir, logic_str = ' Or '):
    where_clause_list = ['"{0}"={1}'.format(field, val) for val in val_list]
    print(where_clause_list)
    where_clause = logic_str.join(where_clause_list)
    fp_out = os.path.join(out_dir, r'sql_temp.txt')
    print(where_clause)
    with open(fp_out, 'w') as out_file:
        out_file.write(where_clause)

def return_fields(fp_in, fp_out):
    fields_obj = arcpy.ListFields(fp_in)
    fields = [field.name.encode('utf-8') for field in fields_obj]
    dtype = [field.type for field in fields_obj]
    df = pd.DataFrame(np.column_stack([fields, dtype]), columns = ['original_fields', 'dtype'])
    pd.DataFrame.to_csv(df, fp_out)

def cursor_merge(fp_csv, fp_list, add_fp_source_field = True):
    df = pd.read_csv(mapping_csv, dtype = {'feature_id':int})
    feature_id = list(df.feature_id)
    feature_id_unique = set(feature_id)
    num_features = len(feature_id_unique)
    target_df = df[df.feature_id == feature_id_unique[0]]

def mxd_inventory_temp(mxd_dir):
    '''
    Possibly redundant function.  inventory for management plans - Camas MP2
    20210104
    '''
    mxd_list = [item for item in os.listdir(mxd_dir) if os.path.splitext(item)[-1] == '.mxd']
    fp_mxd_list = [os.path.join(mxd_dir, item) for item in mxd_list]
    visible_lyr = []
    visible_lyr_source = []
    mxd_list_csv = []
    ct = 1
    for idx, mxd in enumerate(fp_mxd_list):
        mxd_obj = arcpy.mapping.MapDocument(mxd)
        lyr_list = arcpy.mapping.ListLayers(mxd_obj)
        temp1 = []
        temp2 = []
        ct+=1
        for lyr in lyr_list:
            if (lyr.supports("DATASOURCE")) & (lyr.visible):
                temp1.append(lyr.name)
                temp2.append(lyr.dataSource)
        visible_lyr.extend(temp1)
        visible_lyr_source.extend(temp2)
        temp_name = [mxd_list[idx]] * len(temp1)
        mxd_list_csv.extend(temp_name)
    df = pd.DataFrame(np.column_stack([mxd_list_csv, visible_lyr, visible_lyr_source]), columns = ['filename', 'layer_name', 'layer_source'])
    fp_out = r'C:\Users\uhlmann\Box\GIS\Project_Based\Klamath_River_Renewal_MJA\GIS_Request_Tracking\GIS_Requests_Management_Plans\Camas_MPs\MP2\mp2_inventory.csv'
    pd.DataFrame.to_csv(df, fp_out)


def delete_features(fp_csv):
    '''
    pass a csv and delete indicated features from gdb
    csv should include:
    fp_feat                 file path to feature
    remove_feature          Boolean
    feature_name            name of feature
    '''
    df = pd.DataFrame.from_csv(fp_csv)
    df_selection = df[df.remove_feature == True]
    fp_feat = df_selection.fp_feat.tolist()
    feat_name = df_selection.feature_name.tolist()
    for feat, feat_name in zip(fp_feat, feat_name):
        print('DELETING: {}'.format(feat_name))
        arcpy.Delete_management(feat)

def files_in_folder(fp_in, csv_name, ext = 'mxd', return_df = False):
    '''
    quick function could use improvement. Saves csv of files in fp_in matching
    extentsion provided (mxd is default).  Pass return_df = True to return df
    instead. ZU 20210226

    fp_in           file path in
    fp_out          path to csv with ext
    ext             extentsion to hunt. default is .mxd
    return_df       pass True if want to returen df INSTEAD of saving to csv
    '''
    from pathlib import Path

    # https://stackoverflow.com/questions/168409/how-do-you-get-a-directory-listing-sorted-by-creation-date-in-python
    paths = sorted(Path(fp_in).iterdir(), key=os.path.getmtime)
    paths.reverse()
    file_matching_ext =[f.name for f in paths if '.{}'.format(ext) == os.path.splitext(f.name)[-1]]
    df = pd.DataFrame(file_matching_ext)
    if not return_df:
        fp_out = os.path.join(fp_in, csv_name)
        pd.DataFrame.to_csv(df, fp_out)
    else:
        return(df)

def feat_to_feat_provenance(fcs_in, fcs_dir_out, feat_name):
    '''
    copy field with orig field path attribute
    '''
    arcpy.FeatureClassToFeatureClass_conversion(fcs_in, fcs_dir_out, feat_name)
    fp_fcs_copied = os.path.join(fcs_dir_out, feat_name)
    arcpy.AddField_management(fp_fcs_copied, 'fp_fc_orig', 'text')
    # cast into proper delimeters - followed links in accepted answer
    # https://stackoverflow.com/questions/4415259/convert-regular-python-string-to-raw-string
    fcs_in = fcs_in.replace('\\','/')
    arcpy.CalculateField_management(fp_fcs_copied, 'fp_fc_orig', '"'+fcs_in+'"', "PYTHON")

def feat_select_union(fp_in, field_name, val_list, feat_name_out):
    fcs_list = []
    for val in val_list:
        sql_clause = '"{}" IN ({})'.format(field_name, val)
        print(fp_in)
        print(val)
        print(sql_clause)
        arcpy.FeatureClassToFeatureClass_conversion(fp_in, 'in_memory', val, where_clause = sql_clause)
        fcs_list.append('in_memory/'.format(val))
    arcpy.Union_analysis(fcs_list, 'in_memory/feat_name_out')

def extract_cursor(fp_csv, feat_name_out, arc_env):
    arcpy.env.workspace = arc_env
    df = pd.read_csv(fp_csv)
    lst = []
    for i in range(len(df)):
        fp_feat = df.iloc[i].fp_feat
        field_name = df.iloc[i].field_name
        target_val = df.iloc[i].target_val
        print('FEATURE: {}\nFIELD NAME {} TARGET VAL {}'.format(fp_feat, field_name, target_val))
        # accumulate id fields in case multiple rows in one feature
        with arcpy.da.SearchCursor(fp_feat, [field_name, 'SHAPE@']) as cursor:
            for row in cursor:
                if target_val in row:
                    # get shape field from tuple
                    # initiate new feature
                    if 'shapes_union' not in locals():
                        shapes_union = copy.copy(row[1])
                        print('initiate shapes_union')
                    else:
                        shapes_union = shapes_union.union(row[1])
                        print('Perform union')
                    lst.append(row)
    return(lst)

def fix_fp(path_orig, delim_style = 'os_sep'):
    '''
    Abstracted function to pass single path to for formatting to os.sep of some
    specified sort.  ZU 20220211
    ARGS
    path_orig           path/to/format with delimiters
    delim_style         os_sep = 2x backslash
                        agol   = 2x forward slash
    '''

    if delim_style == 'agol':
        try:
            path_orig = path_orig.replace('\\', '//')
            path_orig = path_orig.replace('////','//')
            path_orig = path_orig.replace('/','//')
            path_orig = path_orig.replace('////','//')
        except AttributeError:
            pass
    if delim_style == 'os_sep':
        try:
            path_orig = path_orig.replace('/','\\')
            path_orig = path_orig.replace('\\\\', '\\')
            path_orig = path_orig.replace('//','\\')
            print('here')
        except AttributeError:
            pass
    return(path_orig)

def fix_fp_df(df, target_col_list, fp_csv_out, delim_style = 'os_sep'):
    '''
    Used to change delimeters from linux to windows or in my case, AGOL to the os.
    If not converted to agol_delim, the Item Description in AGOL gets butchered.
    ZU 20220211 updated
    ARGS
    df                  dataframe to fix, in this case with indices compatible with
                        .at (not integers)
    target_col_list     the col titles of dataframe containing rows to fix
    fp_csv_out          path to csv_out
    delim_style         double backslash for windows, double forward for agol
    '''


    for tc in target_col_list:
        for idx in df.index.to_list():
            path_orig = df.at[idx, tc]
            path_formatted = fix_fp(path_orig, delim_style)
            df.at[idx, tc] = path_formatted

    pd.DataFrame.to_csv(df, fp_csv_out)

def check_layer_source(fp_mxd, fp_csv_inventory, fp_csv_out,
                        df_index_col = 'layer_name', target_col = 'layer_source'):
    df = pd.read_csv(fp_csv_inventory, index_col = df_index_col)
    mxd = arcpy.mapping.MapDocument(fp_mxd)
    lyr_name, lyr_source = [],[]
    for lyr in arcpy.mapping.ListLayers(mxd):
        # supports(DATASOURCE) is a convenient method to determine if layer
        # has value for that attribute essentially
        # visibile obviously if checked on map
        # if (lyr.supports("DATASOURCE")) & (lyr.visible):
        if lyr.supports("DATASOURCE"):
            try:
                temp_path = df.loc[lyr.name, target_col]
                if not arcpy.Exists(temp_path):
                    df.at[lyr.name, 'PATH_CHANGED'] = TRUE
                    lyr_name.append(lyr.name)
                else:
                    df.at[lyr.name, 'PATH_CHANGED'] = FALSE
                # if os.path.normpath(lyr.dataSource) == os.path.normpath(df.loc[lyr.name, target_col]):
                #     df.at[lyr.name, 'MATCHED_SOURCES'] = TRUE
            except:
                pass
    print(lyr_name)
    pd.DataFrame.to_csv(df, fp_csv_out)

def ddp_map_series_index(fc_in, **kwargs):
    '''
    Populate page name and page num for index feature
    ZU 20210908
    ARGS:
    fc_in               index feature class path
    kwarg[pagename]     list of names for pagename if necessary
    '''

    try:
        pagename_list = kwargs['pagename']
    except:
        pass
    arcpy.AddField_management(fc_in, 'pagenum', 'SHORT')
    arcpy.AddField_management(fc_in, 'pagename', 'TEXT', field_length = 50)
    with arcpy.da.UpdateCursor(fc_in, ['pagenum', 'pagename']) as cursor:
        for idx, row in enumerate(cursor):
            row[0] = idx + 1
            if 'pagename' not in locals():
                row[1] = idx + 1
            else:
                row[1] = str(pagename_list[idx])
            cursor.updateRow(row)
def reindex_map_series(fc_in, index_mapping):
    '''
    pass a list of ordered (east to west, north to south, whatever) pagenums
    and reindex the pagenum attribute.  Change pagename too.
    ZU 20210908
    ARGS
    fc_in               path to index fx
    index_mapping       list of integers mapping new index nums i.e. [1,4,3,2]
                        changes 1:1 2:4 3:3 4:2
    '''
    # get pagename list
    pname_orig_order = []
    with arcpy.da.SearchCursor(fc_in, ['pagename']) as cursor:
        for row in enumerate(cursor):
            pname_orig_order.append(row[0])
    # Now update pagename and pagenum
    with arcpy.da.UpdateCursor(fc_in, ['pagenum', 'pagename']) as cursor:
        for idx, row in enumerate(cursor):
            new_pnum = index_mapping[idx]
            row[0] = new_pnum
            # change from page num to index
            row[1] = pname_orig_order[new_pnum - 1]
            cursor.updateRow(row)

def add_lat_long(table_in):
    arcpy.AddField_management(fp_fcs, 'easting', 'DOUBLE')
    arcpy.AddField_management(fp_fcs, 'northing', 'DOUBLE')
    with arcpy.da.UpdateCursor(table_in, ['SHAPE@XY', 'easting', 'northing']) as cursor:
        for row in cursor:
            x = row[0][0]
            y = row[0][1]
            row[1] = round(x,2)
            row[2] = round(y,2)
            cursor.updateRow(row)
def centroid_from_attribute(table_in, att):
    '''
    Take an fc with multiple points with grouping field and find centroid of
    grouped points. For example - if ddp index needed and there are groups of
    points/polys spatially clustered that are desired to be in the same index sheet
    then provide the att argument and df.grouby(att) will find the centroid of
    that feature.
    ARGS
    table_in            table (fc) to generate centroids
    att                 groupby attribute
    OUT
    fp_out              feature class centroids
    '''
    # https://gis.stackexchange.com/questions/307782/creating-point-feature-class-from-multiple-points-using-list-comprehension-and-a
    att_list = []
    x, y = [],[]
    with arcpy.da.SearchCursor(table_in, [att, 'SHAPE@XY']) as cursor:
        for rw in cursor:
            att_list.append(rw[0])
            x.append(rw[1][0])
            y.append(rw[1][1])
    del cursor
    del rw

    df = pd.DataFrame(np.column_stack([att_list, x, y]), columns = ['target_att', 'x', 'y'])
    # ensure coords are numeric
    df['x'] = pd.to_numeric(df['x'])
    df['y'] = pd.to_numeric(df['y'])
    ser_centroid_x = df.groupby('target_att')['x'].mean()
    centroid_x_vals = ser_centroid_x.values
    centroid_y_vals = df.groupby('target_att')['y'].mean().values
    # names/attributes we grouped with
    index = ser_centroid_x.index.to_list()
    points = []
    for x,y in zip(centroid_x_vals, centroid_y_vals):
        points.append(arcpy.Point(x,y))
    sr = arcpy.Describe(table_in).spatialReference
    points = [arcpy.PointGeometry(p, sr) for p in points]
    # create feat
    basename = os.path.split(table_in)[-1]
    basedir = os.path.split(table_in)[0]
    basename.replace('.shp', '')
    name_out = '{}_centroids'.format(basename)
    fp_out = os.path.join(basedir, name_out)
    feat_field = '{}_val'.format(att)
    arcpy.CreateFeatureclass_management(basedir, name_out, "POINT")
    arcpy.AddField_management(fp_out, feat_field, "TEXT")
    cursor = arcpy.da.InsertCursor(fp_out, [feat_field, 'SHAPE@XY'])
    for pt, id in zip(points, index):
        cursor.insertRow((id, pt))
    del cursor

def centroid_to_index(table_in, id_att, template_str, feet=True,  wc = '', **kwargs):
    '''
    To be used in a series with centroid_from_attribute.  Get centroids -either
    from multiple inputs like coho_salvage figures for RES, or most likley from
    single points like before.  Format table_in to include fields 'index_scale',
    and id_add field
    ARGS
    table_in        centroid fc
    id_att          attribute name for id field i.e. 'Name' - basically the
                    ddp index page name
    template_str    to pull scale factors from csv lookup table - i.e. 11x17_landscape
    feet            if true, horiz unit convert to feet.  default of false assumes map
                    units horiz in meters
    wc              pass a dict with {attribute name: [val1, val2, ...n]}
    kwargs          update_rows --> if updating the ddp polygons directly after their
                    creation.  Doesn't matter the val, just passing the kwarg
    '''

    # GRAB FIRST in case naming convention not obsrved and function fails
    basedir = os.path.split(table_in)[0]
    feat_name = os.path.split(table_in)[1]
    try:
        idx_name = kwargs['idx_name']
        index_fc_name = idx_name
    except KeyError:
        index_fc_name = '{}_index'.format(feat_name.replace('_centroid',''))
    fp_out = os.path.join(basedir, index_fc_name)

    # GET BASE OFFSETS FROM LOOKUP SPREADSHEET
    reference_csv = r'C:\Users\uhlmann\Box\WR Users\3.0 - Employees\zuhlmann\python_df_docs\df_utility_csvs\centroid_generator.csv'
    df = pd.read_csv(reference_csv, index_col = 'template_str')

    if feet:
        cm_m = .01
        m_ft = 3.28084
        unit_conv = cm_m * m_ft
    else:
        cm_m = 0.01
        unit_conv = cm_m
    width_cent = df.loc[template_str, 'width_cent']
    ht_cent = df.loc[template_str, 'height_cent']
    try:
        rescale = kwargs['rescale']
        e_len_base = width_cent * unit_conv * rescale
        n_len_base = ht_cent * unit_conv *rescale
    except KeyError:
        e_len_base = width_cent * unit_conv
        n_len_base = ht_cent * unit_conv


    if wc != '':
        [(k,v)] = wc.items()
        if not isinstance(v[0], str):
            v = [str(vi) for vi in v]
        # now create wc
        v_str = ','.join(v)
        wc = '{} in ({})'.format(k, v_str)
        print('WHERE_CLAUSE', wc)
    # if updating
    try:
        kwargs['update_rows']
        with arcpy.da.UpdateCursor(fp_out, ['SHAPE@XY', 'SHAPE@', 'index_scale'], where_clause = wc) as cursor:
            for row in cursor:
                # centroids
                x = row[0][0]
                y = row[0][1]
                scale = row[2]
                print(scale)
                e_w = scale * (e_len_base/2)
                n_s = scale * (n_len_base/2)
                ul = arcpy.Point(x - e_w, y + n_s)
                ur = arcpy.Point(x + e_w, y + n_s)
                ll = arcpy.Point(x - e_w, y - n_s)
                lr = arcpy.Point(x + e_w, y - n_s)
                extent = arcpy.Array([ul,ur,lr,ll])
                p = arcpy.Polygon(extent)
                row[1]=p
                cursor.updateRow(row)
        del cursor
    #if proceeding normally
    except KeyError:
        att_list = []
        poly = []
        index_scale = []
        with arcpy.da.SearchCursor(table_in, [id_att, 'SHAPE@XY', 'index_scale','action'], where_clause = wc) as cursor:
            for row in cursor:
                # unable to add boolean value to table to indicate 'skip', so created
                # action col for multiple
                if row[3] != 'skip':
                    x = row[1][0]
                    y = row[1][1]
                    scale = row[2]
                    e_w = scale * (e_len_base/2)
                    n_s = scale * (n_len_base/2)
                    ul = arcpy.Point(x - e_w, y + n_s)
                    ur = arcpy.Point(x + e_w, y + n_s)
                    ll = arcpy.Point(x - e_w, y - n_s)
                    lr = arcpy.Point(x + e_w, y - n_s)
                    extent = arcpy.Array([ul,ur,lr,ll])
                    poly.append(arcpy.Polygon(extent))
                    # get id_name to add below
                    att_list.append(row[0])
                    index_scale.append(int(row[2]))
            del cursor

        arcpy.CreateFeatureclass_management(basedir, index_fc_name, "POLYGON")
        arcpy.AddField_management(fp_out, id_att, "TEXT")
        arcpy.AddField_management(fp_out, 'index_scale', "LONG")

        # CREATE INDEX FC
        cursor = arcpy.da.InsertCursor(fp_out, [id_att, 'index_scale','SHAPE@'])
        for id, p in enumerate(poly):
            id_val = att_list[id]
            scale = index_scale[id]
            cursor.insertRow((id_val, scale, p))
        del cursor

def sql_from_csv_to_lyr(ref_csv, source_dict, field_dict, source_col, val_col, **kwargs):
    '''
    Makes feature layer(s) for the map based off ref_csv.  refer to
    GIS_Request_Tracking//GIS_Requests_RES//2021_09_14
    folder for selection_table.csv and order for reference.  csv will have a column
    with source_col - string for dictionary to reference file paths and field title.
    CSV also includes values to use in sql_statement. ZU 20210917
    ARGS
    ref_csv                 csv with source_str and values to match
    source_dict             dictionary with source_str matching fp_source in dict
    field_dict              dict with source_str matching field to match vals
                            in sql statment.  Note that these field titles are NOT
                            present in table.
    source_col             string val of column containing...strings for source_dict
    val_col                 vals to create field_name in (val) in sql_str.  So the
                            values in column to select from table
    KWARGS
    select_keys             if only using select fc_str, then use this.  For example
                            if there are multiple keys in dictionary, specify which to
                            select
    '''

    df = pd.read_csv(ref_csv)
    # only select keys
    try:
        fc_str = kwargs['select_keys']
        fc_str = [fc_str]
    # use all keys
    except KeyError:
        fc_str = list(source_dict.keys())
    for s in fc_str:
        fp = source_dict[s]
        field = field_dict[s]
        # .all is a hack towards unique vals
        vals = df[df[source_col] == s].groupby(val_col).all().index.to_list()
        # print(vals)
        if isinstance(vals[0], str):
            pass
        else:
            vals = [str(v) for v in vals]
        sql_str = "','".join(vals)
        sql_str = "('{}')".format(sql_str)
        sql_str = '"{}" IN {}'.format(field, sql_str)
        try:
            kwargs['make_feature_layer']
            arcpy.MakeFeatureLayer_management(fp, '{}_lyr'.format(s), sql_str)
        except KeyError:
            pass
        try:
            kwargs['return_sql_statement']
            return(sql_str)
        except:
            pass
def calc_acreage(fp_in, units, geodesic = False):
    '''
    Add acreage field populated with proper stuff. 20210921
    ARGS:
    fp_in               field to operate upon
    units               str Feet Miles Acres, etc
    geodesic            Read link below for info on choosing
    '''
    # https://community.esri.com/t5/new-to-gis-questions/planar-vs-geodesic-area-length/td-p/350368
    # existing_fields = [f.name for f in arcpy.ListFields(fp_fcs)]
    # if 'acres' not in existing_fields:
    #     arcpy.AddField_management(fp_fcs, 'acres', 'TEXT')
    # else:
    #     pass
    if geodesic:
        area_str = ['AREA_GEODESIC', 'LENGTH_GEODESIC']
    else:
        area_str= ['AREA', 'LENGTH']
    shape_type = arcpy.da.Describe(fp_in)['shapeType']
    if shape_type == 'Polygon':
        arcpy.AddGeometryAttributes_management(fp_in, area_str[0], '',units,'')
        fname = 'POLY_AREA'
        units_lc = units.lower()
        new_fname = 'area_{}'.format(units_lc)
    if shape_type == 'Polyline':
        arcpy.AddGeometryAttributes_management(fp_in, area_str[1], units,'','')
        fname = 'LENGTH'
        units_lc = units.replace('(United States)','').replace(' ','_').lower()
        new_fname = 'length_{}'.format(units_lc)
    arcpy.AlterField_management(fp_in, fname, new_fname, new_fname)

def union_z(feat1, feat2, fp_out, where1 = '', where2 = ''):
        lyr1 = arcpy.MakeFeatureLayer_management(feat1, where1)
        lyr2 = arcpy.MakeFeatureLayer_management(feat2, where2)
        arcpy.Union_analysis([lyr1,lyr2], fp_out)

def find_gdb_dir(df, target_col):
    new_col_list = []
    orig_fp_list = df[target_col]
    for fp in orig_fp_list:
        try:
            comp = fp.split('//')
            comp_len = len(comp)
            ct = 1
            gdb_found = False
            for gd in comp:
                if '.gdb' in gd:
                    new_col_list.append(gd[:-4])
                    gdb_found = True
                elif (ct == comp_len) and not gdb_found:
                    new_col_list.append('ADD_DIR_MANUALLY')
                ct+=1
        except AttributeError:
            new_col_list.append('NO_GDB_YET')
    print(len(new_col_list))
    df['GDB_OR_DIR']=new_col_list
    return(df)

def aprx_inventory(aprx_dir, csv_dir_out):
    '''
    List layers and properties used in aprx.  ZU 11/16/2021
    ARGS:
    fp_aprx            path/to/pro_dir/<filename>.aprx
    fp_csv_out          full path - path/to/dir/<filename>.csv

    '''
    aprx = arcpy.mp.ArcGISProject(aprx_dir)
    # maps = aprx.listMaps()
    lyts = aprx.listLayouts()
    maps_active = []
    for l in lyts:
        mapframe_present = False
        lyt_map_names = []
        el_list = l.listElements()
        for el in el_list:
            if el.type == 'MAPFRAME_ELEMENT':
                mapframe_present = True
                map = el.map
                map_name = map.name
                if len(maps_active) == 0:
                    maps_active.append(map)
                else:
                    mn_list = [m.name for m in maps_active]
                    if map_name not in mn_list:
                        maps_active.append(map)
                lyt_map_names.append(map_name)
        # Because layouts without mapframes will break this if not conditional
        if mapframe_present:
            if 'lyt_map_dict' not in locals():
                lyt_map_dict = {l.name:lyt_map_names}
            else:
                lyt_map_dict.update({l.name:lyt_map_names})
        # remove layouts without mapframes
        else:
            lyts.remove(l)

    # names = [m.name for m in maps]
    for m in maps_active:
        map_name = m.name
        lyrs = m.listLayers()
        c0,c1,c2,c3,c4,c5 = [],[],[],[],[],[]
        print('INVENTORYING map: {}'.format(m.name))
        for lyr in lyrs:
            if not lyr.isBasemapLayer:
                try:
                    c1.append(lyr.name)
                except AttributeError:
                    c1.append('')
                try:
                    c2.append(lyr.dataSource)
                except NameError:
                    c2.append('')
                except AttributeError:
                    c2.append('')
                try:
                    c3.append(lyr.visible)
                except NameError:
                    c3.append('')
                except AttributeError:
                    c3.append('')
                try:
                    c4.append(lyr.isRasterLayer)
                except NameError:
                    c4.append('')
                try:
                    c5.append(lyr.definitionQuery)
                except NameError:
                    c5.append('')
                except AttributeError:
                    c5.append('')
                # get map name
                c0.append(map_name)
        df_cols = np.column_stack([c0, c1, c2, c3, c4, c5])
        df_col_names = ['map','layer_name','data_source','visible','raster','def_query']
        df = pd.DataFrame(df_cols, columns = df_col_names)
        if 'df_map_dict' not in locals():
            df_map_dict = {m.name:df}
        else:
            df_map_dict.update({m.name:df})

    for l in lyts:
        ln = l.name
        fp_csv_out = os.path.join(csv_dir_out, '{}_aprx_inventory.csv'.format(ln))
        map_name_list = lyt_map_dict[ln]
        for mn in map_name_list:
            if 'df_lyt' not in locals():
                df_lyt = df_map_dict[mn]
            else:
                df_lyt = df_lyt.append(df_map_dict[mn])
        pd.DataFrame.to_csv(df_lyt, fp_csv_out)
        del df_lyt

def df_to_df_transfer(df_source, df_target, match_col_list, replace_col_list, **kwargs):
    '''
    Taken from spyder_arcgis_oop.  Should be incorprated into that module and this
    funtionality removed and abstracted here. ZU 20211208
    ARGS:
    df_target               dataframe to add values to based off other arguments
    df_source               dataframe to transfer values from
    match_col_list          columns to match from table to table [col_source_str, col_target_str]
    replace_col_list        col we are searching for value in df_source and
                            col where we are replacing in target
    target_val              val to search for in replace_col
    RETURNS:
    df_target              target_df with transferred target_vals
    '''
    match_col_source = match_col_list[0]
    match_col_target = match_col_list[1]
    replace_col_source = replace_col_list[0]
    replace_col_target = replace_col_list[1]
    # If only transfering column values with specific value.
    df_source[match_col_source] = df_source[match_col_source].apply(lambda x: os.path.normpath(x))
    df_target[match_col_target] = df_target[match_col_target].apply(lambda x: os.path.normpath(x))
    try:
        target_val = kwargs['target_val']
        source_indices = df_source.index[df_source[replace_col_source]==target_val]
        # file paths most likely
        vals_match = df_source.loc[source_indices][match_col_source].to_list()
        replace_vals = df_source.loc[source_indices][replace_col_source].to_list()
    # bulk transfer of replace_col_source to replace_col_target
    except KeyError:
        df_select = df_source[df_source[replace_col_source].notnull()]
        print(df_select[df_select[replace_col_source] != ''])
        # print(df_select[df_select[replace_col_source] != ''][replace_col_source])

    # indices in df_target matching source indices
    for row in df_select.itertuples():
        idx = getattr(row, match_col_source)
        val = getattr(row, replace_col_source)
        idx = df_target[df_target[match_col_target]==idx].index.values
        if len(idx)==1:
            idx = idx[0]
        df_target.loc[idx, replace_col_target]=val
    return(df_target)
        # target_indices = idx + df_target[df_target[match_col_target==val]].index.to_list()
    # target_indices = [df_target[df_target[match_col_target]==val] for val in vals_match]

def norm_file_path_df(df, **kwargs):
    '''
    assumes that path/to/folders columns are not Index cols
    '''

    try:
        target_cols = kwargs['target_col']
        print('in try')
        if not isinstance(target_cols, list):
            target_cols = [target_cols]
            print('in not')
    except KeyError:
        target_cols = ['DATA_LOCATION_MCMILLEN_JACOBS',
                    'DATA_LOCATION_MCM_ORIGINAL',
                    'DATA_LOCTION_MCM_STAGING']

    cols_existing = df.columns.to_list()
    for c in target_cols:
        print('for loop')
        if c in cols_existing:
            for i in df.index:
                try:
                    fp_orig = df.loc[i, c]
                    fp_new = os.path.normpath(fp_orig)
                # If no value in row, then a float will be rejected by os.path.normpath
                except TypeError:
                    fp_new = df.loc[i,c]
                df.at[i,c] = fp_new
    return(df)

def update_df_inventory(df_orig, gdb_dir_list, tc = 'DATA_LOCATION_MCMILLEN_JACOBS',
                        offline = True, basic_cols=True, **kwargs):
    '''
    ZU 20220201.  Update data inventories if changed.  Finds omitted (deleted),
    comitted (existing) and added (new) feature classes. NOTE!! need to make
    df['ASSIMILATE'] = conditional.  If already contains "added_<date>" or
    "predates_<date>", then do not replace with "predates_<current_date"

    ARGS
    df_orig             dataframe of current non-updated gdb - i.e. mapping_gdb_inventory.csv
    gdb_dir_or_list     path/to/gdb or [path/to/gdb]
                        note - currently only functions with len = 1 list of fp_gdb
    dset_ll             list of lists of dsets per gdb
    RETURNS
    df_assim            dataframe combining current inventory with newly created
                        dataframe of current gdb contents (compare_data.file_paths_arc)
    '''
    # Inventory all specified gdbs in maestro
    import compare_data

    for idx, gdb in enumerate(gdb_dir_list):
        try:
            dsets = kwargs['dsets_desired']
            if 'df_current' not in locals():
                df_current = compare_data.file_paths_arc(gdb, True, basic_cols, dsets_desired = dsets)
            else:
                temp = compare_data.file_paths_arc(gdb, True, basic_cols, dsets_desired = dsets)
                df_current = df_current.append(temp)
        except KeyError:
            if 'df_current' not in locals():
                df_current = compare_data.file_paths_arc(gdb, True, basic_cols)
            else:
                temp = compare_data.file_paths_arc(gdb, True, basic_cols)
                df_current = df_current.append(temp)

    # standardize paths
    df_current = norm_file_path_df(df_current, target_col = tc)
    df_orig = norm_file_path_df(df_orig, target_col = tc)

    # since all FCs from same gdb, just grab first path/to/gdb
    # Get column iloc id of DATA_LOCATION
    col_id = df_current.columns.get_loc(tc)
    fp_fcs_current = os.path.normpath(df_current.iloc[0, col_id])
    fp_components = fp_fcs_current.split(os.sep)
    # print(fp_components)
    if offline:
        csv = r'C:\Users\uhlmann\Box\GIS\Project_Based\Klamath_River_Renewal_MJA\GIS_Data\data_inventory_and_tracking\offline_lookup_table.csv'
        olt = pd.read_csv(csv, index_col = 'gdb_str')

        try:
            gdb_str = [v.replace('.','_') for v in fp_components if '.gdb' in v][0]
            offline_base = olt.loc[gdb_str, 'offline']
            online_base = olt.loc[gdb_str, 'online']
        except IndexError:
            pass
        # Translate to online path/to... and replace in df
        tc_online = [fp.replace(offline_base, online_base) for fp in df_current[tc].to_list()]
        df_current[tc] = tc_online
    else:
        pass

    df_current = df_current.set_index(tc)
    df_orig = df_orig.set_index(tc)

    # Added, Omited and Comitted
    dloc_o = df_orig.index.to_list()
    dloc_c = df_current.index.to_list()
    so = set(dloc_o)
    sc = set(dloc_c)

    # update updates the series and will NOT assign to variable
    added = list(sc - so)
    omitted = list(so - sc)
    comitted = copy.copy(so)
    comitted = list(comitted.intersection(sc))

    # APPEND and remove duplicates
    df_assim = df_orig.append(df_current)
    # oddly, keep first will Flag the last duplicates as True, the first
    # duplicates as false, and non-duplicates as false ZU 20220202
    df_assim = df_assim[~df_assim.index.duplicated(keep='first')]

    todays_date = datetime.datetime.today().strftime('%Y%m%d')
    df_assim.loc[added, 'ASSIMILATED'] = todays_date
    df_assim.loc[omitted, 'ASSIMILATED'] = 'removed'
    df_assim.loc[comitted, 'ASSIMILATED'] = 'predates_{}'.format(todays_date)

    return(df_assim)

def mark_duplicate_rows(df, target_col, ispath = False):
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
    return(df)
# # NOTES
# # getting path componenets
# # 20210409
# pathnorm = os.path.normpath(fp_desired)
# path_components = pathnorm.split(os.sep)

def rectify_source_maestro(df_source, df_maestro, dir_out, fname_source, fname_maestro):
    '''
    Used to rectify a maestro and source (kauai_offline_gdb_inentory for instance)
    to each other.  Add items missing from one to the other and vice versa. 20220308
    '''
    if '.csv' not in fname_source:
        fname_source = '{}.csv'.format(fname_source)
    if '.csv' not in fname_maestro:
        fname_maestro = '{}.csv'.format(fname_maestro)
    index_source = df_source.index
    index_maestro = df_maestro.index
    add_source_index = index_maestro.difference(index_source)
    add_maestro_index = index_source.difference(index_maestro)
    append_source = df_maestro.loc[add_source_index]
    append_maestro = df_source.loc[add_maestro_index]
    df_source = df_source.append(append_source)
    df_maestro = df_maestro.append(append_maestro)
    df_source.to_csv(os.path.join(dir_out, fname_source))
    df_maestro.to_csv(os.path.join(dir_out, fname_maestro))

def assim_df_cols(df_target, df_append, col_mapping_list):
    '''
    assimilating notes from maestro to gdb i.e. item_desc to gdb_master.
    Used for notes, but could be used for any text column.  I used this to combine
    notes from two df (df_target - gdb / df_append - maestro) into notes_assim
    20220608.
    ARGS
    df_target                 dataframe 1 to assimilate columns
    df_append                 dataframe 2 to grab column text and add to col from
                                df_target
    col_mapping_list    list with cols from d1 and d2 respectively to combine
    RETURN
    df_assim            datatrame df1_target with assimilated column
    '''

    col_target = col_mapping_list[0]
    col_append = col_mapping_list[1]
    #
    df_append = df_append[[col_append]].copy()
    df_append = df_append.rename(columns = {col_target:'{}_TARGET'.format(col_target)})
    df_assim = df_target.join(df_append)

    notes_comb=[]
    for n, n2 in zip(df_assim['NOTES'], df_assim['NOTES_TARGET']):
        n_null = pd.isnull(n)
        n2_null = pd.isnull(n2)
        if n_null:
            if n2_null:
                temp = ''
            else:
                temp = n2
        elif n2_null:
            if not n_null:
                temp = n
        else:
            if not (n == n2):
                temp = '{}\n{}'.format(n, n2)
            else:
                temp = n
        notes_comb.append(temp)
    df_assim['NOTES_ASSIM'] = notes_comb
    return(df_assim)
