# Get CSVs to reproject from input path
import csv
import pyproj
from functools import partial
from os import listdir, path

# From here
# https://gis.stackexchange.com/questions/168081/how-to-reproject-500-csv-files-efficiently-and-easily-using-qgis
# and here
# https://gis.stackexchange.com/questions/168081/how-to-reproject-500-csv-files-efficiently-and-easily-using-qgis

#Define some constants at the top
#Obviously this could be rewritten as a class with these as parameters

lon = 'CoordX' #name of longitude field in original files
lat = 'CoordY' #name of latitude field in original files
f_x = 'CoorX_reprojected' #name of new x value field in new projected files
f_y = 'CoorY_reprojected' #name of new y value field in new projected files
in_file = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Request_Tracking\\GIS_Request_Internal_Fall_Creek\\fch_2019_control_points.csv' #input directory
out_file = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Request_Tracking\\GIS_Request_Internal_Fall_Creek\\fch_2019_control_points_CA_SP12.csv' #output directory
input_projection = 'epsg:6339' #WGS84
output_projecton = 'epsg:2225' #CA State Plane 1 feet

#Define partial function for use later when reprojecting
# user open pyproj.Proj(init=bla, preserve_units = True) if want Z the same
project = partial(
    pyproj.transform,
    pyproj.Proj(init=input_projection),
    pyproj.Proj(init=output_projecton))

#open a writer, appending '_project' onto the base name
with open(out_file, 'w') as w:
    #open the reader
    with open(in_file, 'r') as r:
        reader = csv.DictReader(r)
        #Create new fieldnames list from reader
        # replacing lon and lat fields with x and y fields
        fn = [x for x in reader.fieldnames]
        fn[fn.index(lon)] = f_x
        fn[fn.index(lat)] = f_y
        writer = csv.DictWriter(w, fieldnames=fn)
        #Write the output
        writer.writeheader()
        for row in reader:
            x,y = (float(row[lon]), float(row[lat]))
            try:
                #Add x,y keys and remove lon, lat keys
                row[f_x], row[f_y] = project(x, y)
                row.pop(lon, None)
                row.pop(lat, None)
                writer.writerow(row)
            except Exception as e:
                #If coordinates are out of bounds, skip row and print the error
                print(e)
