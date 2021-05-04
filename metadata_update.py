import os
import arcpy
import xml.etree.ElementTree as ET
import base64
from pyodbc import connect as odbcconn
from pandas import read_sql_query as readsqlqry

# From Here
# https://community.esri.com/t5/python-questions/how-can-i-refresh-metadata-on-geodatabase-feature-classes/m-p/159598

num_elements = 0
featName = 'your_featureClassName'
fcPathName = 'Database Connections/your_geodatabase.sde/' + featName

# set up a connection to read user maintained metadata from a SQL Server table
metaConnStr = 'DRIVER={SQL Server};SERVER=servername;DATABASE=dbname;Trusted_Connection=yes'
conn = odbcconn(metaConnStr)
# your metadata source data will differ from the following
metaqry = 'SELECT [FULL_NAME],[COVER_NAME],[ABSTRACT],[UPDATEDATE],[OWNERNAME]' +\
 ',[PATH],[METAACCESS],[ONMAINT],[MAINTFREQ],[KNOWNERROR],[LINEAGE]' +\
 ',[DOMAIN],[RECTIFIED],[MAINTORG],[MAINTDESC],[LIBINPUT],[SOURCNAME]' +\
 ',[SOURCCONTACT],[SOURCDOCNAME],[SOURCDATE],[SOURCSCALE],[SOURCFORMAT]' +\
 ',[SOUR2NAME],[SOUR2CONTACT],[SOUR2DOCNAME],[SOUR2DATE],[SOUR2SCALE]' +\
 ',[SOUR2FORMAT],[ONMG],[MGLAYERNAME],[MGSCALELOW],[MGSCALEHIGH] ' +\
 'FROM [dbo].[metadata] WHERE [COVER_NAME] = \'' + featName + '\''
df_FCMeta = readsqlqry(metaqry, conn) # load query result to pandas dataframe
df_row = df_FCMeta.iloc[0] # get the one row in the dataframe. There is only one row per COVER_NAME

arcpy.env.overwriteOutput = True
# export the ESRI generated metadata from the target feature class
# install location
dir = arcpy.GetInstallInfo('desktop')['InstallDir']

# stylesheet to use
copy_xslt = r'{0}'.format(os.path.join(dir,'Metadata\Stylesheets\gpTools\exact copy of.xslt'))

# temporary XML file
xmlfile = arcpy.CreateScratchName('.xml',workspace=arcpy.env.scratchFolder)

# export xml
arcpy.XSLTransform_conversion(fcPathName, copy_xslt, xmlfile, '')

# get the tree object and root element from the exported xml file
tree = ET.parse(xmlfile)
root = tree.getroot()

# get the dataIdInfo element
dataIdInfoEl = root.find('dataIdInfo')

# dataIdInfo purpose element
# Create the needed purpose xml element
subEl = ET.SubElement(dataIdInfoEl,'idPurp')
subEl.text = df_row['FULL_NAME']
num_elements += 1

# dataIdInfo abstract element
# Create the needed abstract xml element
subEl = ET.SubElement(dataIdInfoEl,'idAbs')
subEl.text = df_row['ABSTRACT']
num_elements += 1

# import the thumbnail image (jpg) from a file folder by name. Thumbnail file must exist (created by a separate process)
thumbnailsPath = 'c:/thumbnails/'
jpgFile = thumbnailsPath + featName + '.jpg'
if os.path.exists(jpgFile):
 with open(jpgFile, "rb") as img_file:
  strEncoded = base64.b64encode(img_file.read())
 # Create the needed thumbnail xml element
 attrib = {'EsriPropertyType':'PictureX'}
 subEl = ET.SubElement(root,'Binary')
 subEl = ET.SubElement(subEl,'Thumbnail')
 subEl = ET.SubElement(subEl,'Data', attrib)
 subEl.text = strEncoded
 num_elements += 1

if num_elements > 0:
 # save modifications to XML
 tree.write(xmlfile)
 arcpy.MetadataImporter_conversion(xmlfile, fcPathName)
else:
 print('No changes to save')


# Zach's simplified version
# get source
fcs = 'path/to/fcs'
xslt_template = 'path/to/xslt/file'
xml_file = 'name.xml'
# xmltree update xml file
XSLTransform_conversion(fcs, xslt_template, xml_file,'')
arcpy.MetadataImporter_conversion(xmlfile, fcPathName)
