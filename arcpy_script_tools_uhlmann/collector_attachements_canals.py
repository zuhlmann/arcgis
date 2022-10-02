import arcpy
from arcpy import da
import os
import pandas as pd
import numpy as np
import copy

# Directly from here:
# https://support.esri.com/en/technical-article/000011912
# Adapted majorly to link objectids betw attach table and fc
# NOt perfect but pretty solid (ZU 20210825)

# ARGUMENTS
# fc_in             feature class from relational gdb
# inTable           Attach table from relational gdb
# basedir           output directory.  Use a not huge path because subdir and filenames
#                   created by script are LONG and > 250 paths will break this
# field_reference   Attribute Name i.e. Name, OBJECTID.  This will be used in file
#                   and subdir names
# use_all_fields    boolean - true to output all fields to csv for field report
# rel_globalid_field   name of globalid field from relational database diretly downloaded from AGOL
# fc_globalid_field    if updating extracted fc, process is arcpy.da.searchcursor to get globalid
#                   from FGBD and join to extracted FC.

fc_in = arcpy.GetParameterAsText(0)
inTable = arcpy.GetParameterAsText(1)
basedir = arcpy.GetParameterAsText(2)
field_reference = arcpy.GetParameterAsText(3)
use_all_fields = arcpy.GetParameterAsText(4)
rel_globalid_field_fc = arcpy.GetParameterAsText(5)

'''
field_reference         field name from fc_in to use in filename prefix i.e. name or id.
                        filename will then = name5_... for example
in_table                matching attach table from rel gdb
basedir                 where photos will be saved.  A subdir with fc_in title will be created.
                        then <field_reference_name>_<field_reference_val> subdir beneath
                        i.e. name_5
use_all_fields          output all fields from FC.  This is a true/false checkbox
rel_globalid_field_fc   attribute name created in fc_in which holds vals for relational fgdb.
                        Note that field name can be anything, but field values need
                        to match relative globalid from rel fgdb i.e. 1690814A-4E54-4DBC-866E-18E87550D7D2
'''
# check for shp - DON'T THINK this matters because feature class is specified as fc_in data type
if fc_in[-3:] == 'shp':
    feat_name = os.path.split(fc_in)[-1][:-4]
else:
    feat_name = os.path.split(fc_in)[-1]

all_fields = [f.name for f in arcpy.ListFields(fc_in) if 'shape' not in f.name.lower()]
base_fields = [field_reference, 'GLOBALID', 'notes']
if use_all_fields:
    fld_list = all_fields
else:
    fld_list = base_fields
# 1) FEATURE CLASS TABLE
# initiate list of list to add vale
fld_val_list = [[] for i in range(len(fld_list))]
# indices to match list
fld_id_list = list(range(len(fld_val_list)))
with da.SearchCursor(fc_in, fld_list) as cursor:
    for row in cursor:
        for id in fld_id_list:
            if fld_list[id] == rel_globalid_field_fc:
                # get exact globid name for below
                globalid_field_name = fld_list[id]
                temp = row[id]
                temp = temp.replace('{','').replace('}','')
                globid_id = copy.copy(id)
            else:
                temp = row[id]
            fld_val_list[id].append(temp)

df_fc = pd.DataFrame(np.column_stack(
                fld_val_list),
                columns = fld_list,
                index = fld_val_list[globid_id])

# 2) ATTACHMENT TABLE
# replace attid with objectid from from feature class after matching global ids
globid_formatted_list, fname_photo, fp_photo = [], [], []
with da.SearchCursor(inTable, ['DATA', 'ATT_NAME', 'ATTACHMENTID', 'REL_GLOBALID']) as cursor:
    for row in cursor:
        # this is the data itself
        attachment = row[0]
        attid_substr = 'ATT{}'.format(str(row[2]))
        attname_substr = str(row[1]).replace(' ','')
        # GLOBID
        rel_globid = row[3]
        globid_formatted = rel_globid.replace('{','').replace('}','')
        # globid_formatted == globalid in df_fc (table)
        # Not perfect solution to when a point is deleted from extracted table
        # TURN OFF if problems with function.  May be masking other small issue
        # like using wrong attachment table ZU 20220826
        try:
            # If a rel_globalid was never utilized - i.e. deleted from fc
            matched_objid = df_fc.loc[globid_formatted, field_reference]
            deleted_pt = False
            # Terrible way to check if
            if not isinstance(matched_objid, str):
                matched_objid = '_AND_'.join(matched_objid.values.tolist())
            # If None Type then no id --> for instance if no value for
            # field_reference attribute in a row
            try:
                matched_objid_formatted = matched_objid.replace(' - ','_').replace('-','_').replace('.','').replace(' ','_').replace('__','_')
            except AttributeError:
                matched_objid_formatted = matched_objid
            objid_substr = '{}_{}'.format(field_reference, matched_objid_formatted)
            # Should create fname ex) Huntin_Blinds_OBJID20_ATT1_Photo1
            fname_att = '{}_{}_{}_{}'.format(feat_name, objid_substr, attid_substr, attname_substr)

            # Need feature class (fc_subdir) before trying feature (feat_dir)
            fc_subdir = os.path.join(basedir, feat_name)
            if not os.path.isdir(fc_subdir):
                os.mkdir(fc_subdir)
            # Now Make subdir Unless already created (i.e. multiple attachments in a feature)
            feat_subdir = os.path.join(fc_subdir, '{}_{}'.format(field_reference, matched_objid_formatted))
            # for some reason a filename had <filename>_ NOTICe the underscore.
            if feat_subdir[-1]=='_':
                feat_subdir = feat_subdir[:-1]
            if not os.path.isdir(feat_subdir):
                os.mkdir(feat_subdir)
            fp_att = os.path.join(feat_subdir, fname_att)
            open(fp_att, 'wb').write(attachment.tobytes())

            globid_formatted_list.append(globid_formatted)
            fname_photo.append(fname_att)
            fp_photo.append(fp_att)

        except KeyError:
            print('key error with: {}'.format(globid_formatted))
            pass

        del row
        del attachment

del cursor
# 3) PHOTO LOG CSV for Microsoft Publisher photo logs
df_right = pd.DataFrame(np.column_stack([globid_formatted_list, fname_photo, fp_photo]),
                        columns = [globalid_field_name, 'fname_photo', 'fp_photo'],
                        index = globid_formatted_list)
# one to many merge (many to one?)
df_merged = pd.merge(df_fc, df_right, on=globalid_field_name, how = 'outer')
fc_name = os.path.split(fc_in)[-1]
fp_csv_out = os.path.join(basedir, '{}_photo_log.csv'.format(fc_name))
pd.DataFrame.to_csv(df_merged, fp_csv_out)
