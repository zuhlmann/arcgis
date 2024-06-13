import copy
import arcpy
import os

# AMAZING RESOURE
#https://gis.stackexchange.com/questions/339744/python-toolbox-only-update-parameter-when-specific-parameter-changes
import pandas as pd
import numpy as np
import os
import copy

class ToolBox(object):
    def __init__(self):
        '''
        Define the toolbox (name of the toolbox is name of .pyt file).
        '''
        self.label = "Arc Pro PROJECT Utilities"
        self.alias = "pro_project_utils"
        self.tools = [project_lyT_inv, project_lyR_inv]
class project_lyT_inv(object):
    '''
    classifies color ramp from csv.  Note that user must classify color ramp simply with number \
    of classes initially prior to running
    '''

    def __init__(self):
        self.label = "Inventory Pro Project Layouts"
        self.description = "Exports csv itemizing all maps used in all layouts"
        self.canRunInBackground = False

        #https://community.esri.com/t5/arcgis-pro-questions/arcpy-parameter-for-arcgis-pro-document/td-p/1039453

    def getParameterInfo(self):
        '''
        Define parameter defitions
        '''
        param0 = arcpy.Parameter(
            displayName="Current Pro-Document",
            name="currentProDocument",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input")

        param1 = arcpy.Parameter(
            displayName="Other Pro-Document",
            name="otherProDocument",
            datatype="DEFile",
            parameterType="Optional",
            direction="Input")
        param1.filter.list = ["aprx"]
        param2 = arcpy.Parameter(
            displayName="path/to/output/directory/ for formatted table",
            name="dir_out",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")
        param3 = arcpy.Parameter(
            displayName="File Name",
            name="file_name",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        parameters = [param0,param1,param2,param3]
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
            prodoc_selected = True
            parameters[2].values = None
            parameters[3].values = None
        elif parameters[0].altered and not parameters[0].hasBeenValidated:
            parameters[1].value=None
            prodoc_selected=True
            parameters[2].values = None
            parameters[3].values = None
        else:
            prodoc_selected  = False
        if prodoc_selected:
            parameters[2].values = None
            parameters[3].values = None
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

        aprx = arcpy.mp.ArcGISProject(prodoc)
        lyt_list = aprx.listLayouts()
        lyt_name = []
        el_map_formatted = []
        for lyt in lyt_list:
            el = lyt.listElements()
            el_map = [e.map.name for e in el if e.type == 'MAPFRAME_ELEMENT']
            el_map_formatted = el_map_formatted + el_map
            lyt_name = lyt_name + ([lyt.name] * len(el_map))

        df = pd.DataFrame(np.column_stack([lyt_name, el_map_formatted]), columns=['LAYOUT', 'SOURCE_MAP'])
        if os.path.splitext(parameters[3].valueAsText)[-1]=='.csv':
            fname = copy.copy(parameters[3].valueAsText)
        else:
            fname = r'{}.csv'.format(os.path.splitext(parameters[3].valueAsText)[0])
        csv = os.path.join(parameters[2].valueAsText,fname)
        df.to_csv(csv)

        return
class project_lyR_inv(object):
    '''
    To identify layers from map elements in all layouts.  Outputs layer name, layout name, data source.
    # ZU 20240523
    '''

    def __init__(self):
        self.label = "Layer Inventory for Map Elements"
        self.description = "Inventory Pro Project Layers visible in Map Elements in Layouts"
        self.canRunInBackground = False

        #https://community.esri.com/t5/arcgis-pro-questions/arcpy-parameter-for-arcgis-pro-document/td-p/1039453

    def getParameterInfo(self):
        '''
        Define parameter defitions
        '''
        param0 = arcpy.Parameter(
            displayName="Current Pro-Document",
            name="currentProDocument",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input")

        param1 = arcpy.Parameter(
            displayName="Other Pro-Document",
            name="otherProDocument",
            datatype="DEFile",
            parameterType="Optional",
            direction="Input")
        param1.filter.list = ["aprx"]
        param2 = arcpy.Parameter(
            displayName="path/to/output/directory/ for formatted table",
            name="dir_out",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")
        param3 = arcpy.Parameter(
            displayName="File Name",
            name="file_name",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        parameters = [param0,param1,param2,param3]
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
            prodoc_selected = True
            parameters[2].values = None
            parameters[3].values = None
        elif parameters[0].altered and not parameters[0].hasBeenValidated:
            parameters[1].value=None
            prodoc_selected=True
            parameters[2].values = None
            parameters[3].values = None
        else:
            prodoc_selected  = False
        if prodoc_selected:
            parameters[2].values = None
            parameters[3].values = None
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

        aprx = arcpy.mp.ArcGISProject(prodoc)
        lyt_list = aprx.listLayouts()

        lyt_name, ds_list, lyr_name, map_element = [], [], [], []
        for lyt in lyt_list:
            el = lyt.listElements()
            el_map = [e.map for e in el if e.type == 'MAPFRAME_ELEMENT']
            for em in el:
                if em.type == 'MAPFRAME_ELEMENT':
                    for lyr in em.map.listLayers():
                        if lyr.visible:
                            lyr_name.append(lyr.name)
                            lyt_name.append(lyt.name)
                            map_element.append(em.name)
                            try:
                                ds_list.append(lyr.dataSource)
                            except AttributeError:
                                ds_list.append('NA')
                        else:
                            pass

        df = pd.DataFrame(np.column_stack([lyt_name, map_element,lyr_name, ds_list]),
                          columns = ['layout','map_element','layer','source'])

        if os.path.splitext(parameters[3].valueAsText)[-1]=='.csv':
            fname = copy.copy(parameters[3].valueAsText)
        else:
            fname = r'{}.csv'.format(os.path.splitext(parameters[3].valueAsText)[0])
        csv = os.path.join(parameters[2].valueAsText,fname)
        df.to_csv(csv)

        return


