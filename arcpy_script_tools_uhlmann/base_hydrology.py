import os

class Toolbox(object):
    def __init__(self):
        '''
        Define the toolbox (name of the toolbox is name of .pyt file).
        '''
        self.label = "Base Hydrology Toolset"
        self.alias = "Base Hydrology Toolset"
        self.tools = [format_NHD_flowline]

class format_NHD_flowline(object):
    '''
    classifies color ramp from csv.  Note that user must classify color ramp simply with number \
    of classes initially prior to running
    '''

    def __init__(self):
        self.label = "Format NHD Flowline"
        self.description = "Streamlines NHD flowline feature class by first dissolving by ReachCode," \
                           "then dissolving by GNIS_name (if not NULL)"
        self.canRunInBackground = False

        #https://community.esri.com/t5/arcgis-pro-questions/arcpy-parameter-for-arcgis-pro-document/td-p/1039453

    def getParameterInfo(self):
        '''
        Define parameter defitions
        '''
        param0 = arcpy.Parameter(
            displayName="Feature",
            name="feat",
            datatype=["GPLayer","DEFeatureClass"],
            parameterType="Required",
            direction="Input")

        param1 = arcpy.Parameter(
            displayName="path/to/output/directory or gdb",
            name="dir_out",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")
        param2 = arcpy.Parameter(
            displayName="File Name",
            name="file_name",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param3 = arcpy.Parameter(
            displayName="Overwrite Output File",
            name="overwrite_output",
            datatype="GPBoolean",
            parameterType="Required",
            direction="Input")

        parameters = [param0, param1, param2, param3]
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
        if parameters[0].altered and not parameters[0].hasBeenValidated:
            parameters[1].value = None
            parameters[2].value = None
        if parameters[1].altered and not parameters[1].hasBeenValidated:
            parameters[2].value = None
            parameters[3].value = False
        if parameters[2].altered and not parameters[2].hasBeenValidated:
            fp_out = os.path.join(parameters[1].valueAsText, parameters[2].valueAsText)
            if os.path.exists(fp_out):
                if parameters[3].altered and not parameters[3].hasBeenValidated:
                    if parameters[3].value == True:
                        parameters[3].clearMessage()
                        parameters[3].setWarningMessage('Existing file will be overwritten')
                    elif parameters[3].value == False:
                        msg = r'{} Exists.  Set {} to True or change file path to continue'.format(fp_out, 'TSHOOT')
                        parameters[3].setErrorMessage(msg)
            else:
                parameters[3].value = False

        return parameters

    def execute(self, parameters, messages):
        """The source code of the tool."""

        feat_in = parameters[0].valueAsText
        DE_workspace = parameters[1].valueAsText
        fname_out = parameters[2].valueAsText

       # 1) Dissolve
        dissolve1 = 'memory\dissolve1'
        dissolve_fld = ['ReachCode']
        stat_fld = [['GNIS_Name', 'FIRST']]
        arcpy.Dissolve_management(feat_in, dissolve1, dissolve_fld, statistics_fields=stat_fld)

        # 2a) split by SQL
        sql1 = "FIRST_gnis_name IS NOT NULL"
        sql2 = "FIRST_gnis_name IS NULL"
        arcpy.FeatureClassToFeatureClass_conversion(dissolve1, 'memory','named', where_clause=sql1)
        arcpy.FeatureClassToFeatureClass_conversion(dissolve1, 'memory','unnamed', where_clause=sql2)

        # # 2b) dissolve names
        arcpy.Dissolve_management(r'memory\named', 'memory\dissolved','FIRST_gnis_name', "", "", "")
        # 2c) Merge
        fp_out = os.path.join(DE_workspace,fname_out)
        arcpy.Merge_management([r'memory\dissolved', r'memory\unnamed'], fp_out)

        return
