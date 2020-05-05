# Try creating polygon feature indexes with points
path_to_gdb = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/KRRP_Project.gdb'
path_out = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/camas_transLines_20200422.gdb'
scratch_workspace = 'C:/Users/uhlmann/GIS/data/scratch/scratch.gdb'

path_working=copy.copy(path_out)
arcpy.env.workspace=copy.copy(path_working)
arcpy.env.scratchWorkspace = copy.copy(scratch_workspace)

output = "test_line.shp"
first_point = 'idx_first_point.shp'
arcpy.CreateFeatureClass_management(path_working, output, "Polygon")
cur = arcpy.InsertCursor(output)
lineArray = arcpy.Array()

# start point
arcpy.da.SearchCursor(first_point_lyr)
first_point=[]
with arcpy.da.SearchCursor(first_point_lyr, ["shape@x", "shape@y"]) as cursor:
    first_point.append(cursor)
start = arcpy.Point()
(start.ID, start.X, start.Y) = (1, origin_x, origin_y)
lineArray.add(start)

# end point
end = arcpy.Point()
(end.ID, end.X, end.Y) = (2, end_x, end_y)
lineArray.add(end)

# write our fancy feature to the shapefile
feat = cur.newRow()
feat.shape = lineArray
cur.insertRow(feat)

# yes, this shouldn't really be necessary...
lineArray.removeAll()
del cur
