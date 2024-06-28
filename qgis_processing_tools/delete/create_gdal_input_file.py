# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

import os
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFileDestination,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterField,
                       QgsProcessingParameterString,
                       QgsProcessingParameterFolderDestination,
                       QgsProcessingOutputString)

class gdal_input_file(QgsProcessingAlgorithm):
    """
    Use tile index file to perform gdal functions. Tile feature must have attribute
    with path/to/raster/tiles.  

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    OUTPUT = 'output'
    INPUT_DIR = 'output_dir'
    FILENAME = 'base_filename'
    FILETYPE_FILTER = 'filetype_filter'
    FULL_PATH = 'full_path'

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return gdal_input_file()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Input File for GDAL Utilities'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('gdal_input_file')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('scripts')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'scripts'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("Pass a directory with rasters, return a text file with folder contents." +
                        "List to be used as input_file_list / opt_list in GdalBuildVRT and GdalTindex" +
                        "To build .vrt and tile index respectively")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # We add the input vector features source. It can have any kind of
        # geometry.
        
        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.INPUT_DIR,
                'Output directory for results of this tool - a text file with list of rasters in INPUT_DIR'
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.FILENAME, 
                'Filename (without file extension i.e. - Klamath_2021_lidar_inventory)'
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                self.FILETYPE_FILTER,
                'Select raster type / file extension to inventory',
                ['.tif','.vrt'], defaultValue='.tif',
                usesStaticStrings=True
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.FULL_PATH,
                'Do you want full path (Yes) or just Filename (No)'
            )
        )
        # https://docs.qgis.org/3.34/en/docs/user_manual/processing/scripts.html
        self.addOutput(
            QgsProcessingOutputString(
                self.OUTPUT,
                'test this sting'
            )
        )
        
    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        input_dir = self.parameterAsString(
            parameters,
            self.INPUT_DIR,
            context)
        filename = self.parameterAsString(
            parameters,
            self.FILENAME,
            context)
        # https://gis.stackexchange.com/questions/481785/using-qgsprocessingparameterenum-in-qgis-python-processing-script
        filetype_filter = self.parameterAsString(
            parameters,
            self.FILETYPE_FILTER,
            context)
        full_path = self.parameterAsBoolean(
            parameters,
            self.FULL_PATH,
            context)

        # If source was not found, throw an exception to indicate that the algorithm
        # encountered a fatal error. The exception text can be any string, but in this
        # case we use the pre-built invalidSourceError method to return a standard
        # helper text for when a source cannot be evaluated
        
        #if source is None:
        #    raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))

        #(sink, dest_id) = self.parameterAsSink(
        #    parameters,
        #    self.OUTPUT,
        #    context, source.fields(),source.wkbType(),source.sourceCrs())

        # #Send some information to the user
        # feedback.pushInfo('CRS is {}'.format(source.sourceCrs().authid()))
        
        # if user added file extension, replace with nothing
        # whiteapces  -->  https://stackoverflow.com/questions/60290732/subprocess-with-a-variable-that-contains-a-whitespace-path
        filename = filename.replace('.txt','')
        fp_optfile = '{}.txt'.format(os.path.join(input_dir, filename))
        fn_list, fp=[],[]
        for fn in os.listdir(input_dir):
            if os.path.splitext(fn)[-1] in filetype_filter:
                fp_temp=os.path.join(input_dir,fn)
                fp.append(r'"{}"'.format(fp_temp))
                fn_list.append(fn)
        if full_path:
            file_list = fp
        elif not full_path:
            file_list=fn_list
        with open(fp_optfile, 'w') as list_out:
            basic_str = '\n'.join(file_list)
            list_out.write(basic_str)    

        message_out = 'Check in {} for the File: {}.txt'.format(input_dir, filename)
        
        results= {self.OUTPUT: message_out}
        
        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        return results
