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
        self.label = "Parcels Toolbox"
        self.alias = "Parcels Toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [pull_PQ_parcels]

class pull_PQ_parcels(object):
    """Outputs a csv to be populated and used in subsequent method - update_attr """
    def __init__(self):
        self.label = "from shapefile subset csv, get parcel quest parcels from PQ csv"
        self.desciption = "from shapefile subset csv, get parcel quest parcels from PQ csv"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="path/to/output/directory/ for formatted table",
            name="dir_out",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")
        param1 = arcpy.Parameter(
            displayName="output filename for formatted PQ records",
            name="filename formatted PQ csv",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param2 = arcpy.Parameter(
            displayName="path/to/ParcelQuest/csv",
            name="csv file",
            datatype="DETextfile",
            parameterType="Required",
            direction="Input")
        param3 = arcpy.Parameter(
            displayName= "csv GIS attribute table",
            name="csv file",
            datatype="DETextfile",
            parameterType="Required",
            direction="Input")
        param4 = arcpy.Parameter(
            displayName="APN column name GIS",
            name="APN column name GIS",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        parameters = [param0, param1, param2, param3, param4]

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
        if parameters[1].value:
            csv_dir = parameters[0].valueAsText
            fname_out = parameters[1].valueAsText
            # ensure file type is specified
            if fname_out[-4:] == '.csv':
                pass
            else:
                fname_out = '{}.csv'.format(fname_out)
            fp_csv = os.path.join(csv_dir, fname_out)

            if os.path.exists(fp_csv):
                parameters[2].setErrorMessage('File specified by path and filename already exists')
            else:
                parameters[2].clearMessage()
        if parameters[4].value:
            gis_csv = parameters[3].valueAsText
            df_source = pd.read_csv(gis_csv)
            if parameters[4].valueAsText not in df_source.columns.to_list():
                parameters[4].setErrorMessage('Column title for APN is not in specified csv')
            else:
                parameters[4].clearMessage()

        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        dir_out = parameters[0].valueAsText
        csv_name = parameters[1].valueAsText
        csv_pq = parameters[2].valueAsText
        csv_source = parameters[3].valueAsText
        apn_source = parameters[4].valueAsText

        apn_target = 'APN_D'

        # ensure file specifier
        if csv_name[-4:] == '.csv':
            pass
        else:
            csv_name = '{}.csv'.format(fname)

        csv_out = os.path.join(dir_out, csv_name)


        # in case duplicates
        df_source = pd.read_csv(csv_source)
        df_pq = pd.read_csv(csv_pq, index_col='APN_D')
        df_source = df_source.drop_duplicates(subset=[apn_source], keep='first')
        df_source = df_source.set_index(apn_source)
        ommitted = df_source.index.difference(df_pq.index)
        df_source = df_source.drop(ommitted)

        df_pq = df_pq.loc[df_source.index]
        ser_append = pd.DataFrame(ommitted, columns=[apn_target])
        df_pq = df_pq.reset_index()
        df_source.index.names = [apn_target]

        df_pq = pd.concat([df_pq, ser_append])
        df_pq = df_pq.set_index(apn_target)
        df_pq.to_csv(csv_out)

        return


