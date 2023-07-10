import arcpy
import os
import pandas as pd

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Metadata Toolbox"
        self.alias = "Metadata Toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [xml_element_template, define_xml_elements]

class xml_element_template(object):
    """Outputs a csv to be populated and used in subsequent method - update_attr """
    def __init__(self):
        self.label = "step1_attr_level_metadata"
        self.desciption = "create inventory of xml elements relevant to fields"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="Path to Input File Geodatabase",
            name="gdb_in",
            datatype="DEGeodatasetType",
            parameterType="Required",
            direction="Input")
        param1 = arcpy.Parameter(
            displayName="path/to/directory/output/shp",
            name="shapefile directory",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")
        param2 = arcpy.Parameter(
            displayName="Dataset Folders",
            name="Dataset Folders",
            datatype="GPBoolean",
            parameterType="Required",
            direction="Input")
        parameters = [param0, param1, param2]

        return parameters

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""

        # This if statement required or else error message will for parameter[0]
        # "TypeError: stat: path should be string, bytes, os.PathLike or integer, not NoneType.
        # Apparently this method will run through ALL parameters right off the bat.  So add
        # conditional statements to only validate target parameters i.e. parameter[1] in this case
        if parameters[1].value and parameters[2].value:
            shp_dir = parameters[1].valueAsText
            dsets = parameters[2]
            # ensure file type is specified
            if dsets:
                dsets = arcpy.ListDatasets
                subdirs = [os.path.join(shp_dir, d) for d in dsets]
            else:
                pass
            if fname[-4:] == '.csv':
                pass
            else:
                fname = '{}.csv'.format(fname)
            fp_csv = os.path.join(csv_dir, fname)

            if os.path.exists(fp_csv):
                parameters[2].setErrorMessage('File specified by path and filename already exists')
            else:
                parameters[2].clearMessage()

        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        fc = parameters[0]
        desc = arcpy.Describe(fc)
        fp_fc = desc.featureClass.catalogPath
        csv_dir = parameters[1].valueAsText
        fname = parameters[2].valueAsText

        # ensure file specifier
        if fname[-4:] == '.csv':
            pass
        else:
            fname = '{}.csv'.format(fname)

        fp_csv = os.path.join(csv_dir, fname)
        flds = [f.name for f in arcpy.ListFields(fp_fc)]
        vals = np.column_stack([flds, [None] * len(flds), [None] * len(flds), [None] * len(flds)])
        # attrdef = definition
        # attrdefs = definition source
        cn = ['attrlabl', 'attralias', 'attrdef', 'attrdefs']
        df_fields = pd.DataFrame(vals, columns=cn)
        df_fields.to_csv(fp_csv)
        return
