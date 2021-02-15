import arcpy

class mxdAbstractions(object):
    def __init__(self, fp_mxd_or_string):
        '''
        fp_mxd_or_string        either a filepath of recognized string i.e. "CURRENT"
        '''
        self.mxd = arcpy.mapping.MapDocument(fp_mxd_or_string)
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
