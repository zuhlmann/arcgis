import arcpy

layout_width = 9.8
layout_ht = 6
# Set true for relative, false for 1 inch = n feet scale convention
relative=False
ft_to_in_scale = 1320
relative_scale = 24000

def get_incr(is_relative, scale_factor):
    # multiply by 0.5 because we are starting at centroid.  dx + dx = full indice width
    # _relative and _in2feet are for the two scale representations.  Set one above along with boolean
    dx_relative = (scale_factor * layout_width * (1/12)) * 0.5
    dy_relative = (scale_factore * layout_ht * (1/12)) * 0.5
    dx_in2feet = (scale_factor * layout_width) *0.5
    dy_in2feet = (scale_factor * layout_ht) * 0.5
    if is_relative:
        dx = dx_relative
        dy = dy_relative
    else:
        dx = dx_in2feet
        dy = dy_in2feet
    return(dx, dy)

feat_centroid = r'C:\Box\MCMGIS\Project_Based\Chugach_Electric\Chugage_Hydro_24_057\map_docs\chugach_hydro_regulatory\chugach_hydro_regulatory.gdb\labels_ddp\chugach_regulatory_extents_v2'
feat_index = r'C:\Box\MCMGIS\Project_Based\Chugach_Electric\Chugage_Hydro_24_057\map_docs\chugach_hydro_regulatory\chugach_hydro_regulatory.gdb\labels_ddp\chugach_regulatory_extents_v3'
bad_vals = ['shape', 'objectid', 'fid']
fields_base = [f for f in arcpy.ListFields(feat_centroid) if not any(v in f.name.lower() for v in bad_vals)]
field_names_base = [f.name for f in fields_base]
fields_cursor = ['SHAPE@X','SHAPE@Y','SCALE_FACTOR']
fields_cursor.extend(field_names_base)
fields_index = ['SHAPE@','SCALE_FACTOR']
fields_index.extend(field_names_base)

#Add fields to new feature class if not existing
field_names_index = [f.name for f in arcpy.ListFields(feat_index)]
# add_fields = list(set(field_names_base)-set(field_names_index))
# add_fields = [f for f in fields_base if f.name in add_fields]
for f in fields_base:
    if f.name not in field_names_index:
        print(f"ADDING field: {f.name} to Index Feat")
        arcpy.AddField_management(feat_index, f.name, f.type)

with arcpy.da.SearchCursor(feat_centroid, fields_cursor) as cursor_centroid:
    with arcpy.da.InsertCursor(feat_index, fields_index) as cursor_index:
        for row in cursor_centroid:
            x = row[0]
            y = row[1]
            scale_factor = row[2]
            dx,dy = get_scale_factor(relative, scale_factor)
            xmin=x-dx
            xmax=x+dx
            ymin=y-dy
            ymax=y+dy
            array = arcpy.Array([arcpy.Point(xmin, ymin),
                                 arcpy.Point(xmax, ymin),
                                 arcpy.Point(xmax, ymax),
                                 arcpy.Point(xmin, ymax)
                                 ])
            polygon = arcpy.Polygon(array)
            row_index = [polygon]
            row_index.extend(row[2:])
            cursor_index.insertRow(row_index)
del cursor_centroid
del cursor_index