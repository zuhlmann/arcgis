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
                       QgsProcessingParameterFile,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFileDestination,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterField,
                       QgsProcessingParameterString,
                       QgsProcessingParameterFolderDestination,
                       QgsProcessingOutputString)

class gdaltindex_from_list(QgsProcessingAlgorithm):
    """
    Use tile index file to perform gdal functions. Tile feature must have attribute
    with path/to/raster/tiles.  

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    INPUT = 'INPUT'
    OUTPUT = 'output'
    OUTPUT_DIR = 'output_dir'
    BASE_FILENAME = 'base_filename'

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return gdal_from_slxn()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'GDAL Utilities from Selection'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('gdaltindex_from_list')

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
        return self.tr("Pass raster list to get index file")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # We add the input vector features source. It can have any kind of
        # geometry.
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input Layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.OUTPUT_DIR,
                'output directory for index file'
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.BASE_FILENAME, 
                'filename for index'
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
        source = self.parameterAsSource(
            parameters,
            self.INPUT,
            context)
        output_dir = self.parameterAsString(
            parameters,
            self.OUTPUT_DIR,
            context)
        base_filename = self.parameterAsString(
            parameters,
            self.BASE_FILENAME,
            context)
        

        # If source was not found, throw an exception to indicate that the algorithm
        # encountered a fatal error. The exception text can be any string, but in this
        # case we use the pre-built invalidSourceError method to return a standard
        # helper text for when a source cannot be evaluated
        if source is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))

        #(sink, dest_id) = self.parameterAsSink(
        #    parameters,
        #    self.OUTPUT,
        #    context, source.fields(),source.wkbType(),source.sourceCrs())

        # #Send some information to the user
        # feedback.pushInfo('CRS is {}'.format(source.sourceCrs().authid()))
        fp_optfile = '{}.txt'.format(os.path.join(output_dir, base_filename))
        features = source.getFeatures()
        vals = [f[location_field] for f in features]
        with open(fp_optfile, 'w') as list_out:
            basic_str = '\n'.join(vals)
            list_out.write(basic_str)    

        vrt_out = '{}.vrt'.format(os.path.join(output_dir, base_filename))
        
        import subprocess

        # constants
        gdalbuildvrt = r'"C:\Program Files\QGIS 3.22.6\bin\gdalbuildvrt.exe"'
        cmd = '-input_file_list "{}" "{}"'.format(fp_optfile, vrt_out)

        fullCmd = ' '.join([gdalbuildvrt, cmd])
        with open(os.path.join(output_dir, 'command_call.txt'),'w') as txt_file2:
            txt_file2.write(fullCmd)
        subprocess.run(fullCmd)
        
        results= {self.OUTPUT: fullCmd}
        
        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        return results
