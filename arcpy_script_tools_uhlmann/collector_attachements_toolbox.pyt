import arcpy
# AMAZING RESOURE
#https://gis.stackexchange.com/questions/339744/python-toolbox-only-update-parameter-when-specific-parameter-changes
import pandas as pd
import numpy as np
import os
import copy
import ntpath

class Toolbox(object):
    def __init__(self):
        '''
        Define the toolbox (name of the toolbox is name of .pyt file).
        '''
        self.label = "Field Maps Utilities"
        self.alias = "Field Maps Utilities"
        self.tools = [Parse_Attachments]
class Parse_Attachments(object):
    '''
    classifies color ramp from csv.  Note that user must classify color ramp simply with number \
    of classes initially prior to running
    '''

    def __init__(self):
        self.label = "Unpack Field Map Attachments"
        self.description = "Unpack Field Map (and Collector) attachments into folder(s) with inventory csv"
        self.canRunInBackground = False

        #https://community.esri.com/t5/arcgis-pro-questions/arcpy-parameter-for-arcgis-pro-document/td-p/1039453

    def getParameterInfo(self):
        '''
        Define parameter defitions
        '''

        param0 = arcpy.Parameter(
            displayName="Feature IN",
            name="fc_in",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")
        param1 = arcpy.Parameter(
            displayName="Attachment Table",
            name="attach_table",
            datatype="DETable",
            parameterType="Required",
            direction="Input")
        param2 = arcpy.Parameter(
            displayName="Relational DBase GlobalID",
            name="rel_globalid",
            datatype="Field",
            parameterType="Required",
            direction="Input")
        param2.parameterDependencies = [param0.name]
        param3 = arcpy.Parameter(
            displayName="path/to/base/output/directory/ to save attachments",
            name="dir_out",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")
        param4 = arcpy.Parameter(
            displayName="Descriptive Field",
            name="desc_field",
            datatype="Field",
            parameterType="Field",
            direction="Input")
        param4.parameterDependencies = [param0.name]
        param5 = arcpy.Parameter(
            displayName="Use All Fields",
            name="use_all_flds",
            datatype="GPBoolean",
            parameterType="Required",
            direction="Input")
        param6 = arcpy.Parameter(
            displayName="Directory Design",
            name="dir_design",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param6.filter.type="ValueList"
        param6.filter.list=['Branched','Single']
        param6.value = 'Branched'
        parameters = [param0,param1,param2,param3,param4,param5,param6]
        return parameters
    def isLicensed(self):
        '''
        set whether tool is licensed to execute.
        '''
        return True
    def updateParameters(self, parameters):
        '''
        Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed.
        '''
        fc_in = parameters[0]
        attach_table = parameters[1]
        rel_globalid = parameters[2]
        dir_out = parameters[3]
        desc_field = parameters[4]
        use_all_fields=parameters[5]
        dir_design=parameters[6]
        if fc_in.altered and not fc_in.hasBeenValidated:
            parameters[2].Value = None
            parameters[4].Value = None
            parameters[2].parameterDependencies = [parameters[0].name]
            parameters[4].parameterDependencies = [parameters[0].name]
            parameters[1].Value = None

        return parameters


    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return
    def execute(self, parameters, messages):
        """The source code of the tool."""
        fc_in = parameters[0].valueAsText
        attach_table = parameters[1].valueAsText
        rel_globalid = parameters[2].valueAsText
        dir_out = parameters[3].valueAsText
        desc_field = parameters[4].valueAstext
        use_all_fields=parameters[5]
        dir_design=parameters[6].valueAsText

        describe_obj = arcpy.da.Describe(fc_in)
        all_fields = [f.name for f in describe_obj['fields'] if 'shape' not in f.name.lower()]

        feat_name = os.path.split(fc_in)[-1]
        base_fields = [desc_field, 'GLOBALID', 'notes']
        if use_all_fields.value:
            fld_list = all_fields
        else:
            fld_list = base_fields
        # 1) FEATURE CLASS TABLE
        # initiate list of list to add vale
        fld_val_list = [[] for i in range(len(fld_list))]
        # indices to match list
        fld_id_list = list(range(len(fld_val_list)))
        with arcpy.da.SearchCursor(fc_in, fld_list) as cursor:
            for row in cursor:
                for id in fld_id_list:
                    if fld_list[id] == rel_globalid:
                        # get exact globid name for below
                        globalid_field_name = fld_list[id]
                        temp = row[id]
                        temp = temp.replace('{', '').replace('}', '')
                        globid_id = copy.copy(id)
                    else:
                        temp = row[id]
                    fld_val_list[id].append(temp)

        df_fc = pd.DataFrame(np.column_stack(
            fld_val_list),
            columns=fld_list,
            index=fld_val_list[globid_id])

        # 2) ATTACHMENT TABLE
        # replace attid with objectid from from feature class after matching global ids
        globid_formatted_list, fname_photo, fp_photo = [], [], []
        with arcpy.da.SearchCursor(attach_table, ['DATA', 'ATT_NAME', 'ATTACHMENTID', 'REL_GLOBALID']) as cursor:
            for row in cursor:
                # this is the data itself
                attachment = row[0]
                attid_substr = 'ATT{}'.format(str(row[2]))
                attname_substr = str(row[1]).replace(' ', '')
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
                    deleted_pt = False
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
                    # Should create fname ex) Huntin_Blinds_OBJID20_ATT1_Photo1
                    fname_att = '{}_{}_{}_{}'.format(feat_name, objid_substr, attid_substr, attname_substr)

                    # Need feature class (fc_subdir) before trying feature (feat_dir)
                    fc_subdir = os.path.join(dir_out, feat_name)
                    if not os.path.isdir(fc_subdir):
                        os.mkdir(fc_subdir)
                    # Now Make subdir Unless already created (i.e. multiple attachments in a feature)
                    if dir_design=="Branched":
                        attach_dir = os.path.join(fc_subdir, '{}_{}'.format(desc_field, matched_objid_formatted))
                    elif dir_design=="Single":
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
        fc_name = os.path.split(fc_in)[-1]
        fp_csv_out = os.path.join(dir_out, '{}_photo_log.csv'.format(fc_name))
        pd.DataFrame.to_csv(df_merged, fp_csv_out)

        return

