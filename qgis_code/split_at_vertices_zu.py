
import arcpy

in_feat = 'RoadSegment'
def vertices_to_pts(in_feat, out_feat, split_type):
    # get line feature geometry objects
    with arcpy.da.SearchCursor(in_feat, ['OBJECTID', 'SHAPE@']) as cursor:
        lines = [r[1] for r in cursor]
    del cursor

    # b) Assemble pts into array and package into Polyline
    start_pts, end_pts = [],[]
    ct=0
    coord_array = arcpy.Array()
    for line in lines:
        segments = line.getPart()[0]
        start, end = segments[0], segments[-1]
        start_pts = start_pts + [arcpy.Point(start.X,start.Y)]
        end_pts = end_pts + [arcpy.Point(end.X, end.Y)]
        ct+=1
    # CREATE FCs
    # c) manually
    feat_type = 'Point'
    m = 'No'
    z = 'Yes'
    shp_dir = r'C:\Users\Uhlmann\boxish\graip_dir\staging\scratch'
    arcpy.CreateFeatureclass_management(arcpy.env.scratchGDB, '{}point}'.format(split_type), feat_type, has_m = m, has_z = z)

    new_feat = arcpy.CreateUniqueName(split_type, arcpy.env.scratchGDB)
    split_type_dict = {'Start':start_pts,'End':end_pts}
    pts = split_type_dict[split_type]
    feats = ['SHAPE@XY']
    with arcpy.da.InsertCursor(new_feat, feats) as cursor:
        for pt in pts:
            cursor.insertRow([pt])
    del cursor