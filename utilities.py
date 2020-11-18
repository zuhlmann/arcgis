import os
import pandas as pd
import math
import sys
sys.path = [p for p in sys.path if '86' not in p]
import arcpy
import numpy as np
import datetime
# from compare_data import *

def show_table(display_preference):
    '''
    ARGS:
    display_preference:  desc or path. string
    '''
    from tabulate import tabulate
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

def parse_dir(obj, substr):
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

    indices_match = [idx for idx, method in enumerate(methods) if substr in method]
    methods_match = [methods[idx] for idx in indices_match]
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
    return True

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
        with open('C:/Users/uhlmann/box_offline/bathymetry_project/overlap_extents_{}.txt'.format(reservoir_name), 'w') as text_file:
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
    ddp = mxd_doc.dataDrivenPages
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
        # if (lyr.supports("DATASOURCE")) & (lyr.visible):
        if lyr.supports("DATASOURCE"):
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
def mxd_inventory_csv(fp_base, **kwargs):
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
            mxd_list = list(mxd_list)
    except KeyError:
        mxd_list = [item for item in os.listdir(fp_base) if '.mxd' in item]
    fp_mxd_list = [os.path.join(fp_base, fname_mxd) for fname_mxd in mxd_list]
    lyr_list = []
    lyr_name = []
    lyr_source = []
    mxd_name = []
    for idx, fp_mxd in enumerate(fp_mxd_list):
        mxd = arcpy.mapping.MapDocument(fp_mxd)
        mxd_name_temp = mxd_list[idx]
        for lyr in arcpy.mapping.ListLayers(mxd):
            # supports(DATASOURCE) is a convenient method to determine if layer
            # has value for that attribute essentially
            # visibile obviously if checked on map
            # if (lyr.supports("DATASOURCE")) & (lyr.visible):
            if lyr.supports("DATASOURCE"):
                lyr_name.append(lyr.name)
                lyr_source.append(lyr.dataSource)
                mxd_name.append(mxd_name_temp)
            else:
                pass

        # plane old mxd name
    df = pd.DataFrame(np.column_stack([mxd_name, lyr_name, lyr_source]), columns = ['map_name', 'layer_name', 'layer_source'])
    fp_out = os.path.join(fp_base, 'RAMP_layer_inventory.csv')
    pd.DataFrame.to_csv(df, fp_out)

def write_folder_contents(fp):
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
    basic_str = '\n'.join(files)
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

def return_mxd_obj(fp_mxd):
    '''
    helpful methods and such to add to mapping doc
    arcpy.mapping.ListDataFrames
    '''
    mxd = arcpy.mapping.MapDocument(fp_mxd)
    return(mxd)

def parse_item_desc(sub_item_list, target_key, target_val):
    '''
    Quick utility used for adding and updating Item Description metadata via
    xml files.  ZRU 11/15/2020
    ARGS:
    sub_item_list = pass list from idPurp of xml for shapefiles.  The list will be
                    the item_desc_str.splitlines() which splits at /n - essentially
                    splitting each key:val pair into one item in list i.e.
                    ['DATA_LOCATION_MCMILLEN_JACOBS: <file path',
                    'DATE_ADDED_AGOL: 20201115']
    target_key      list of target keys i.e. [DATA_LOCATION_MCMILLEN_JACOBS,
                                                DATE_ADDED_AGOL]
    target_val      list of vals to pair with each target.  len(target_key) == len(target_list)
    RETURNS
    New Item Description list with strings per sub item
    '''
    # initiate as false
    replaced_sub_item = False
    idx_offset = 0
    for idx, sub_item in enumerate(sub_item_list):
        # if empty sub_items shrunk the list, idx will be notched back one at a time
        idx_adjusted = idx - idx_offset
        # if empty string need to remove
        if sub_item != '':
            temp_idx = sub_item.index(':')
            # get exact sub_item_key i.e. SOURCE_CONTACT_MCMILEN
            sub_item_key = sub_item[:temp_idx]
            # if already present, then replace and return new list
            if target_key == sub_item_key:
                print('replacing subitem')
                sub_item_list[idx_adjusted] = '{}: {}'.format(target_key, target_val)
                replaced_sub_item = True
        # if empty string in sub items, remove
        else:
            idx_adjusted = idx - idx_offset
            sub_item_list = [item for idx2, item in enumerate(sub_item_list) if idx_adjusted != idx2]
            idx_offset += 1
    # if no matched sub items were found, then simply add to list
    if not replaced_sub_item:
        sub_item_list.append('{}: {}'.format(target_key, target_val))
    # if no matches are found, then return original list
    return(sub_item_list)

def create_poly_from_pts(table_in, fp_out, offsets):
    '''
    Takes points and offsets by specified e,w,s,n into polygon feat class
    ZRU 20201116

    table_in        point feature from arc.  can be adapted for csv
    fp_out          full path name to gdb or with .shp
    offsets         list in [w,e,n,s] units of projection system
    '''
    w, e, n, s = offsets[0], offsets[1], offsets[2], offsets[3]
    poly = []
    with arcpy.da.Cursor(table_in, ['SHAPE@XY']) as cursor:
        for row in cursor:
            x = row[0][0]
            y = row[0][1]
            ul = arcpy.Point(x - w, y + n)
            ur = arcpy.Point(x + e, y + n)
            ll = arcpy.Point(x - w, y - s)
            lr = arcpy.POint(x + e, y - s)
            extent = arcpy.Array([ul,ur,lr,ll])
            poly.append(arcpy.Polygon(extent))
    arcpy.CopyFeatures_management(poly, fp_out)
