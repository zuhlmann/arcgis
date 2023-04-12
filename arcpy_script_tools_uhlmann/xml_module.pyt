# -*- coding: utf-8 -*-

import arcpy
from arcpy import metadata as md
import os
import logging
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET


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
            displayName="Input Feature",
            name="fc_in",
            datatype="Layer",
            parameterType="Required",
            direction="Input")
        param1 = arcpy.Parameter(
            displayName="path/to/directory/for/csv",
            name="csv directory",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")
        param2 = arcpy.Parameter(
            displayName="filename or filename.csv",
            name="csv filename",
            datatype="GPString",
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
        if parameters[2].value:
            csv_dir = parameters[1].valueAsText
            fname = parameters[2].valueAsText
            # ensure file type is specified
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

class define_xml_elements(object):
    """Updates metadata of Layer (shp, feature class, etc.) from template"""
    def __init__(self):
        self.label = 'step2_attr_level_metadata'
        self.description = 'Metadata step 2: after adding values to xml element template, run this to stamp metadata'
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
            displayName="Processing Directory",
            name="processing_dir",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")
        param2 = arcpy.Parameter(
            displayName="Populated XML CSV",
            name="xml_csv",
            datatype="DETextFile",
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
        processing_dir = parameters[1].valueAsText
        xml_csv = parameters[2].valueAsText
        desc = arcpy.Describe(fc)
        fp_fc = desc.featureClass.catalogPath

        # Initiate logging: send to processing dir
        fname = os.path.split(fp_fc)[-1]
        fp_logfile = os.path.join(processing_dir, r'{}_logfile.log'.format(fname))

        # Path/to/xml create or identify
        if desc.featureClass.dataType == 'ShapeFile':
            fp_xml = '{}.xml'.format(fp_fc)
        elif desc.featureClass.dataType == 'FeatureClass':
            fp_xml = os.path.join(processing_dir, '{}.xml'.format(fname))

        tgt_item_md = md.Metadata(fp_fc)
        tgt_item_md.synchronize('ALWAYS')
        tgt_item_md.exportMetadata(fp_xml, metadata_export_option = r'FGDC_CSDGM')

        logging.basicConfig(filename = fp_logfile, level = logging.DEBUG)

        df_xml_trans = pd.read_csv(xml_csv, index_col='attrlabl')
        tree = ET.parse(fp_xml)
        root = tree.getroot()
        # Main nodes
        eainfo = root.find('eainfo')
        detailed = eainfo.find('detailed')

        # If more nodes requiring updates from df add to tgt_nodes list
        tgt_nodes = ['attrdef', 'attrdefs']
        attr_child = detailed.findall('attr')
        for c in attr_child:
            try:
                attrlabl = c.find('attrlabl').text
                for nd in tgt_nodes:
                    try:
                        v = df_xml_trans.loc[attrlabl, nd]
                        # No value from csv/dataframe i.e. no value to replace
                        if not pd.isnull(v):
                            c.find(nd).text = df_xml_trans.loc[attrlabl, nd]
                            logging.info('Replaced: {} with: {}'.format(c.find(nd).text, v))
                    except KeyError:
                        logging.info('Key: {} not present in dataframe'.format(attrlabl))
                    except AttributeError:
                        # if NoneType --> tgt_node needs to be created and populated in xml
                        ET.SubElement(c, nd)
                        c.find(nd).text = df_xml_trans.loc[attrlabl, nd]
                        logging.info('Created new subelement: {} in {}'.format(nd, attrlabl))
            except KeyError:
                logging.info('The following Key does not have attrlabl: {}'.format(c.tag, c.attr))

        tree.write(fp_xml)

        tgt_item_md.importMetadata(fp_xml, metadata_import_option = 'FGDC_CSDGM')
        tgt_item_md.save()
        return
