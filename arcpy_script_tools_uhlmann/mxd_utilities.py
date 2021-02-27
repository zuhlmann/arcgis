import arcpy
import os

class mxdAbstractions(object):
    def __init__(self, fp_mxd_or_string):
        '''
        fp_mxd_or_string        either a filepath of recognized string i.e. "CURRENT"
        '''
        self.mxd = arcpy.mapping.MapDocument(fp_mxd_or_string)
    def match_element_type(self, element_type):
        '''
        element_type        TEXT_ELEMENT, or anything from ListLayoutElements
        '''
        elements = arcpy.mapping.ListLayoutElements(self.mxd, element_type)
        self.elements = elements
        self.element_type = element_type
        # if using individually (not with dataframe) and want to dir()
        properties = [item for item in dir(elements[0]) if '_' not in item]
        temp_str = '{}_properties'.format(element_type.lower())
        setattr(self, temp_str, properties)

    def replace_and_export(self, target_list, replace_list, base_dir, fname_prepend):
        '''
        target_list           list of name of string of text element to match
        replace_list           list of text to replace in target_list
        base_di                 to ouptut new figures
        '''
        for elm in self.elements:
                for target_text, replace_text in zip(target_list, replace_list):
                    if elm.name == target_text:
                        # set element to property of class instance
                        attr_str = '{}_named_{}'.format(self.element_type.lower(), target_text)
                        setattr(self, attr_str, elm)
                        if target_text == 'figure_num':
                            replace_text = 'Figure {}'.format(replace_text)
                        elm.text = replace_text
                fname = '_'.join(replace_list).replace(' ', '_').replace('.','').replace('-','').lower() + '.pdf'
                fname = '{}_{}'.format(fname_prepend, fname)
                fp_mxd_out = os.path.join(base_dir, fname)
                arcpy.mapping.ExportToPDF(self.mxd, fp_mxd_out)
