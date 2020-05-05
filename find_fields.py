mxd = arcpy.mapping.MapDocument("CURRENT")
layers = arcpy.mapping.ListLayers(mxd)
layers_with_id = []
for layer in layers:
    #this simply makes a SQL expression
    expression1 = '{}{}'.format(arcpy.AddFieldDelimiters(layer, "DisturbTy"), " = 'Permanent'")
    expression2 = '{}{}'.format(arcpy.AddFieldDelimiters(layer, "DisturbTy"), " = 'Temporary'")
    #combine permanent and temporary SQL query into OR statement to find BOTH
    expression = '{} OR {}'.format(expression1, expression2)
    # add try/except because NOT ALL layers have fields
    try:
        with arcpy.da.SearchCursor(layer, "DisturbTy", where_clause=expression) as cursor:
            for row in cursor:
                print('{} {}'.format(layer, row[i]))
            # get layers with pertinent fields
            layers_with_id.append(layer.name)
    except:
        pass


print "The following layers have that unique ID:"
for a in layers_with_id:
    print a
