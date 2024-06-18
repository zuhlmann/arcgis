# USEFUL RESOURCES
# A) finding python exe in qgis python
# https://gis.stackexchange.com/questions/361545/how-do-i-specify-the-qgis-specific-python-version-to-add-python-packages-to-that
# B) QGIS in Conda
# https://gis.stackexchange.com/questions/119495/does-qgis-work-with-anaconda

# 20240502 Output values from selected features in location field

lyr_name = 'lidar_index_2022'
layer_in = QgsProject.instance().mapLayersByName(lyr_name)
layer_in = layer_in[0].selectedFeatures()


# Append a list with the values of your field
values_field = []
for feature in layer_in:
    values_field.append(feature['location']) # gml_id is the name of my field

# Open your csv file
with open(r'C:\Box\MCM USERS\3.0 - Employees\zuhlmann\qgis_utils\staging2\tutorial_data_reproject.txt', 'w') as file:
    # Write in your file
    for feature in values_field:
        file.write(feature)
        file.write('\n') # line break

# Close your csv file
file.close()

# A) Creating Vector File
# from qgis.core import (
#   QgsApplication,
#   QgsDataSourceUri,
#   QgsCategorizedSymbolRenderer,
#   QgsClassificationRange,
#   QgsPointXY,
#   QgsProject,
#   QgsExpression,
#   QgsField,
#   QgsFields,
#   QgsFeature,
#   QgsFeatureRequest,
#   QgsFeatureRenderer,
#   QgsGeometry,
#   QgsGraduatedSymbolRenderer,
#   QgsMarkerSymbol,
#   QgsMessageLog,
#   QgsRectangle,
#   QgsCoordinateReferenceSystem,
#   QgsRendererCategory,
#   QgsRendererRange,
#   QgsSymbol,
#   QgsVectorDataProvider,
#   QgsVectorLayer,
#   QgsVectorFileWriter,
#   QgsWkbTypes,
#   QgsSpatialIndex,
#   QgsVectorLayerUtils
# )
#
# from qgis.PyQt.QtCore import QVariant
#
# # https://gis.stackexchange.com/questions/30261/creating-new-empty-vector-layer-with-pyqgis/349354#349354
# vl = QgsVectorLayer("Point", "lebranius", "memory")
# pr = vl.dataProvider()
# # Enter editing mode
# vl.startEditing()
# # add fields
# pr.addAttributes([QgsField("location", QVariant.String),
#                   QgsField("age", QVariant.Int),
#                   QgsField("size", QVariant.Double)])
# # add a feature
# # To just create the layer and add features later, delete the four lines from here until Commit changes
# fet = QgsFeature()
# fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(15, 60)))
# fet.setAttributes(["Johny", 20, 0.3])
# pr.addFeatures([fet])
# # Commit changes
# vl.commitChanges()
#
# # https://docs.qgis.org/3.34/en/docs/pyqgis_developer_cookbook/vector.html
# save_options = QgsVectorFileWriter.SaveVectorOptions()
# save_options.driverName = "ESRI Shapefile"
# save_options.fileEncoding = "UTF-8"
# context = QgsCoordinateTransformContext()
# error = QgsVectorFileWriter.writeAsVectorFormatV3(vl,
#                                                   r'C:\Users\UhlmannZachary\Documents\staging\CONVERTED_zu\temp_index\test.shp',
#                                                   context, save_options)
#
# if error[0] == QgsVectorFileWriter.NoError:
#     print("success again!")
# else:
#   print(error)

# # GDALTINDEX
# # B1) gdaltindex through shell
# import subprocess
#
# # constants
# gdalTranslate = r'"C:\Program Files\QGIS 3.22.6\bin\gdaltindex.exe"'
# dst = r'C:\Users\UhlmannZachary\Documents\staging\CONVERTED_zu\temp_index\cl_text.shp'
# input_list = r'C:\Users\UhlmannZachary\Documents\staging\CONVERTED_zu\projected\README_projected.txt'
# cmd = '"{}" --optfile "{}"'.format(dst, input_list)
#
# fullCmd = ' '.join([gdalTranslate, cmd])
# subprocess.run(fullCmd)

# B2) From scratch withOUT shelling out
from osgeo import gdal
import os

# https://gis.stackexchange.com/questions/57834/how-to-get-raster-corner-coordinates-using-python-gdal-bindings
base_dir = r'C:\Box\MCM USERS\3.0 - Employees\zuhlmann\qgis_utils'
# fp_in = r'C:\Users\UhlmannZachary\Documents\staging\CONVERTED_zu\temp_index\tile_index.shp'
# # df=pd.read_csv(fp_in, )
# src = gdal.Open(r"C:\Users\UhlmannZachary\Documents\staging\CONVERTED_zu\temp_index\2015_OLC_Wallowa_3DEP_bh_45117d2.tif")
# ulx, xres, xskew, uly, yskew, yres  = src.GetGeoTransform()
# lrx = ulx + (src.RasterXSize * xres)
# lry = uly + (src.RasterYSize * yres)

# # WRITE METHODS/atts to txt
# gdal_dset_atts = dir(gdal)
# os_environ = os.environm
# with open(os.path.join(base_dir, 'GDAL_CL_methods.txt'), 'w') as out_file:
#     str_formatted = '\n'.join(gdal_dset_atts)
#     out_file.write(str_formatted)
# out_file.close()
