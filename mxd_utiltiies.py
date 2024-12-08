import arcpy
import re

def match_layout_elements(self, element_property, target_str):
    '''
    element_property        TEXT_ELEMENT, or anything from ListLayoutElements
    target_str              string of text element to match
    '''
    elements = arcpy.mapping.MapDocument.ListLayoutElements(self.mxd, element_property)
    for elm in elements:
        if elm.element_property == target_str:
            attr_str = '{}_matched_{}'.format(element_property, target_str)
            setattr(self, attr_str, elm)

def getMXDVersion(mxdFile):
    # https://gis.stackexchange.com/questions/62090/using-arcpy-to-determine-arcmap-document-version
    # Loop through mxds in folder and print mxd version number
    # 20241022
    matchPattern = re.compile("9.2|9.3|10.0|10.1|10.2|10.3|10.4|10.5|10.6|10.7|10.8")
    with open(mxdFile, 'rb') as mxd:
        fileContents = mxd.read().decode('latin1')[1000:4500]
        removedChars = [x for x in fileContents if x not in [u'\xff', u'\x00', u'\x01', u'\t']]
        joinedChars = ''.join(removedChars)
        regexMatch = re.findall(matchPattern, joinedChars)
        if len(regexMatch) > 0:
            version = regexMatch[0]
            return version
        else:
            return 'version could not be determined for ' + mxdFile