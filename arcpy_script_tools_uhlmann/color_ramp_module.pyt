import pandas as pd

class Toolbox(object):
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
        param0 = arcpy.Parameter(displayName="Current Pro-Document",
                                 name="currentProDocument",
                                 datatype="GPBoolean",
                                 parameterType="Optional",
                                 direction="Input")

        param1 = arcpy.Parameter(displayName="Other Pro-Document",
                                 name="otherProDocument",
                                 datatype="DEFile",
                                 parameterType="Optional",
                                 direction="Input")
        param1.filter.list = ['aprx']
        param2 = arcpy.Parameter(
            displayName="map",
            name="map",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param3 = arcpy.Parameter(
            displayName="layer",
            name="layer",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param4 = arcpy.Parameter(
            displayName="Formatting CSV",
            name="csv",
            datatype="DETextFile",
            parameterType="Required",
            direction="Input")
        param4.filter.list=['csv']
        parameters = [param0,param1,param2,param3,param4]
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
        if parameters[1].altered and not parameters[1].hasBeenValidated:
            parameters[0].value=False
            parameters[2].value=None
            parameters[2].filter.list=[]
            prodoc = parameters[1].valueAsText
            prodoc_selected = True
        elif parameters[0].altered and not parameters[0].hasBeenValidated:
            parameters[1].value=None
            parameters[2].value=None
            parameters[2].filter.list=[]
            prodoc='current'
            prodoc_selected=True
        else:
            prodoc_selected  = False
        if prodoc_selected:
            project=arcpy.mp.ArcGISProject(prodoc)
            map_list = [m.name for m in project.listMaps()]
            parameters[2].value=None
            parameters[2].filter.list=map_list
            parameters[3].value = None
            parameters[3].filter.list = []
        if parameters[2].altered and not parameters[2].hasBeenValidated:
            if parameters[0].value is not None:
                prodoc = 'current'
            elif parameters[1].value is not None:
                prodoc = parameters[1].valueAsText
            project = arcpy.mp.ArcGISProject(prodoc)
            map_name = parameters[2].valueAsText
            map_object = project.listMaps(map_name)[0]
            layer_list = [l.name for l in map_object.listLayers()]
            parameters[3].filter.list=layer_list
        if 'prodoc' in locals():
            return parameters, prodoc
        else:
            return parameters

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return
    def execute(self, parameters, messages):
        """The source code of the tool."""
        if parameters[0].value is not None:
            prodoc = 'current'
        elif parameters[1].value is not None:
            prodoc = parameters[1].valueAsText
        project_name=prodoc
        layer_name = parameters[3].valueAsText
        map_name = parameters[2].valueAsText
        csv = parameters[4].valueAsText

        p = arcpy.mp.ArcGISProject(project_name)
        m = p.listMaps(map_name)[0]
        l = m.listLayers(layer_name)[0]
        cim_lyr = l.getDefinition('V3')
        arcpy.AddMessage('pro {} map {} layer {}'.format(p,m,l))

        # csv = r'C:\Users\UhlmannZachary\Box\MCMGIS\Project_Based\Eklutna\Maps\dam_break\symbology_bounds_eklutna_dam_break_debug.csv'
        df = pd.read_csv(csv)

        if len(cim_lyr.colorizer.classBreaks) != len(df):
            print('check number of class breaks matches csv')
        for idx, cn in enumerate(cim_lyr.colorizer.classBreaks):
            rgba = [df.loc[idx, 'red'], df.loc[idx, 'green'], df.loc[idx, 'blue'], df.loc[idx, 'alpha']]
            rgba = [float(v) for v in rgba]
            cn.color.values = rgba
            print(cn.color.values)
            lower = df.loc[idx, 'lower_bound']
            upper = df.loc[idx, 'upper_bound']
            cn.upperBound = int(upper)
            cn.label = '{} to {} ft'.format(lower, upper)
        #     print('UPPER BOUND: ', upper)

        l.setDefinition(cim_lyr)
        cn.color.values

        return
