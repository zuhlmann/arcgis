import arcpy
import pandas as pd
import copy

class props(object):
    def __init__(self):
    # paths_dict = {'working':0, 'reworked':1, 'project_features':2, 'scratch':3, 'diversions':4}
        props = ['working', 'reworked', 'project_features', 'scratch', 'diversions']
        paths_list =  [r'C:\Users\uhlmann\Box\Projects\KIUC\West Kauai Energy Project\6.0 Phase 2 Design\6.0 Plans and Specs\6.6_GIS\GIS_files\Working',
        r'C:\Users\uhlmann\Box\Projects\KIUC\West Kauai Energy Project\6.0 Phase 2 Design\6.0 Plans and Specs\6.6_GIS\GIS_files\Working\kaui_reworked_data_202103.gdb',
        r'C:\Users\uhlmann\Box\Projects\KIUC\West Kauai Energy Project\6.0 Phase 2 Design\6.0 Plans and Specs\6.6_GIS\GIS_files\Working\Project_Features',
        r'C:\Users\uhlmann\Box\Projects\KIUC\West Kauai Energy Project\6.0 Phase 2 Design\6.0 Plans and Specs\6.6_GIS\GIS_files\Working\kaui_scratch.gdb\scratch_projected',
        r'C:\Users\uhlmann\Box\Projects\KIUC\West Kauai Energy Project\6.0 Phase 2 Design\6.0 Plans and Specs\6.6_GIS\GIS_files\Working\kaui_reworked_data_202103.gdb\diversions']

        for prop, path in zip(props, paths_list):
            prop = 'fp_{}'.format(prop)
            setattr(self, prop, path)
        print('PROPERTIES:')
        print('\n'.join(props))
        print('fuck offs')
    # def extract_cursor(self, fp_csv, feat_name_out, arc_env):
    #     arcpy.env.workspace = arc_env
    #     df = pd.read_csv(fp_csv)
    #     for i in range(len(df)):
    #         fp_feat = df.iloc[i].fp_feat
    #         field_name = df.iloc[i].field_name
    #         target_val = df.iloc[i].target_val
    #         print('FEATURE: {}\nFIELD NAME {} TARGET VAL {}'.format(fp_feat, field_name, target_val))
    #         # accumulate id fields in case multiple rows in one feature
    #         with arcpy.da.SearchCursor(fp_feat, [field_name, 'SHAPE@']) as cursor:
    #             for row in cursor:
    #                 if target_val in row:
    #                     # get shape field from tuple
    #                     print(dir(row[1]))
    #                     # initiate new feature
    #                     if 'shapes_union' not in locals():
    #                         shapes_union = copy.copy(row[1])
    #                         print('initiate shapes_union')
    #                     else:
    #                         shapes_union = shapes_union.union(row[1])
    #                         print('Perform union')
    #     # arcpy.CopyFeatures_management(shapes_union, feat_name_out)


# # python window buffer stuff
# buff_str = ['2.5 Feet', '5 Feet']
# fp_name = ['moe_to_opae_access_rd_{}_buff'.format(str.replace('.','_')) for str in buff_str]
# fp_name = [fpn.replace(' ', '_') for fpn in fp_name]
# for name, buff in zip(fp_name, buff_str):
#     arcpy.Buffer_analysis("roads_appendum_mana",os.path.join(gdb_out, name), buff)
