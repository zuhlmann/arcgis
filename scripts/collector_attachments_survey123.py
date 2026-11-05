import arcpy
import os
import pandas as pd
import numpy as np
import copy

table_in_child = r'D:\projects\snettisham\add_box\AGOL\gdb\Snettisham_Veg_Plots_2026_EDIT_v1_20261008\Snettisham_Veg_Plots_2026_EDIT_v1_20261008.gdb\Plots'
attach_table_child = r'D:\projects\snettisham\add_box\AGOL\gdb\Snettisham_Veg_Plots_2026_EDIT_v1_20261008\Snettisham_Veg_Plots_2026_EDIT_v1_20261008.gdb\Plots__ATTACH'
rel_globalid_child = 'GlobalID'
# desc_field_child = 'PointNbr'
dir_out = r"D:\projects\snettisham\add_box\AGOL\extracted\Snettisham_Veg_Plots_2026"
desc_field = 'SiteID'

idx = 'SpeciesInventory_TABLE'
csv_master = r"D:\projects\snettisham\add_box\AGOL\snett_gdb_attachment_files.xlsx"
df_master = pd.read_excel(csv_master, index_col = 'FEATURE')
table_in_child = df_master.loc[idx, 'TABLE']
attach_table_child = df_master.loc[idx, 'ATTACH_TABLE']
rel_globalid_parent = df_master.loc[idx, 'FEATURE_KEY']
dir_out = df_master.loc[idx, 'DIR_OUT']
desc_field = df_master.loc[idx, 'DESC_FIELD_FEATURE']
branch_field = df_master.loc[idx, 'BRANCH_FIELD']
dir_design = df_master.loc[idx, 'DIR_DESIGN']
use_all_fields = True
prepend_fname = False

describe_obj = arcpy.da.Describe(table_in_child)
all_fields = [f.name for f in describe_obj['fields'] if 'shape' not in f.name.lower()]

feat_name = os.path.split(table_in_child)[-1]
base_fields = [desc_field, 'globalid', 'notes']
base_fields = [desc_field, branch_field, 'globalid', 'notes']
if use_all_fields:
    fld_list = all_fields
else:
    fld_list = base_fields
# 1) FEATURE CLASS TABLE
# initiate list of list with empty values to add vale
fld_val_list = [[] for i in range(len(fld_list))]
# indices to match list
fld_id_list = list(range(len(fld_val_list)))
with arcpy.da.SearchCursor(table_in_child, fld_list) as cursor:
    for row in cursor:
        for id in fld_id_list:
            # Formatt relative id (remove spaces, characters, etc.)
            if fld_list[id] == rel_globalid_parent:
                # get exact globid name for below
                globalid_field_name = fld_list[id]
                temp = row[id]
                temp = temp.replace('{', '').replace('}', '')
                globid_id = copy.copy(id)
            else:
                temp = row[id]
            fld_val_list[id].append(temp)

# Dataframe with all rows from feat with globid as index
df_fc = pd.DataFrame(np.column_stack(
    fld_val_list),
    columns=fld_list,
    index=fld_val_list[globid_id])

# 2) ATTACHMENT TABLE
# replace attid with objectid from from feature class after matching global ids
globid_formatted_list, fname_photo, fp_photo = [], [], []
with arcpy.da.SearchCursor(attach_table_child, ['DATA', 'ATT_NAME', 'ATTACHMENTID', 'REL_GLOBALID']) as cursor:
    for row in cursor:
        # this is the data itself
        attachment = row[0]
        attid_substr = 'ATT{}'.format(str(row[2]))
        attname_substr = str(row[1]).replace(' ', '').replace('-','_')
        # GLOBID
        rel_globid = row[3]
        globid_formatted = rel_globid.replace('{', '').replace('}', '')
        # globid_formatted == globalid in df_fc (table)
        # Not perfect solution to when a point is deleted from extracted table
        # TURN OFF if problems with function.  May be masking other small issue
        # like using wrong attachment table ZU 20220826
        try:
            # If a rel_globalid was never utilized - i.e. deleted from fc
            matched_objid = df_fc.loc[globid_formatted, desc_field]
            # Terrible way to check if
            if isinstance(matched_objid, list):
                matched_objid = '_AND_'.join(matched_objid.values.tolist())
            # If None Type then no id --> for instance if no value for
            # field_reference attribute in a row
            try:
                matched_objid_formatted = matched_objid.replace(' - ', '_').replace('-', '_').replace('.',
                                                                                                      '').replace(
                    ' ', '_').replace('__', '_')
            except AttributeError:
                matched_objid_formatted = matched_objid
            objid_substr = '{}_{}'.format(desc_field, matched_objid_formatted)
            fname_att = row[1].replace(' ','').replace('-','_')
            # Need feature class (fc_subdir) before trying feature (feat_dir)
            fc_subdir = os.path.join(dir_out, feat_name)
            if not os.path.isdir(fc_subdir):
                os.mkdir(fc_subdir)
            # Now Make subdir Unless already created (i.e. multiple attachments in a feature)
            if dir_design == "Branched":
                # If match or branch val is objectid or non-string
                try:
                    matched_val = df_fc.loc[globid_formatted, branch_field]
                    matched_val_fmt = matched_val.replace('-','_')
                except AttributeError:
                    matched_val_fmt = copy.copy(matched_val)
                try:
                    branch_field_fmt =branch_field.replace('-', '_')
                except AttributeError:
                    branch_field_fmt = copy.copy(branch_field)
                if prepend_fname:
                    attach_dir = os.path.join(fc_subdir, '{}_{}'.format(branch_field_fmt, matched_val_fmt))
                else:
                    attach_dir = os.path.join(fc_subdir, '{}'.format(matched_val_fmt))
            elif dir_design == "Single":
                attach_dir = copy.copy(fc_subdir)
            # for some reason a filename had <filename>_ NOTICe the underscore.
            if attach_dir[-1] == '_':
                attach_dir = attach_dir[:-1]
            if not os.path.isdir(attach_dir):
                os.mkdir(attach_dir)
            fp_att = os.path.join(attach_dir, fname_att)
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
                        columns=[globalid_field_name, 'fname_photo', 'fp_photo'],
                        index=globid_formatted_list)
# one to many merge (many to one?)
df_merged = pd.merge(df_fc, df_right, on=globalid_field_name, how='outer')
fc_name = os.path.split(table_in_child)[-1]
fp_csv_out = os.path.join(dir_out, '{}_photo_log.csv'.format(fc_name))
pd.DataFrame.to_csv(df_merged, fp_csv_out)
