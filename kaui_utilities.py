import arcpy
import pandas as pd
import copy
import os

class props(object):
    def __init__(self):
    # paths_dict = {'working':0, 'reworked':1, 'project_features':2, 'scratch':3, 'diversions':4}
        props = ['working', 'reworked', 'project_features', 'scratch', 'diversions', 'dist_bdry_scratch']
        paths_list =  [r'C:\Users\uhlmann\Box\Projects\KIUC\West Kauai Energy Project\6.0 Phase 2 Design\6.0 Plans and Specs\6.6_GIS\GIS_files\Working',
        r'C:\Users\uhlmann\Box\Projects\KIUC\West Kauai Energy Project\6.0 Phase 2 Design\6.0 Plans and Specs\6.6_GIS\GIS_files\Working\kaui_reworked_data_202103.gdb',
        r'C:\Users\uhlmann\Box\Projects\KIUC\West Kauai Energy Project\6.0 Phase 2 Design\6.0 Plans and Specs\6.6_GIS\GIS_files\Working\Project_Features',
        r'C:\Users\uhlmann\Box\Projects\KIUC\West Kauai Energy Project\6.0 Phase 2 Design\6.0 Plans and Specs\6.6_GIS\GIS_files\Working\kaui_scratch.gdb\scratch_projected',
        r'C:\Users\uhlmann\Box\Projects\KIUC\West Kauai Energy Project\6.0 Phase 2 Design\6.0 Plans and Specs\6.6_GIS\GIS_files\Working\kaui_reworked_data_202103.gdb\diversions',
        r'C:\Users\uhlmann\Box\Projects\KIUC\West Kauai Energy Project\6.0 Phase 2 Design\6.0 Plans and Specs\6.6_GIS\GIS_files\Working\kaui_reworked_data_202103.gdb\disturbance_boundary_scratch']
        for prop, path in zip(props, paths_list):
            prop = 'fp_{}'.format(prop)
            setattr(self, prop, path)
        print('PROPERTIES:')
        print('\n'.join(props))
        print('fuck offs')
    def extract_cursor(self, fp_csv, feat_name_out):
        # add iff needed
        # arcpy.env.workspace = arc_env
        df = pd.read_csv(fp_csv)
        for i in range(len(df)):
            fp_feat = df.iloc[i].fp_feat
            field_name = df.iloc[i].field_name
            target_val = df.iloc[i].target_val
            print('FEATURE: {}\nFIELD NAME {} TARGET VAL {}'.format(fp_feat, field_name, target_val))
            # accumulate id fields in case multiple rows in one feature
            with arcpy.da.SearchCursor(fp_feat, [field_name, 'SHAPE@']) as cursor:
                for row in cursor:
                    if target_val in row:
                        # get shape field from tuple
                        print(dir(row[1]))
                        # initiate new feature
                        if 'shapes_union' not in locals():
                            shapes_union = copy.copy(row[1])
                            print('initiate shapes_union')
                        else:
                            shapes_union = shapes_union.union(row[1])
                            print('Perform union')
        arcpy.CopyFeatures_management(shapes_union, feat_name_out)

    def extract_cursor2(self, fcs_list, where_clause, fname):
        shapes = []
        for fc, where in zip(fcs_list, where_clause):
            for row in arcpy.da.SearchCursor(fc, ["SHAPE@"], where):
                shapes.append(row[0])
        merged_shape = shapes[0]
        for s in shapes[1:]:
            merged_shape = merged_shape.union(s)
        arcpy.CopyFeatures_management(merged_shape, fname)

    def buff_line_merge(self, fcs_list, buff_str_list, fp_fcs_out, gaps = True):
        arcpy.env.overwriteOutput = True
        fcs_out_memory_list = []
        for fc, buff_str in zip(fcs_list, buff_str_list):
            buff_str_formatted = buff_str.replace(' ', '_')
            buff_str_formatted = buff_str_formatted.replace('.', '_')
            buff_str_formatted = buff_str_formatted.lower()
            fcs_out_memory = os.path.join("in_memory", '{}_{}_buffer'.format(fc, buff_str_formatted))
            fcs_out_memory_list.append(fcs_out_memory)
            arcpy.Buffer_analysis(fc, fcs_out_memory, buff_str, '','',"ALL",'')
        # print('unioning these\n: {}'.format('\n'.join(fcs_out_memory_list)))
        # print('\n'.join(fcs_out_memory_list))
        if gaps:
            arcpy.Union_analysis(fcs_out_memory_list, fp_fcs_out)
        else:
            arcpy.Union_analysis(fcs_out_memory_list, fp_fcs_out,'','', False)




# # python window buffer stuff
# buff_str = ['2.5 Feet', '5 Feet']
# fp_name = ['moe_to_opae_access_rd_{}_buff'.format(str.replace('.','_')) for str in buff_str]
# fp_name = [fpn.replace(' ', '_') for fpn in fp_name]
# for name, buff in zip(fp_name, buff_str):
#     arcpy.Buffer_analysis("roads_appendum_mana",os.path.join(gdb_out, name), buff)
