import arcpy
import os

# https://gis.stackexchange.com/questions/229187/copying-only-certain-fields-columns-from-shapefile-into-new-shapefile-using-mode

def copy_with_fields(in_fc, out_fc, keep_fields, where=''):
    """
    Required:
        in_fc -- input feature class
        out_fc -- output feature class
        keep_fields -- names of fields to keep in output

    Optional:
        where -- optional where clause to filter records
    """
    fmap = arcpy.FieldMappings()
    fmap.addTable(in_fc)

    # get all fields
    fields = {f.name: f for f in arcpy.ListFields(in_fc)}

    # clean up field map
    for fname, fld in fields.items():
        if fld.type not in ('OID', 'Geometry') and 'shape' not in fname.lower():
            if fname not in keep_fields:
                fmap.removeFieldMap(fmap.findFieldMapIndex(fname))

    # copy features
    path, name = os.path.split(out_fc)
    arcpy.conversion.FeatureClassToFeatureClass(in_fc, path, name, where, fmap)
