import os
import pandas as pd
from tabulate import tabulate
from compare_data import *

def show_table(display_preference):
    '''
    ARGS:
    display_preference:  desc or path. string
    '''
    paths_table = """C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers/path_list.csv"""
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
    pd.DataFrame.to_csv(df, paths_table)
def add_table_entry(alias, desc, fp):
    '''
    can add table entry by passing three required args
    ARGS
    alias       string. alias should be 'fp_<descriptive name>'
    desc        description of feature class
    fp          file path to dataset
    '''
    paths_table = """C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers/path_list.csv"""
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
    paths_table = """C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers/path_list.csv"""
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
    paths_table = """C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/compare_vers/path_list.csv"""
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
def new_unpack_cursor(fp_in):
    # from stack exchange Q I posted
    with arcpy.da.SearchCursor(fp_in, ['OBJECTID', 'name']) as cursor:
        rows = [row for row in cursor]    # I don't know if zip() works with cursor (can't test)
        objectid, name = zip(*rows) # If it does work, use objectid, name = list(zip(*cursor))
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

def sequential_update_field(fp, field, incr):
    '''
    quick tool to add sequential numbers to field
    '''
    if isinstance(field, list):
        pass
    else:
        field = [field]
    with arcpy.da.UpdateCursor(fp, field) as cursor:
        ct = 1
        for row in cursor:
            row[0] = ct
            cursor.updateRow(row)
            ct += incr

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
    fp_out              file path out
    unmapped            Boolean.  if True then include unmapped fields from target.
                        this will set vals in fp_append to NULL since presumably
                        those values do not exist
    '''
    df = pd.read_csv(mapping_csv)
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
        target_names_unmapped_all = [field.name.encode('utf-8') for field in fields]
        target_type_unmapped_all = [field.type for field in fields]
        # create dataframe for selecting type
        df = pd.DataFrame(np.column_stack([target_names_unmapped_all, target_type_unmapped_all]), columns = ['field_name', 'field_type'])
        target_names_unmapped_set = set(target_names_unmapped_all)
        target_set = set(target_fields)
        # remove target values which will be mapped
        target_names_unmapped_set.difference_update(target_set)
        target_names_unmapped_list = list(target_names_unmapped_set)
        target_types_unmapped = df[df['field_name'].isin(target_names_unmapped_list)].field_type.tolist()
        target_names_unmapped = df[df['field_name'].isin(target_names_unmapped_list)].field_name.tolist()
        print(df)

        # add fields to append fc
        # https://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy-classes/field.htm
        # The field object's type property does not match completely
        #  with the choices listed for the Add Field tool's field_type parameter.
        #To allow the Add Field tool to use all type keywords, field types are
        # mapped: Integer to LONG, String to TEXT, and SmallInteger to SHORT.
        # Not sure if this is necessary
        dict_ToField = {'Integer':'LONG', 'String':'TEXT', 'SmallInteger':'SHORT'}
        for name_add, type_add in zip(target_names_unmapped, target_types_unmapped):
            print('in the for loop')
            # because of wierd disconnect betw addField and FieldMappings type F these types
            if type_add in ['OID', 'GUID', 'Geometry']:
                pass
            # now that we are types AddField can handle
            elif name_add in ['Shape']:
                pass
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
        # [target_fields.append(unmapped_field) for unmapped_field in target_names_unmapped_list]
        # [append_fields.append(unmapped_field) for unmapped_field in target_names_unmapped_list]
        # [new_field_names.append(unmapped_field) for unmapped_field in target_names_unmapped_list]
        print(target_names_unmapped_list)
        print(target_fields)
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

def parse_dir(obj, substr):
    '''
    matchses substrings to dir(obj) from python interactive
    document and add to: ZRU 5/26/2020
    '''
    # if dir used on list:
    if isinstance(obj, list):
        methods = dir(obj)
        print('here')
        pass
    # if dir is used on locals then a dictionary is returned
    elif isinstance(obj, dict):
        methods = obj.keys()
        print('dict')

    indices_match = [idx for idx, method in enumerate(methods) if substr in method]
    methods_match = [methods[idx] for idx in indices_match]
    return(indices_match, methods_match)
