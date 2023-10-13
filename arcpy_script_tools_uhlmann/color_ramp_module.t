

class ToolBox(object):
    def __init__(self):
        '''
        Define the toolbox (name of the toolbox is name of .pyt file).
        '''
        self.label = "Color Ramp Toolbox"
        self.alias = "Color Ramp Toolbox"
        self.tools = [color_ramp_from_csv]
class color_ramp_from_csv(object):
    '''
    classifies color ramp from csv.  Note that user must classify color ramp simply with number \
    of classes initially prior to running
    '''

    def __init__(self):
        self.label = "format_color_ramp"
        self.description = "specify breaks, colors and labels for color ramps of rasters"
        self.canRunInBackground = False

        #https://community.esri.com/t5/arcgis-pro-questions/arcpy-parameter-for-arcgis-pro-document/td-p/1039453

    def getParameterInfo(self):
        '''
        Define parameter defitions
        '''

        param0 = arcpy.Parameter(
            displayName='Current Pro-Document',
            name='current_pro_doc',
            dataType='GPBoolean',
            parameterType='Optional',
            direction='Input')

        param1 = arcpy.Parameter(
            displayName='Other Pro-Document',
            name='other_pro_document',
            dataType='DEFile',
            parameterType='Optional',
            direction='Input')
        param1.filter.list=['aprx']
        param2 = arcpy.Parmameter(
            displayName='map',
            dataType='GPString',
            parameterType='Required',
            direction='Input')
        param3 = arcpy.Parmameter(
            displayName='layer',
            dataType='GPString',
            parameterType='Required',
            direction='Input')
        param4 = acrpy.Parameter(
            displayName='Formatting CSV',
            name='csv',
            dataType='DETextFile',
            parameterType='Required',
            direction='Input')
        parameters=[]
        parameters.append(param0,param1,param2,param3,param4)
        return params
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
        if parameters[1].altered and not parameters[1].hasBeenValidated:
            parameters[0].value=False
            parameters[2].value=None
            paramaters[2].filter.list=[]
            prodoc = paramaters[1].valueAsText
        elif parameters[0].value and paramaters[0].altered and not parameters[0].hasBeenValidated:
            parameters[1].value=None
            parameters[2].value=None
            parameters[2].filter.list=[]
            prodoc='current'
        else:
            prodoc = None
        if  prodoc is not None:
            self.project=arcpy.mp.ArcGISProject(prodoc)
            map_list = [m.name for m in self.project.listMaps()]
            parameters[2].filter.list=map_list
            parameters[3].value = None
            paramaters[3].filter.list = []
        if parameters[2].altered and not parameters[2].hasBeenValidated:
            map = parameters[2].valueAsText
            layer_list = self.project.listMaps(map)
            parameters[3].filter.list=layer_list
        return parameters

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # try:
        #     project_name = parameters[0]
        # except OSError:
        #     logging.info('{} does not exist.  Check spelling and/or file path \
        #                     (if providing full path)'.format(parameters[0].))
        project_name = self.prodoc
        layer_name = parameters[3]
        map_name = parameters[2]
        # csv = parameters[4]

        p = arcpy.mp.ArcGISProject(project_name)
        m = p.listMaps(map_name)[0]
        l = m.listLayers(layer_name)[0]
        arcpy.AddMessage('pro {} map {} layer {}'.format(p,m,l))

        return
