import arcpy
import os

def buffer_range_merge(fp_in, buffer_list, base_dir_out):
    '''
    multiple buffers and merging into one feature.  ZrU 2/22/21 for NFMS weeds
    buffer. Not the if/elif/else statmement pretty rough - if fp_in passed by dragging
    from TOC in ArcMap then it will simply be string of layer name.  This block
    deals with full paths and shapefils (shp not yet tested though...)
    SO if 10 buffer sizes are passed, the output will have 10 polygons.
    Note - need to add add_field for buff_distance in output feature

    ARGS:
    fp_in           file path of feature to buffer
    buffer_list     ['<len/size> <units>, <len/size> <units>, ...]
                    i.e ["100 feet", "20 feet", "10 feet"]
    base_dir_out    self explanatory
    '''
    # hack to deal with inability to delete in_memory without reading a thesis on
    # or else running multiple times will error out because in_memory layers have
    # same name
    # arc madness: https://community.esri.com/t5/python-questions/how-to-delete-in-memory-table/m-p/162044
    arcpy.env.overwriteOutput = True

    # create string to used to create output filename
    buffer_string_formatted = [buff_string.replace(' ', '') for buff_string in buffer_list]
    buffer_string_formatted = '_'.join(buffer_string_formatted)
    # Note - have not tried using .shp yet
    if fp_in[-4:] == '.shp':
        fname_orig = os.path.splitext(os.path.basename(fp_in)[-1])[0]
    # if full file path to feature
    elif '\\' in fp_in:
        fname_orig = os.path.split(fp_in)[-1]
    # if string dragged from TOC directly (in ArcMap mxd)
    else:
        fname_orig = fp_in
    fname_new = '{}_merged_buffers_{}'.format(fname_orig, buffer_string_formatted)
    fp_out = os.path.join(base_dir_out, fname_new)
    lyr_list = []
    for buff_val in buffer_list:
        lyr = 'in_memory\\buff_{}'.format(buff_val.replace(' ', '_'))
        # accumulate buffered layer names to merge
        lyr_list.append(lyr)
        arcpy.Buffer_analysis(fp_in, lyr, buffer_distance_or_field = buff_val, dissolve_option = 'ALL')

    arcpy.Merge_management(lyr_list, fp_out)

def union_custom(fcs_in, fp_out):
    arcpy.env.overwriteOutput = True
    # check if fcs_in passed as list
    if not isinstance(fcs_in, list):
        fcs_in = [fcs_in]
    else:
        pass
    for feat in fcs_in:
        fcs_name = feat.replace(' ','_')
        fcs_name = 'in_memory/{}_dissolved'.format(fcs_name)
        # create list of strings for argument into union
        if 'fcs_dissolved' not in locals():
            fcs_dissolved = [fcs_name]
        else:
            fcs_dissolved.append(fcs_name)
        # dissolve feature layers
        arcpy.Dissolve_management(feat, fcs_name)
    arcpy.Union_analysis(fcs_dissolved, fp_out)
