# -*- coding: utf-8 -*-

import arcpy
from arcpy import metadata as md
import os


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "balls"

        # List of tool classes associated with this toolbox
        self.tools = [metadata_mcm]


class metadata_mcm(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "metadata_mcm"
        self.description = "something"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="Input Feature",
            name="fc_in",
            datatype="Layer",
            parameterType="Required",
            direction="Input")
        param1 = arcpy.Parameter(
            displayName="Output Directory",
            name="dir_out",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")
        param2 = arcpy.Parameter(
            displayName="XML Filename",
            name="fname_xml",
            datatype="String",
            parameterType="Required",
            direction="Input")
        params = []
        params.append(param0)
        params.append(param1)
        params.append(param2)
        return params

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
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        fc = parameters[0]
        desc = arcpy.Describe(fc)
        fp_fc = desc.featureClass.catalogPath
        dir_out = parameters[1].valueAsText
        fname_xml = r'{}.xml'.format(parameters[2].valueAsText)
        tgt_item_md = md.Metadata(fp_fc)
        tgt_item_md.synchronize('ALWAYS')
        fp_xml = os.path.join(dir_out, fname_xml)
        tgt_item_md.saveAsXML(fp_xml, 'EXACT_COPY')

        # if desc.featureClass.dataType == 'FeatureClass':
        # else:
        #     fp_shp = desc.featureClass.catalogPath
        #     fp_xml = fp_shp.replace('.shp', '.xml')
        #     if not os.path.exists(fp_xml):
        #     tgt_item_md.synchronize('ALWAYS')
        #     tgt_item_md.saveAsXML(fp_xml, 'EXACT_COPY')
        #     tgt_item_md = md.Metadata(fp_in)

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""

        return