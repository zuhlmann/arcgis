import arcpy

class mxdAbstractions(object):
    def __init__(self, fp_mxd_or_string):
        '''
        fp_mxd_or_string        either a filepath of recognized string i.e. "CURRENT"
        '''
        self.mxd = arcpy.mapping.MapDocument(fp_mxd_or_string)
    def match_layout_elements(self, element_type, target_str, **kwargs):
        '''
        element_type        TEXT_ELEMENT, or anything from ListLayoutElements
        target_str              string of text element to match
        '''
        elements = arcpy.mapping.ListLayoutElements(self.mxd, element_type)
        for elm in elements:
            if elm.name == target_str:
                try:
                    elm.text = kwargs['replace_text']
                except KeyError:
                    # if using individually (not with dataframe) and want to dir()
                    properties = [item for item in dir(elements[0]) if '_' not in item]
                    temp_str = '{}_properties'.format(element_type.lower())
                    setattr(self, temp_str, properties)
                    # set element to property of class instance
                    attr_str = '{}_named_{}'.format(element_type.lower(), target_str)
                    setattr(self, attr_str, elm)
