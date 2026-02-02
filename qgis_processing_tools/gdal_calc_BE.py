# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (atS your option) any later version.                                   *
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

class gdal_calc_BE(QgsProcessingAlgorithm):
    """
    Use tile index file to perform gdal functions. Tile feature must have attribute
    with path/to/raster/tiles.  

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    INPUT_A = 'INPUT_A'
    INPUT_B = 'INPUT_B'
    OUTFILE = 'Output File'

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return gdal_calc_BE()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'GDAL BuildVRT from Selection'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('gdal_calc_cutline')

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
        return self.tr("Using Tile Index, output vrt from tile selected in att table.")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # We add the input vector features source. It can have any kind of
        # geometry.
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_A,
                self.tr('Input Raster Interior'),
                [QgsProcessing.TypeRaster]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_B,
                self.tr('Input Raster Exterior'),
                [QgsProcessing.TypeRaster]
            )
        )
        self.addParameter(
            QgsProcessingParameterParameterFileDestination(
                self.OUTFILE,
                self.tr('Output raster from calculator'),
                self.fileFilter('.tif'),
                self.defaultValue('.tif')
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
        fp_raster1 = self.parameterAsFile(
            parameters,
            self.INPUT_1,
            context)
        fp_raster2 = self.parameterAsFile(
            parameters,
            self.INPUT_2,
            context)
        fp_raster_out = self.parameterAsString(
            parameters,
            self.OUTFILE,
            context)

        # If source was not found, throw an exception to indicate that the algorithm
        # encountered a fatal error. The exception text can be any string, but in this
        # case we use the pre-built invalidSourceError method to return a standard
        # helper text for when a source cannot be evaluated
        if raster1 is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT_A))
        if raster2 is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT_B))

        #(sink, dest_id) = self.parameterAsSink(
        #    parameters,
        #    self.OUTPUT,
        #    context, source.fields(),source.wkbType(),source.sourceCrs())


        CL_gdal_calc = f'gdal_calc -A r"{fp_raster1}" -B r"{fp_raster2}" --extent union --co COMPRESS=LZW --NoDataValue -9999 --outfile fp_out --calc="A-B"'

        import subprocess

        # constants
        output_dir = r'E:\tolt\2022'
        with open(os.path.join(output_dir, 'command_call.txt'),'w') as txt_file2:
            txt_file2.write(CL_gdal_calc)
        subprocess.run(CL_gdal_calc)
        
        results= {self.OUTPUT: cmd}
        
        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        return results
