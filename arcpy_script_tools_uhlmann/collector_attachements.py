import arcpy
from arcpy import da
import os
import pandas as pd
import numpy as np

# Directly from here:
# https://support.esri.com/en/technical-article/000011912
# Adapted majorly to link objectids betw attach table and fc

fc_in = arcpy.GetParameterAsText(0)
inTable = arcpy.GetParameterAsText(1)
basedir = arcpy.GetParameterAsText(2)
field_reference = arcpy.GetParameterAsText(3)

# check for shp - DON'T THINK this matters because feature class is specified as fc_in data type
if fc_in[-3:] == 'shp':
    feat_name = os.path.split(fc_in)[-1][:-4]
else:
    feat_name = os.path.split(fc_in)[-1]

# field_reference = 'OBJECTID'

objid_fc, globid_fc = [],[]
with da.SearchCursor(fc_in, [field_reference, 'GLOBALID']) as cursor:
    for row in cursor:
        objid_fc.append(row[0])
        temp_globid = row[1]
        globid_formatted = temp_globid.replace('{','').replace('}','')
        globid_fc.append(globid_formatted)

df_fc = pd.DataFrame(np.column_stack(
                [globid_fc, objid_fc]),
                columns = ['globalid', field_reference],
                index = globid_fc)


# replace attid with objectid from from feature class after matching global ids
with da.SearchCursor(inTable, ['DATA', 'ATT_NAME', 'ATTACHMENTID', 'REL_GLOBALID']) as cursor:
    for row in cursor:
        # this is the data itself
        attachment = row[0]
        attid_substr = 'ATT{}'.format(str(row[2]))
        attname_substr = str(row[1]).replace(' ','')
        # GLOBID
        temp_globid = row[3]
        globid_formatted = temp_globid.replace('{','').replace('}','')
        matched_objid = df_fc.loc[globid_formatted, field_reference]
        objid_substr = '{}_{}'.format(field_reference, matched_objid)
        # Should create fname ex) Huntin_Blinds_OBJID20_ATT1_Photo1
        fname_att = '{}_{}_{}_{}'.format(feat_name, objid_substr, attid_substr, attname_substr)

        # Need feature class (fc_subdir) before trying feature (feat_dir)
        fc_subdir = os.path.join(basedir, feat_name)
        if not os.path.isdir(fc_subdir):
            os.mkdir(fc_subdir)
        # Now Make subdir Unless already created (i.e. multiple attachments in a feature)
        feat_subdir = os.path.join(fc_subdir, '{}_{}'.format(field_reference, matched_objid))
        if not os.path.isdir(feat_subdir):
            os.mkdir(feat_subdir)
        fname_att = os.path.join(feat_subdir, fname_att)
        open(fname_att, 'wb').write(attachment.tobytes())
        del row
        del attachment
