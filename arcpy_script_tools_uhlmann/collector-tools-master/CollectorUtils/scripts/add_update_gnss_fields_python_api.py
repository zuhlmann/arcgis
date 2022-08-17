"""
   Copyright 2017 Esri
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.​    
"""
import arcpy
import argparse
import sys
import json
from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection


# Parse Command-line arguments
def parseArguments():
    parser = argparse.ArgumentParser(
        usage='Add/Update GNSS metadate fields')

    arcpy.AddMessage("Parsing Arguments..")

    parser.add_argument('url', help='Organization url')
    parser.add_argument('username', help='Organization username')
    parser.add_argument('password', help='Organization password')
    parser.add_argument('itemId', type=str, help='Feature service Item Id')
    parser.add_argument('layerIndex', type=int, help='Feature Layer index. If not specified use 0 as index')
    parser.add_argument('-r', dest='remove', default=False, type=bool,
                        help='Set True if GNSS metadata fields need to be removed')

    args_parser = parser.parse_args()
    if '*' in args_parser.password:
        args_parser.password = password = arcpy.GetParameterAsText(2)
    arcpy.AddMessage("Done parsing arguments..")
    return args_parser


# Search for a item id and add GNSS Metadata fields
def searchItems_addGNSSMetadataFields(args_parser):
    # Search ItemIds
    gis = GIS(args_parser.url, args_parser.username, args_parser.password)
    
    arcpy.AddMessage("Signed into organization..")

    itemId = args_parser.itemId

    try:

        featureLayerItem = gis.content.get(itemId)

        # Construct a FeatureLayerCollection from the portal item.
        featureLayerCollection = FeatureLayerCollection.fromitem(featureLayerItem)

        # Extract fields from Feature layer service definition
        featureLayerFields = featureLayerCollection.manager.layers[args_parser.layerIndex].properties[
            'fields'] if args_parser.layerIndex else \
            featureLayerCollection.manager.layers[0].properties['fields']

        # Feature Layer index
        featureLayerIndex = args_parser.layerIndex if args_parser.layerIndex else 0

        # Check if the Feature layer is of type esriGeometryPoint
        if featureLayerCollection.manager.layers[featureLayerIndex].properties['geometryType'] != 'esriGeometryPoint':
            arcpy.AddError("Feature layer is not a point layer")
            raise ValueError("Feature layer is not a point layer")
        
        # New fields which need to be added
        gnssMetadataFields = {'fields': []}

        # Operations list - Add, Update or delete GNSS Metadata fields.
        operations = []

        arcpy.AddMessage("Adding/Updating gnss fields..")
        # Add/Update GNSS Metadata fields
        if not args_parser.remove:

            # ESRIGNSS_POSITIONSOURCETYPE
            positionsourcetypeField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_POSITIONSOURCETYPE']

            if positionsourcetypeField:
                # Field does exist check if the domain is set.
                if positionsourcetypeField[0]['domain'] == None:
                    if ([operation for operation in operations if operation == 'updateDefinition']):
                        operations.append('updateDefinition')

                    positionsourcetypeFieldIndex = featureLayerFields.index(positionsourcetypeField[0])
                    positionsourcetypeDomain = {'type': 'codedValue',
                                     'name': 'ESRI_POSITIONSOURCETYPE_DOMAIN',
                                     'codedValues': [{'name': 'Unknown',
                                                      'code': 0},
                                                     {'name': 'User defined', 'code': 1},
                                                     {'name': 'Integrated (System) Location Provider', 'code': 2},
                                                     {'name': 'External GNSS Receiver', 'code': 3},
                                                     {'name': 'Network Location Provider', 'code': 4}]}
                    featureLayerFields[positionsourcetypeFieldIndex]['domain'] = positionsourcetypeDomain

            else:
                gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_POSITIONSOURCETYPE',
                                                     'type': 'esriFieldTypeInteger',
                                                     'alias': 'Position source type',
                                                     'sqlType': 'sqlTypeOther',
                                                     'nullable': True,
                                                     'editable': True,
                                                     'domain': {'type': 'codedValue',
                                                                'name': 'ESRI_POSITIONSOURCETYPE_DOMAIN',
                                                                'codedValues': [
                                                                    {'name': 'Unknown', 'code': 0},
                                                                    {'name': 'User defined', 'code': 1},
                                                                    {'name': 'Integrated (System) Location Provider', 'code': 2},
                                                                    {'name': 'External GNSS Receiver', 'code': 3},
                                                                    {'name': 'Network Location Provider', 'code': 4}]},
                                                     'defaultValue': None})

            # ESRIGNSS_RECEIVER
            recieverField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_RECEIVER']
            
            if not recieverField:
                gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_RECEIVER',
                                                     'type': 'esriFieldTypeString',
                                                     'alias': 'Receiver Name',
                                                     'sqlType': 'sqlTypeOther',
                                                     'length': 50,
                                                     'nullable': True,
                                                     'editable': True,
                                                     'domain': None,
                                                     'defaultValue': None})

            # ESRIGNSS_LATITUDE
            latitudeField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_LATITUDE']

            if not latitudeField:
                gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_LATITUDE',
                                                     'type': 'esriFieldTypeDouble',
                                                     'alias': 'Latitude',
                                                     'sqlType': 'sqlTypeOther',
                                                     'nullable': True,
                                                     'editable': True,
                                                     'domain': None,
                                                     'defaultValue': None})

            # ESRIGNSS_LONGITUDE
            longitudeField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_LONGITUDE']

            if not longitudeField:
                gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_LONGITUDE',
                                                     'type': 'esriFieldTypeDouble',
                                                     'alias': 'Longitude',
                                                     'sqlType': 'sqlTypeOther',
                                                     'nullable': True,
                                                     'editable': True,
                                                     'domain': None,
                                                     'defaultValue': None})

            # ESRIGNSS_ALTITUDE
            altitudeField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_ALTITUDE']

            if not altitudeField:
                gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_ALTITUDE',
                                                     'type': 'esriFieldTypeDouble',
                                                     'alias': 'Altitude',
                                                     'sqlType': 'sqlTypeOther',
                                                     'nullable': True,
                                                     'editable': True,
                                                     'domain': None,
                                                     'defaultValue': None})

            # ESRIGNSS_H_RMS
            horizontalAccuracyField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_H_RMS']

            if not horizontalAccuracyField:
                gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_H_RMS',
                                                     'type': 'esriFieldTypeDouble',
                                                     'alias': 'Horizontal Accuracy (m)',
                                                     'sqlType': 'sqlTypeOther',
                                                     'nullable': True,
                                                     'editable': True,
                                                     'domain': None,
                                                     'defaultValue': None})
            # ESRIGNSS_V_RMS
            verticalAccuracyField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_V_RMS']

            if not verticalAccuracyField:
                gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_V_RMS',
                                                     'type': 'esriFieldTypeDouble',
                                                     'alias': 'Vertical Accuracy (m)',
                                                     'sqlType': 'sqlTypeOther',
                                                     'nullable': True,
                                                     'editable': True,
                                                     'domain': None,
                                                     'defaultValue': None})

            # ESRIGNSS_FIXDATETIME
            fixTimeField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_FIXDATETIME']

            if not fixTimeField:
                gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_FIXDATETIME',
                                                     'type': 'esriFieldTypeDate',
                                                     'alias': 'Fix Time',
                                                     'sqlType': 'sqlTypeOther',
                                                     'length': 0,
                                                     'nullable': True,
                                                     'editable': True,
                                                     'domain': None,
                                                     'defaultValue': None})

            # ESRIGNSS_FIXTYPE
            fixTypeField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_FIXTYPE']

            if fixTypeField:
                # Field does exist check if the domain is set.
                if fixTypeField[0]['domain'] == None:
                    if ([operation for operation in operations if operation == 'updateDefinition']):
                        operations.append('updateDefinition')

                    fixtypeFieldIndex = featureLayerFields.index(fixTypeField[0])
                    fixTypeDomain = {'type': 'codedValue',
                                     'name': 'ESRI_FIX_TYPE_DOMAIN',
                                     'codedValues': [{'name': 'Fix not valid',
                                                      'code': 0},
                                                     {'name': 'GPS', 'code': 1},
                                                     {'name': 'Differential GPS', 'code': 2},
                                                     {'name': 'RTK Fixed', 'code': 4},
                                                     {'name': 'RTK Float', 'code': 5}]}
                    featureLayerFields[fixtypeFieldIndex]['domain'] = fixTypeDomain

            else:
                gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_FIXTYPE',
                                                     'type': 'esriFieldTypeInteger',
                                                     'alias': 'Fix Type',
                                                     'sqlType': 'sqlTypeOther',
                                                     'nullable': True,
                                                     'editable': True,
                                                     'domain': {'type': 'codedValue',
                                                                'name': 'ESRI_FIX_TYPE_DOMAIN',
                                                                'codedValues': [
                                                                    {'name': 'Fix not valid', 'code': 0},
                                                                    {'name': 'GPS', 'code': 1},
                                                                    {'name': 'Differential GPS', 'code': 2},
                                                                    {'name': 'RTK Fixed', 'code': 4},
                                                                    {'name': 'RTK Float', 'code': 5}]},
                                                     'defaultValue': None})

            # ESRIGNSS_CORRECTIONAGE
            correctionAgeField = [field for field in featureLayerFields if
                                  field['name'] == 'ESRIGNSS_CORRECTIONAGE']

            if not correctionAgeField:
                gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_CORRECTIONAGE',
                                                     'type': 'esriFieldTypeDouble',
                                                     'alias': 'Correction Age',
                                                     'sqlType': 'sqlTypeOther',
                                                     'nullable': True,
                                                     'editable': True,
                                                     'domain': None,
                                                     'defaultValue': None})

            # ESRIGNSS_STATIONID
            stationIdField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_STATIONID']

            if not stationIdField:
                gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_STATIONID',
                                                     'type': 'esriFieldTypeInteger',
                                                     'alias': 'Station ID',
                                                     'sqlType': 'sqlTypeOther',
                                                     'nullable': True,
                                                     'editable': True,
                                                     'domain': None,
                                                     'defaultValue': None})

            # ESRIGNSS_NUMSATS
            numstatsField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_NUMSATS']

            if numstatsField:
                # Field does exist check if the domain is set.
                if numstatsField[0]['domain'] == None:
                    if ([operation for operation in operations if operation == 'updateDefinition']):
                        operations.append('updateDefinition')
                    numSatellitesFieldIndex = featureLayerFields.index(numstatsField[0])
                    numSatellitesDomain = {'type': 'range',
                                           'name': 'ESRI_NUM_SATS_DOMAIN',
                                           'range': [0, 99]}
                    featureLayerFields[numSatellitesFieldIndex]['domain'] = numSatellitesDomain

            else:
                gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_NUMSATS',
                                                     'type': 'esriFieldTypeInteger',
                                                     'alias': 'Number of Satellites',
                                                     'sqlType': 'sqlTypeOther',
                                                     'nullable': True,
                                                     'editable': True,
                                                     'domain': {'type': 'range',
                                                                'name': 'ESRI_NUM_SATS_DOMAIN',
                                                                'range': [0, 99]},
                                                     'defaultValue': None})

            # ESRIGNSS_PDOP
            pdopField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_PDOP']

            if not pdopField:
                gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_PDOP',
                                                     'type': 'esriFieldTypeDouble',
                                                     'alias': 'PDOP',
                                                     'sqlType': 'sqlTypeOther',
                                                     'nullable': True,
                                                     'editable': True,
                                                     'domain': None,
                                                     'defaultValue': None})

            # ESRIGNSS_HDOP
            hdopField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_HDOP']

            if not hdopField:
                gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_HDOP',
                                                     'type': 'esriFieldTypeDouble',
                                                     'alias': 'HDOP',
                                                     'sqlType': 'sqlTypeOther',
                                                     'nullable': True,
                                                     'editable': True,
                                                     'domain': None,
                                                     'defaultValue': None})

            # ESRIGNSS_VDOP
            vdopField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_VDOP']

            if not vdopField:
                gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_VDOP',
                                                     'type': 'esriFieldTypeDouble',
                                                     'alias': 'VDOP',
                                                     'sqlType': 'sqlTypeOther',
                                                     'nullable': True,
                                                     'editable': True,
                                                     'domain': None,
                                                     'defaultValue': None})
                
            # ESRIGNSS_DIRECTION
            directionField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_DIRECTION']

            if not directionField:
                gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_DIRECTION',
                                                     'type': 'esriFieldTypeDouble',
                                                     'alias': 'Direction of travel (°)',
                                                     'sqlType': 'sqlTypeOther',
                                                     'nullable': True,
                                                     'editable': True,
                                                     'domain': None,
                                                     'defaultValue': None})

            # ESRIGNSS_SPEED
            speedField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_SPEED']

            if not speedField:
                gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_SPEED',
                                                     'type': 'esriFieldTypeDouble',
                                                     'alias': 'Speed (km/h)',
                                                     'sqlType': 'sqlTypeOther',
                                                     'nullable': True,
                                                     'editable': True,
                                                     'domain': None,
                                                     'defaultValue': None})

            # ESRISNSR_AZIMUTH
            azimuthField = [field for field in featureLayerFields if field['name'] == 'ESRISNSR_AZIMUTH']

            if not azimuthField:
                gnssMetadataFields['fields'].append({'name': 'ESRISNSR_AZIMUTH',
                                                     'type': 'esriFieldTypeDouble',
                                                     'alias': 'Compass reading (°)',
                                                     'sqlType': 'sqlTypeOther',
                                                     'nullable': True,
                                                     'editable': True,
                                                     'domain': None,
                                                     'defaultValue': None})

            # ESRIGNSS_AVG_H_RMS
            averageHorizontalAccuracyField = [field for field in featureLayerFields if
                                              field['name'] == 'ESRIGNSS_AVG_H_RMS']

            if not averageHorizontalAccuracyField:
                gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_AVG_H_RMS',
                                                     'type': 'esriFieldTypeDouble',
                                                     'alias': 'Average Horizontal Accuracy (m)',
                                                     'sqlType': 'sqlTypeOther',
                                                     'nullable': True,
                                                     'editable': True,
                                                     'domain': None,
                                                     'defaultValue': None})

            # ESRIGNSS_AVG_V_RMS
            averageVerticalAccuracyField = [field for field in featureLayerFields if
                                            field['name'] == 'ESRIGNSS_AVG_V_RMS']

            if not averageVerticalAccuracyField:
                gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_AVG_V_RMS',
                                                     'type': 'esriFieldTypeDouble',
                                                     'alias': 'Average Vertical Accuracy (m)',
                                                     'sqlType': 'sqlTypeOther',
                                                     'nullable': True,
                                                     'editable': True,
                                                     'domain': None,
                                                     'defaultValue': None})

            # ESRIGNSS_AVG_POSITIONS
            averagePositionsField = [field for field in featureLayerFields if
                                     field['name'] == 'ESRIGNSS_AVG_POSITIONS']

            if not averagePositionsField:
                gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_AVG_POSITIONS',
                                                     'type': 'esriFieldTypeInteger',
                                                     'alias': 'Averaged Positions',
                                                     'sqlType': 'sqlTypeOther',
                                                     'nullable': True,
                                                     'editable': True,
                                                     'domain': None,
                                                     'defaultValue': None})

            # ESRIGNSS_H_STDDEV"
            standardDeviationField = [field for field in featureLayerFields if
                                      field['name'] == 'ESRIGNSS_H_STDDEV']

            if not standardDeviationField:
                gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_H_STDDEV',
                                                     'type': 'esriFieldTypeDouble',
                                                     'alias': 'Standard Deviation (m)',
                                                     'sqlType': 'sqlTypeOther',
                                                     'nullable': True,
                                                     'editable': True,
                                                     'domain': None,
                                                     'defaultValue': None})


                # Check if AddToDefinition operation needs to be added.
            initialFeatureLayerFieldsCount = len(featureLayerFields)
            if (len(gnssMetadataFields[
                        'fields']) + initialFeatureLayerFieldsCount) > initialFeatureLayerFieldsCount:
                operations.append('addToDefinition')

        else:
            operations.append('deleteFromDefinition')
            gnssMetadataFields = {
                'fields': [{'name': 'ESRIGNSS_DIRECTION'},
                           {'name': 'ESRIGNSS_SPEED'},
                           {'name': 'ESRISNSR_AZIMUTH'},
                           {'name': 'ESRIGNSS_POSITIONSOURCETYPE'},
                           {'name': 'ESRIGNSS_FIXDATETIME'},
                           {'name': 'ESRIGNSS_RECEIVER'},
                           {'name': 'ESRIGNSS_H_RMS'},
                           {'name': 'ESRIGNSS_V_RMS'},
                           {'name': 'ESRIGNSS_LATITUDE'},
                           {'name': 'ESRIGNSS_LONGITUDE'},
                           {'name': 'ESRIGNSS_ALTITUDE'},
                           {'name': 'ESRIGNSS_PDOP'},
                           {'name': 'ESRIGNSS_HDOP'},
                           {'name': 'ESRIGNSS_VDOP'},
                           {'name': 'ESRIGNSS_CORRECTIONAGE'},
                           {'name': 'ESRIGNSS_FIXTYPE'},
                           {'name': 'ESRIGNSS_STATIONID'},
                           {'name': 'ESRIGNSS_AVG_H_RMS'},
                           {'name': 'ESRIGNSS_AVG_V_RMS'},
                           {'name': 'ESRIGNSS_AVG_POSITIONS'},
                           {'name': 'ESRIGNSS_H_STDDEV'},
                           {'name': 'ESRIGNSS_NUMSATS'}]}

        # Add/Delete/Modify service definition.
        for operation in operations:

            # Add
            if operation == 'addToDefinition':
                response = featureLayerCollection.manager.layers[featureLayerIndex].add_to_definition(
                    gnssMetadataFields)
                arcpy.AddMessage("Successfully added GNSS fields..")

            # Delete
            elif operation == 'deleteFromDefinition':
                response = featureLayerCollection.manager.layers[featureLayerIndex].delete_from_definition(
                    gnssMetadataFields)


            # Modify
            else:
                response = featureLayerCollection.manager.layers[featureLayerIndex].update_definition(
                    featureLayerFields)
                arcpy.AddMessage("Successfully updated GNSS fields..")

            result = response['success']

            if not result:
                print('Failed to update Feature layer service definition..')
            else:
                print('Service definition updated successfully..')


    except Exception as e:
        arcpy.AddError(e)        


if __name__ == '__main__':
    args_parser = parseArguments()
    searchItems_addGNSSMetadataFields(args_parser)
