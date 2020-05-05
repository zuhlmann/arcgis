# 4/13/20
# exporting multiple layers to gdb
import arcpy

# arcpy.env.scratchWorkspace = 'C:/Users/uhlmann/GIS/data/scratch/scratch.gdb'
arcpy.env.scratchWorkspace = 'C:/Users/uhlmann/GIS/data/scratch/scratch.gdb'
arcpy.env.workspace = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived'

# in_feature = ['feature1.shp', 'feature2.shp']
in_feature_dataset = ['Stantec/klamath_rec_rest_30per_2/Recreation_30pct_Site_Boundaries.shp',
                        'Stantec/20191204_ToBenji_CurrentLoWs.gdb/Low_Stantac_Recreation']
out_location = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/Proposed_Deliverables/Kleinshmidt.gdb'

arcpy.FeatureClassToGeodatabase_conversion(in_feature, out_location)

Internal review QA/QC process
