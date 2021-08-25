import arcpy
from arcpy import da
import os
import pandas as pd
import numpy as np

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

fc_in = arcpy.GetParameterAsText(0)
inTable = arcpy.GetParameterAsText(1)
basedir = arcpy.GetParameterAsText(2)
field_reference = arcpy.GetParameterAsText(3)

# check for shp - DON'T THINK this matters because feature class is specified as fc_in data type
if fc_in[-3:] == 'shp':
    feat_name = os.path.split(fc_in)[-1][:-4]
else:
    feat_name = os.path.split(fc_in)[-1]

# 1) FEATURE CLASS TABLE
objid_fc, globid_fc, notes = [],[],[]
with da.SearchCursor(fc_in, [field_reference, 'GLOBALID', 'notes']) as cursor:
    for row in cursor:
        objid_fc.append(row[0])
        temp_globid = row[1]
        notes.append(row[2])
        globid_formatted = temp_globid.replace('{','').replace('}','')
        globid_fc.append(globid_formatted)

df_fc = pd.DataFrame(np.column_stack(
                [globid_fc, objid_fc, notes]),
                columns = ['globalid', field_reference, 'notes'],
                index = globid_fc)

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
        temp_globid = row[3]
        globid_formatted = temp_globid.replace('{','').replace('}','')
        # globid_formatted == globalid in df_fc (table)
        matched_objid = df_fc.loc[globid_formatted, field_reference]
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

        # Populate DF for Microsoft Publisher Report Mailings table
        globid_formatted_list.append(globid_formatted)
        fname_photo.append(fname_att)
        fp_photo.append(fp_att)

        del row
        del attachment

# 3) PHOTO LOG CSV for Microsoft Publisher photo logs
df_right = pd.DataFrame(np.column_stack([globid_formatted_list, fname_photo, fp_photo]),
                        columns = ['globalid', 'fname_photo', 'fp_photo'],
                        index = globid_formatted_list)
# one to many merge (many to one?)
df_merged = pd.merge(df_fc, df_right, on='globalid', how = 'outer')
fc_name = os.path.split(fc_in)[-1]
fp_csv_out = os.path.join(basedir, '{}_photo_log.csv'.format(fc_name))
pd.DataFrame.to_csv(df_merged, fp_csv_out)
