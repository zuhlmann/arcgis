import copy
import arcpy
import os

# AMAZING RESOURE
#https://gis.stackexchange.com/questions/339744/python-toolbox-only-update-parameter-when-specific-parameter-changes

class ToolBox(object):
    def __init__(self):
        '''
        Define the toolbox (name of the toolbox is name of .pyt file).
        '''
        self.label = "Arc Pro Mapping Utilities"
        self.alias = "mapping_utils"
        self.tools = [selection_to_sql]
class selection_to_sql(object):
    '''
    classifies color ramp from csv.  Note that user must classify color ramp simply with number \
    of classes initially prior to running
    '''

    def __init__(self):
        self.label = "Selection to SQL"
        self.description = "Creates an SQL Query and saves to text file (.exp)"
        self.canRunInBackground = False

        #https://community.esri.com/t5/arcgis-pro-questions/arcpy-parameter-for-arcgis-pro-document/td-p/1039453

    def getParameterInfo(self):
        '''
        Define parameter defitions
        '''
        param0 = arcpy.Parameter(
            displayName="Feature",
            name="feat",
            datatype="GPLayer",
            parameterType="Required",
            direction="Input")
        param1 = arcpy.Parameter(
            displayName="Field",
            name="field",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        # param1.filter.list = ['aprx']
        param2 = arcpy.Parameter(
            displayName="Condition",
            name="condition",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param3 = arcpy.Parameter(
            displayName="path/to/output/directory/ for formatted table",
            name="dir_out",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")
        param4 = arcpy.Parameter(
            displayName="File Name",
            name="file_name",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param5 = arcpy.Parameter(
            displayName="Overwrite SQL",
            name="overwrite_sql",
            datatype="GPBoolean",
            parameterType="Required",
            direction="Input")

        # param4.filter.list=['csv']
        parameters = [param0,param1,param2,param3,param4,param5]
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
        if not parameters[0].altered:
            parameters[1].filter.list=[]
            parameters[2].filter.list=[]
        if parameters[0].altered and not parameters[0].hasBeenValidated:
            parameters[1].value=None
            parameters[2].values=None
            flds = arcpy.da.Describe(parameters[0])
            flds = [f.name for f in flds['fields']]
            parameters[1].filter.list=flds
            parameters[2].filter.list=['Contains', 'Does NOT Contain']
        if parameters[3].altered and not parameters[3].hasBeenValidated:
            first_pass=False
            if os.path.exists(parameters[3].valueAsText):
                parameters[3].clearMessage()
                if parameters[4].altered and not parameters[4].hasBeenValidated:
                    file_ext = os.path.splitext(parameters[4].valueAsText)[-1]
                    if file_ext not in ['.txt','exp']:
                        msg = r'File type needs to be .exp or .txt'
                        parameters[4].setErrorMessage(msg)
                    else:
                        parameters[4].clearMessage()
                        first_pass = True
            else:
                parameters[3].setErrorMessage('{} Does Not Exist'.format('TSHOOT'))
            if first_pass:
                fp_out = os.path.join(parameters[3].valueAsText, parameters[4].valueAsText)
                if os.path.exists(fp_out):
                    if parameters[5].altered and not parameters[5].hasBeenValidated:
                        if parameters[5].value == True:
                            parameters[4].clearMessage()
                            parameters[5].clearMessage()
                            parameters[5].setWarningMessage('Existing file will be overwritten')
                        else:
                            msg = r'{} Exists.  Set {} to True or change file path to continue'.format(fp_out, 'TSHOOT')
                            parameters[4].setErrorMessage(msg)
                            parameters[5].setErrorMessage(msg)
                # else:
                #     parameters[5].value = False

        return parameters

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return
    def execute(self, parameters, messages):
        """The source code of the tool."""

        cond_dict = {'Contains':'IN','Does NOT Contain':'NOT IN'}
        type_dict = {'String':'String','OID':'number','Double':'number'}
        feat = parameters[0].valueAsText
        fld = parameters[1].valueAsText
        cond = parameters[2].valueAsText
        print(cond)
        arcpy.AddMessage('Val: {} Type{}'.format(cond, type(cond)))
        cond_keyed = cond_dict[cond]
        describe_obj = arcpy.da.Describe(feat)
        for f in describe_obj['fields']:
            if f.name==fld:
                fld_type = f.type

        vals = []
        fld_list = [fld]
        with arcpy.da.SearchCursor(feat, fld_list) as cursor:
            for row in cursor:
                vals.append(row[0])
            del cursor

        if type_dict[fld_type]=='String':
            vals = list(set(vals))
            # empty rows
            vals_remove = ['',' ']
            for v in vals_remove:
                try:
                    vals.remove(v)
                except ValueError:
                    pass
            vals = "','".join(str(v) for v in vals)
            vals = "'{}'".format(vals)
        elif type_dict[fld_type]=='number':
            vals = ','.join(str(v) for v in vals)

        fp_out = os.path.join(parameters[3].valueAsText, parameters[4].valueAsText)
        str_formatted = r'{} {} ({})'.format(fld, cond_keyed, vals)

        # fp_out = r'C:\Box\MCM Projects\Magic Dam Wood Hydro - Part 12 and other work' + \
        #          r'\24-009 Magic Dam Inundation Mapping\6.0 Plans and Specs\6.6_GIS\GIS_files\gis_inventories\test_roads.exp'
        with open(fp_out, 'w') as out_file:
            out_file.write(str_formatted)
        return


