import os
from osgeo import gdal
from osgeo import osr
import numpy

# FROM HERE:
# https://gis.stackexchange.com/questions/290776/how-to-create-a-tiff-file-using-gdal-from-a-numpy-array-and-specifying-nodata-va

# config
GDAL_DATA_TYPE = gdal.GDT_Int32
GEOTIFF_DRIVER_NAME = r'GTiff'
NO_DATA = 15
SPATIAL_REFERENCE_SYSTEM_WKID = 4326

def create_raster(output_path,
                  columns,
                  rows,
                  nband = 1,
                  gdal_data_type = GDAL_DATA_TYPE,
                  driver = GEOTIFF_DRIVER_NAME):
    ''' returns gdal data source raster object

    '''
    # create driver
    driver = gdal.GetDriverByName(driver)

    output_raster = driver.Create(output_path,
                                  int(columns),
                                  int(rows),
                                  nband,
                                  eType = gdal_data_type)
    return output_raster

def numpy_array_to_raster(output_path,
                          numpy_array,
                          upper_left_tuple,
                          cell_resolution,
                          nband = 1,
                          no_data = NO_DATA,
                          gdal_data_type = GDAL_DATA_TYPE,
                          spatial_reference_system_wkid = SPATIAL_REFERENCE_SYSTEM_WKID,
                          driver = GEOTIFF_DRIVER_NAME, **kwargs):
    ''' returns a gdal raster data source

    keyword arguments:

    output_path -- full path to the raster to be written to disk
    numpy_array -- numpy array containing data to write to raster
    upper_left_tuple -- the upper left point of the numpy array (should be a tuple structured as (x, y))
    cell_resolution -- the cell resolution of the output raster [x,y]; prior to 202408 it was a single value
    nband -- the band to write to in the output raster
    no_data -- value in numpy array that should be treated as no data
    gdal_data_type -- gdal data type of raster (see gdal documentation for list of values)
    spatial_reference_system_wkid -- well known id (wkid) of the spatial reference of the data
    driver -- string value of the gdal driver to use
    kwarg -- raster_with_projection.  provide file path to raster with
            proper projection info if wkid unrecognized by OGR.  ZU 20220909

    '''

    print('UL: ({}, {})'.format(upper_left_tuple[0],
                            upper_left_tuple[1]))

    rows, columns = numpy_array.shape
    print('ROWS: {}\n COLUMNS: {}\n'.format(rows,
                                        columns))

    # create output raster
    output_raster = create_raster(output_path,
                                  int(columns),
                                  int(rows),
                                  nband,
                                  gdal_data_type)

    # info here on affine transformation:
    # https://stackoverflow.com/questions/27166739/description-of-parameters-of-gdal-setgeotransform
    # Follow link to GDAL docs in link for more info
    geotransform = (upper_left_tuple[0],
                    cell_resolution[0], 0,
                    upper_left_tuple[1], 0,
                    cell_resolution[1])

    # If not assigning proper projection, may mean that OGR does not recognize the Wkt.
    # In that case, try pulling from raster with properly-assigned projection info
    # probably originated from ESRI.  ZU 20220909
    try:
        ds = gdal.Open(kwargs['raster_with_projection'])
        output_raster.SetProjection(ds.GetProjection())##sets same projection as input
    except KeyError:
        spatial_reference = osr.SpatialReference()
        spatial_reference.ImportFromEPSG(spatial_reference_system_wkid)
        output_raster.SetProjection(spatial_reference.ExportToWkt())
    output_raster.SetGeoTransform(geotransform)
    output_band = output_raster.GetRasterBand(1)
    output_band.SetNoDataValue(no_data)
    output_band.WriteArray(numpy_array)
    output_band.FlushCache()
    output_band.ComputeStatistics(False)

    if os.path.exists(output_path) == False:
        raise Exception('Failed to create raster: {}'.format(output_path))

    return  output_raster
