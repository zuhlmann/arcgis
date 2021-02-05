# SCROUNGING DELETED SCRIPTS
# ZRU 1/29/21
# Add to this overtime to grab useful tidbits

# 1) PRINT EXCEPTION
arcpy.overwriteOutput = True

input1 = 'KauiRoads'
temp_lyr = 'temp_lyr'
file_out = 'road_buffer'

gdb_main = 'C:/Users/uhlmann/GIS/West_Kaui_Energy_Project/Easements/Easements_Digitize.gdb'
gdb_scratch = 'C:/Users/uhlmann/GIS/data/scratch/scratch.gdb'

output = '{0}/{1}'.format(gdb_scratch, file_out)

try:
    # Make a layer from a feature class
    print(input)
    arcpy.MakeFeatureLayer_management(input1, temp_lyr)
    arcpy.Buffer_analysis(temp_lyr, output, '12.5 Feet')
except Exception:
    e = sys.exc_info()[1]
    print(e.args[0])
