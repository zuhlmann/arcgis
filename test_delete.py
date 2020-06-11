import arcpy

def test_feat_methods(fp_in):
    arcpy.MakeFeatureLayer_management(fp_in, 'layer_make_feature')
    arcpy.CopyFeatures_management(fp_in, 'in_memory/in_memory_feature')
