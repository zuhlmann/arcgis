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
        self.label = "Create and update map series / data driven pages indices"
        self.alias = "map_series_index"
        self.tools = [create_series_from_centroid, update_map_series]

class create_series_from_centroid(object):
    '''
    classifies color ramp from csv.  Note that user must classify color ramp simply with number \
    of classes initially prior to running
    '''

    def __init__(self):
        self.label = "Create Map Series from Centroid"
        self.description = "Creates a Map Seris from formatted Centroid"
        self.canRunInBackground = False

        #https://community.esri.com/t5/arcgis-pro-questions/arcpy-parameter-for-arcgis-pro-document/td-p/1039453

    def getParameterInfo(self):
        '''
        Define parameter defitions
        '''
        param0 = arcpy.Parameter(
            displayName="Centroid Feature",
            name="Centroid Feature",
            datatype="GPLayer",
            parameterType="Required",
            direction="Input")
        param1 = arcpy.Parameter(
            displayName="Map Series Feature",
            name="map_series_feature",
            datatype="GPLayer",
            parameterType="Required",
            direction="Input")
        param2 = arcpy.Parameter(
            displayName="Scale Type",
            name="Scale Type",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param2.filter.list=['Relative','Ratio_FtToIich']
        parameters = [param0,param1,param2]
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

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return
    def execute(self, parameters, messages):
        """The source code of the tool."""

        def get_scale_factor(is_relative, scale_factor, layout_width, layout_ht):
            dx_relative = (scale_factor * layout_width * (1 / 12)) * 0.5
            dy_relative = (scale_factor * layout_ht * (1 / 12)) * 0.5
            dx_in2feet = (scale_factor * layout_width) * 0.5
            dy_in2feet = (scale_factor * layout_ht) * 0.5
            if is_relative:
                dx = dx_relative
                dy = dy_relative
            else:
                dx = dx_in2feet
                dy = dy_in2feet
            return (dx, dy)

        feat_centroid = parameters[0].valueAsText
        feat_index = parameters[1].valueAsText
        scale_factor_type = parameters[2].valueAsText
        sd = {'Relative':True,'Ratio_FtToIich':False}

        relative=sd[scale_factor_type]
        bad_vals = ['shape', 'objectid', 'fid']
        fields_base = [f for f in arcpy.ListFields(feat_centroid) if not any(v in f.name.lower() for v in bad_vals)]
        field_names_base = [f.name for f in fields_base]
        fields_cursor = ['SHAPE@XY']
        fields_cursor.extend(field_names_base)
        fields_index = ['SHAPE@']
        fields_index.extend(field_names_base)
        calc_fields_order = ['LAYOUT_HT','LAYOUT_WIDTH','SCALE_FACTOR']

        # Add fields to new feature class if not existing
        field_names_index = [f.name for f in arcpy.ListFields(feat_index)]
        for f in fields_base:
            if f.name not in field_names_index:
                arcpy.AddField_management(feat_index, f.name, f.type)

        with arcpy.da.SearchCursor(feat_centroid, fields_cursor) as cursor_centroid:
            with arcpy.da.InsertCursor(feat_index, fields_index) as cursor_index:
                d = {val:idx for idx, val in enumerate(fields_cursor) if val in calc_fields_order}
                for row in cursor_centroid:
                    layout_ht=row[d['LAYOUT_HT']]
                    layout_width=row[d['LAYOUT_WIDTH']]
                    scale_factor = row[d['SCALE_FACTOR']]
                    dx, dy = get_scale_factor(relative, scale_factor, layout_width, layout_ht)
                    x,y = row[0]
                    xmin = x - dx
                    xmax = x + dx
                    ymin = y - dy
                    ymax = y + dy
                    array = arcpy.Array([arcpy.Point(xmin, ymin),
                                         arcpy.Point(xmax, ymin),
                                         arcpy.Point(xmax, ymax),
                                         arcpy.Point(xmin, ymax)
                                         ])
                    polygon = arcpy.Polygon(array)
                    row_index = [polygon]
                    row_index.extend(row[1:])
                    cursor_index.insertRow(row_index)
        del cursor_centroid
        del cursor_index

class update_map_series(object):
    '''
    classifies color ramp from csv.  Note that user must classify color ramp simply with number \
    of classes initially prior to running
    '''

    def __init__(self):
        self.label = "Update Map Series Geometry"
        self.description = "Update existing map seris from SCALE_FACTOR field"
        self.canRunInBackground = False

        #https://community.esri.com/t5/arcgis-pro-questions/arcpy-parameter-for-arcgis-pro-document/td-p/1039453

    def getParameterInfo(self):
        '''
        Define parameter defitions
        '''
        param0 = arcpy.Parameter(
            displayName="Map Series Feature",
            name="map_series_feature",
            datatype="GPLayer",
            parameterType="Required",
            direction="Input")
        param1 = arcpy.Parameter(
            displayName="Scale Type",
            name="Scale Type",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param1.filter.list = ['Relative', 'Ratio_FtToIich']
        parameters = [param0, param1]
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

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return
    def execute(self, parameters, messages):
        """The source code of the tool."""

        def get_scale_factor(is_relative, scale_factor, layout_width, layout_ht):
            dx_relative = (scale_factor * layout_width * (1 / 12)) * 0.5
            dy_relative = (scale_factor * layout_ht * (1 / 12)) * 0.5
            dx_in2feet = (scale_factor * layout_width) * 0.5
            dy_in2feet = (scale_factor * layout_ht) * 0.5
            if is_relative:
                dx = dx_relative
                dy = dy_relative
            else:
                dx = dx_in2feet
                dy = dy_in2feet
            return (dx, dy)

        feat_index = parameters[0].valueAsText
        scale_factor_type = parameters[1].valueAsText
        sd = {'Relative':True,'Ratio_FtToIich':False}
        relative = sd[scale_factor_type]

        fields_index = ['SHAPE@','SHAPE@XY']
        calc_fields_order = ['LAYOUT_HT', 'LAYOUT_WIDTH', 'SCALE_FACTOR']
        fields_index.extend(calc_fields_order)

        with arcpy.da.UpdateCursor(feat_index, fields_index) as cursor_index:
            d = {val:idx for idx, val in enumerate(fields_index) if val in calc_fields_order}
            for row in cursor_index:
                layout_ht = row[d['LAYOUT_HT']]
                layout_width = row[d['LAYOUT_WIDTH']]
                scale_factor = row[d['SCALE_FACTOR']]
                x,y=row[1]
                dx, dy = get_scale_factor(relative, scale_factor, layout_width, layout_ht)
                xmin = x - dx
                xmax = x + dx
                ymin = y - dy
                ymax = y + dy
                array = arcpy.Array([arcpy.Point(xmin, ymin),
                                     arcpy.Point(xmax, ymin),
                                     arcpy.Point(xmax, ymax),
                                     arcpy.Point(xmin, ymax)
                                     ])
                polygon = arcpy.Polygon(array)
                row[0]=polygon
                cursor_index.updateRow(row)
        del cursor_index

