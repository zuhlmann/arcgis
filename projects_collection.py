# # Used for projects - basically script calling random functions
# import compare_data
import os
import sys
# sys.path = [p for p in sys.path if '86' not in p]
# import arcpy
import utilities
import pandas as pd
import numpy as np

# file paths for Item Desciption
fp_aecom = 'C://Users//uhlmann//Box//GIS//Project_Based//Klamath_River_Renewal_MJA//GIS_Data//new_data_downloads//AECOM_dump//KlamathDamRemoval_Data_20200605//KlamathDamRemoval_Data_20200605.gdb'
fp_working = 'C://Users//uhlmann//Box//GIS//Project_Based//Klamath_River_Renewal_MJA//GIS_Data//McmJac_KRRP_GIS_data//working.gdb'
fp_orders = 'C://Users//uhlmann//Box//GIS//Project_Based//Klamath_River_Renewal_MJA//GIS_Data//McmJac_KRRP_GIS_data//orders.gdb'
fp_GIS_data = 'C://Users//uhlmann//Box//GIS//Project_Based//Klamath_River_Renewal_MJA//GIS_Data'
fp_request_mp = 'C://Users//uhlmann//Box//GIS//Project_Based//Klamath_River_Renewal_MJA//GIS_Request_Tracking//GIS_Requests_Management_Plans'
fp_agol = 'C://Users//uhlmann//Box//GIS//Project_Based//Klamath_River_Renewal_MJA//GIS_Data//AGOL_DataUploads'
fp_new_data_dl = 'C://Users//uhlmann//Box//GIS//Project_Based//Klamath_River_Renewal_MJA//GIS_Data//new_data_downloads//'

# # # 1) RAMP and Tributary Connectivity for Management Plans
# # # a)  Appendix D1.
# # # bullet 6. - below IG dam
# # (gnis_name = 'Bogus Creek') OR (gnis_name = 'Dry Creek') OR
# # (gnis_name = 'Little Bogus Creek') OR (gnis_name = 'Willow Creek') OR
# # (gnis_name = 'Cottonwood Creek')
# #
# # ('108313183', '108307517', '108313173', '165568594', '108303883', '108304215', '108306877', '165549459', '108304183', '165566523', '108313163', '108304175', '108312941', '108304243', '165568457', '108303975', '108304225', '165568235', '108307545', '108313291', '108303691', '108312891', '108313199', '165568927', '108313359', '108313089', '108306801', '108307449', '165568458', '108312815', '165561954', '108311369', '108304157', '165573121', '108312857', '108306951', '165557001', '108312889', '108311395', '108312841', '108313367', '165571773', '165568455', '165557022', '165568233', '108307493', '108311305', '165549458', '108312849', '108313259', '165568563', '165549457', '108306965', '108312939', '108313067', '108313387', '165568596', '108307491', '108303697', '108303963', '108313149', '108307489', '108304149', '108304199', '165566524', '108312223', '108313161', '108306535', '108313357', '108304077', '108304197', '165568452', '108311405', '108313071', '165567025', '108313159', '165573120', '108307477', '165568561', '108313379', '108313133', '108311337', '108313383', '108312229', '108313181', '108306901', '108311317', '108313169', '108306891', '108311313', '108304179', '108303685', '108311331', '108311323', '108307471', '108307431', '108307439', '108313405', '108312837', '108312861', '108313171', '108304191', '108312895', '165568459', '108303839', '108313363', '108307451', '108313145', '108304205', '108306869', '108313225', '108307445', '108312901', '108312803', '108312765', '108306945', '108304223', '165566521', '108313091', '108304211', '108312859', '108307537', '108306853', '108313153', '108307441', '108307447', '108312887', '108306925', '108312869', '108312853', '108303847', '165561979', '108311365', '108306837', '165568236', '108312883', '108312893', '108313355', '108306533', '108311393', '108303689', '108312919', '108307555', '108312805', '108313177', '165568451', '108313075', '108303909', '108312847', '108307495', '108312907', '108313269', '108306923', '108306947', '108311195', '165573761', '165571771', '108313279', '108311423', '108313167')
# #
# # # bullets 7 and 8 -JCB and between res
# # (gnis_name = 'Spencer Creek') OR (gnis_name = 'Shovel Creek')
# # # Spencer Creek and Shovel Creek
# # ('165562580', '165566896', '165545853', '108319197', '165568066', '165567909', '165549625', '165568070', '165567860', '165568069', '165567915', '165547612', '165562609', '165567859', '165546521', '108319173', '108319155', '165568067', '165549036', '165567918', '165567916', '165569912', '165548076', '165552635', '108319137', '165548075', '108319151', '108318961', '165569910', '108319149', '165546522', '108318963', '108319153', '165552636', '108319171', '108318965', '165568071', '165570401', '108319143', '165567857', '108319125', '165562616', '165567911', '165556914', '108316121', '108317431', '165568402', '165560265', '165572977', '108316111', '108317339', '108317463', '108317193', '165565931', '108317443', '165568407', '108317453', '108317317', '108317467', '108317455', '108317413', '108317389', '108316115', '108317435', '165566101', '165572976', '165555220', '165571680', '108317369', '165555221', '108317439', '108317395', '165568404', '108317307', '108316101', '165556941', '165566102', '108316133', '108316081', '165556815')
# #
# # # bullet 9 Beaver Creek from Copco rd to Klamath
# # # TO DO: clip to Copco Rd
# # (gnis_name = 'Beaver Creek')
# # ('108306557', '108306283', '108306291', '108306317', '108306281')
# #
# # # Bullet 10 Fall Creek 400 feet from Dagget to Klamath
# # # TO DO Clip Dagget
# # (gnis_name = 'Fall Creek')
# # ('108306393', '165565748')
# #
# # # Bullet 11 approximately 0.5 mi Jenny Cr from 500 feet upstream Copco to Klamath
# # # TO DO clip Copco
# # (gnis_name = 'Jenny Creek') OR (gnis_name = 'Camp Creek')
# # ('165550502', '165549188')
# #
# # # Bullet 12 1.25 miles from Camp-Dutch Creek complex Copco to Klamath
# # # manually selected river stretch
# # # TO DO Clip where intersecects klam
# # # KLAMATH   -->  gnis_id = '00266887'
# # # permanent_identifier IN ('165548957', '165550585', '108312505', '165548958', '108312499', '108312569', '165549566',  '108313351')
# # ('165548957', '165550585', '108312505', '165548958', '108312499', '108312569', '165549566', '108313351')
# #
# # # get ids
# # temp_lst = []
# # with arcpy.da.SearchCursor('NHD_intersect_project_clip', ['permanent_identifier']) as cursor:
# #     for row in cursor:
# #         temp_lst.append(row[0].append('utf8'))
#
# # Management Plans 9/20/20
# # 1) UPLOADING AECOM_DUMP
# # create the dataframe to copy into Item_List.csv
# # fp_gdb = 'C://Users//uhlmann//Box//GIS//Project_Based//Klamath_River_Renewal_MJA//GIS_Data//new_data_downloads//AECOM_dump//KlamathDamRemoval_Data_20200605//KlamathDamRemoval_Data_20200605.gdb'
# fp_out2 = 'C://Users//uhlmann//Box//GIS//Project_Based//Klamath_River_Renewal_MJA//GIS_Data//item_descriptions_append_aecomDump2.csv'
# # df = compare_data.file_paths_arc(fp_gdb, True)
# # pd.DataFrame.to_csv(df, fp_out2)
#
# # Add keys
# df = pd.read_csv(fp_out2)
# fp_out3 = 'C://Users//uhlmann//Box//GIS//Project_Based//Klamath_River_Renewal_MJA//GIS_Data//item_descriptions_append_aecomDump3.csv'
# col = df['dset'].values.tolist()
# col_tags = [dset + ', aecom_vector_gdb' for dset in col]
# df['tags'] = col_tags
# pd.DataFrame.to_csv(df, fp_out3)
#
# # ADD Sequential nums to field
# rec = 0
# def auto_incr():
#     global rec
#     global += 1
#     return(rec)
#
# # add names
# rec = 0
# def auto_incr():
#     global rec
#     list_names = ['JC Boyle', 'Klamath River OR N', 'Klamath River OR S', 'Copco 1','Copco 2', 'Iron Gate']
#     val = list_names[rec]
#     rec += 1
#     return(val)
#
# # Security digitizing
# idx = 0
# val_list = [45, 45, 50, 45, 45, 45, 50, 45, 50, 45, 45, 45]
# key_temp = {45:'Security Unmanned Pipe Gate', 50: 'Security Pipe Gate and Guard Shack'}
# def security_MP():
#   global idx
#   global val_list
#   global key_temp
#   point_type = key_temp[val_list[idx]]
#   idx += 1
#   return(point_type)

# # MANAGEMENT PLANS
# # Stream selections
# # use this to select from stream selection in WPT_MP - cut and paste in Python
# with arcpy.da.SearchCursor('Stream Selection', ['layer']) as cursor:
#     row = [row[0] for row in cursor]
# unique_vals = list(set(row))
# unique_vals.sort()
# unique_vals.reverse()
# for item in unique_vals:
#     print("label = '{}'".format(item))
#
# # CAMAS
# # select from fields
# # 1a) bats
#
fp_bats = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/McmJac_KRRP_GIS_data/working.gdb/MP_Camas/Bat_Roosts_Active_2019'
fp_out_csv = os.path.join(fp_request_mp, 'Camas_MPs\\Bat_Roosts_Active.csv')
# fp_aecom = 'C://Users//uhlmann//Box//GIS//Project_Based//Klamath_River_Renewal_MJA//GIS_Data//new_data_downloads//AECOM_dump//KlamathDamRemoval_Data_20200605//KlamathDamRemoval_Data_20200605.gdb'
# fp_wpt = os.path.join(fp_aecom, 'Biology_CDM_RDG//WPT_Historical_Habitat')
# fp_access = os.path.join(fp_working, 'Project_Data\\Access_Routes\\')
# utilities.feature_table_as_csv(fp_bats, fp_out_csv, ['label'])
# where_clause_list = ["(label='{}')".format(item) for item in road_list]
# where_clause = 'OR'.join(where_clause_list)
#
# # 1b) Camas MP: Select willow fly catcher habitat
# # use this to select from stream selection in WPT_MP - cut and paste in Python
#
# # fp_klam_river_veg_com = 'C://Users//uhlmann//Box//GIS//Project_Based//Klamath_River_Renewal_MJA//GIS_Data//new_data_downloads//AECOM_dump//KlamathDamRemoval_Data_20200605//KlamathDamRemoval_Data_20200605.gdb//Biology_CDM_RDG//Klamath_River_Vegetation_Communities'
# # vals_select = ['Bigleaf maple forest', 'Geyser willow thicket', 'Oregon ash grove', 'Shining willow grove', 'Sandbar willow thicket', 'Willow thickets']
# # where_clause_wfc = utilities.where_clause_create_p1('Alliance_Name', vals_select)
# # where_clause_wfc = ' OR '.join(where_clause_wfc)
# fp_out = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Data/McmJac_KRRP_GIS_data/working.gdb/MP_Camas'
# # arcpy.FeatureClassToFeatureClass_conversion(fp_klam_river_veg_com, fp_out, 'WFC_habitat', where_clause_wfc)
# arcpy.FeatureClassToFeatureClass_conversion(fp_wpt, fp_out, 'WPT_Historical_Habitat')

# # # 2) CREATE SQL for labels
# df = pd.read_csv(fp_out_csv)
# objectid = df.loc[df.mp_select=='y']['OBJECTID'].tolist()
# field = 'OBJECTID'
# where_clause_list = ["({0}={1})".format(field, val) for val in objectid]
# where_clause = 'OR'.join(where_clause_list)
# print(where_clause)

# # 3) FEASABILITY RFP for Olivia Mahoney 10/7/20
# #  Create attribute csv from recreation <pts and poly>
# fp_rec_poly = os.path.join(fp_aecom, 'Land_use//Recreational_Areas_Points')
# fp_out = os.path.join(fp_GIS_data, 'compare_vers//attribute_field_contents//Recreation/Recreation_Areas_Points.csv')
# field = ['objectid', 'rec_nm', 'fac_status_ref', 'rec_pt_use_ref']
# df = utilities.list_unique_fields(fp_rec_poly, field, 'in_memory', name = 'rec_points')
# pd.DataFrame.to_csv(df, fp_out)

# # plug into interpreter
# # object IDs from Recreation_Areas_<poly or point> from aecom_dump
# poly_objectid = [14, 27, 46,50,54,61,62, 63, 30]
# point_objectid = [3, 19, 530]
# select_poly = ['(objectid={})'.format(objid) for objid in poly_objectid]
# select_string_poly = 'OR'.join(select_poly)
# print(select_string_poly)
# select_point = ['(objectid={})'.format(objid) for objid in point_objectid]
# select_string_point = 'OR'.join(select_point)
# print(select_string_point)
#
# # change list
# inc = 0
# key_list = ['New Sites','Modify', 'No Changes']
# replace_field_list = [1,2,2,2,0,0,0]
# def incr_list():
#   global inc
#   global key_list
#   global replace_field_list
#   status = key_list[replace_field_list[inc]]
#   inc += 1
#   return(status)

# # indices
# idx = 0
# def incr():
#   global idx
#   page_num = [1,2,5,6,4,3,7,8]
#   page_name = ['JC Boyle', 'Klamath R.', 'Klamath R.', 'Klamath R.', 'Copco 1', 'Copco 1 & 2', 'Iron Gate', 'Klamath R.']
#   num = page_name[page_num[idx]-1]
#   idx += 1
#   return(num)
#
# # Symbols
# fp_routes = 'C://Users//uhlmann//Box//GIS//Project_Based//Klamath_River_Renewal_MJA//GIS_Data//compare_vers//attribute_field_contents//Access_Routs_MP//Access_Routes_label.csv'
# df = pd.read_csv(fp_routes)

# # making maps
# fp_request = 'C://Users//uhlmann//Box//GIS//Project_Based//Klamath_River_Renewal_MJA//GIS_Request_Tracking'
# fp_map = os.path.join(fp_request, 'GIS_Requests_KRRC//Feasibility_RFP.mxd')
# print(fp_map)
# mxd_doc = arcpy.mapping.MapDocument(fp_map)
# ddp = mxd_doc.dataDrivenPages
# pages = '1-2'
# fp_pdf = fp_map = os.path.join(fp_request, 'GIS_Requests_KRRC//Feasibility_RFP.pdf')
# ddp.exportToPDF(fp_pdf, 'RANGE', pages)

# # WPT
# # file path to data gis
# fp_in = os.path.join(fp_working, 'MP_Camas//WPT_indices_final')
# fp_camas_MP = os.path.join(fp_working, 'MP_Camas')
# arcpy.FeatureClassToFeatureClass_conversion(fp_in, fp_camas_MP, 'WPT_habitat_OR_indices')

# # 5) mxd INVENTORIES
# # file path to mxds

# # 5a) Camas
# # inventories for Camas
# fp_camas_requests = os.path.join(fp_request_mp, 'Camas_MPs')
# mxd_list_camas = ['GBH Colony.mxd', \
#             'Spotted Owl.mxd', 'Swallows_v2_MP.mxd', 'Wetland Buffer.mxd', \
#             'WFC_MP.mxd', 'WPT Habitat_MP_v2_CA.mxd', 'WPT Habitat_MP_v2_OR.mxd', \
#             'WPT_Relocation_MP_8_5_11_final.mxd', 'Special_Status_Plants.mxd']
# fp_mxds_camas = [os.path.join(fp_camas_requests, mxd) for mxd in mxd_list_camas]
# fig_names = ['GBH_Colony_MP_draft2', 'Spotted_Owl_MP_draft1', 'Swallows_v2_MP_draft2', \
#             'wetland_buffer_<reservoir_name>_MP_draft1', \
#             'WFC_MP_draft1', 'WPT Habitat_MP_v2_CA', 'WPT Habitat_MP_v2_OR', \
#             'WPT_Relocation_MP_8_5_11', 'special_status_plants_MP_draft1']
# fig_names_camas = [fig_name + '.pdf' for fig_name in fig_names]
#
# # path to inventory lists for easy functionality
# fp_dict = {'camas': 'C://Users//uhlmann//Box//GIS//Project_Based//Klamath_River_Renewal_MJA' \
#                     '//GIS_Request_Tracking//GIS_Requests_Management_Plans//Camas_MPs//' \
#                     'figure_inventory_camas_MP.csv'}

# # 5b) KP
# # inventories for KP
# fp_kp_requests = os.path.join(fp_request_mp, 'KnightPiesold_MPs')
#
# mxd_list_kp = ['Security_MP_KP_v2.mxd', 'Access_MP_KP_v2.mxd', 'Security_Overview_MP_KP.mxd']
# fp_mxds_kp = [os.path.join(fp_kp_requests, mxd) for mxd in mxd_list_kp]
# fig_names_kp = ['Security_MP_KP_v2.pdf', 'Access_MP_KP_v2.pdf', 'Security_Overview_MP_KP_v2.pdf']

# # GENERAL
# # Provide specific variables for respective MP
# idx = [3, -1]
#
# mxd_list = [mxd_list_camas[id] for id in idx]
# fig_names = [fig_names_camas[id] for id in idx]
# fp_mxds = [fp_mxds_camas[id] for id in idx]
# fp_MP_base = fp_camas_requests
# current_date = [datetime.datetime.today().strftime('%B %d %Y')] * len(fig_names)
# MP_prepend = 'camas2'
#
#
# fp_out = os.path.join(fp_camas_requests, 'figure_inventory_{}_MP.csv'.format(MP_prepend))
# # if path exists, keep adding
# if os.path.exists(fp_out):
#     df = pd.read_csv(fp_out, index_col = 'figure_names')
#     for fp_mxd, fig_name in zip(fp_mxds, fig_names):
#         df.loc[fig_name]
# else:
#     df = pd.DataFrame(np.column_stack([fig_names, mxd_list, fp_mxds, current_date]),
#                         columns = ['fig_name''mxd_filename', 'fp_mxd', 'current_date'])
#     pd.DataFrame.to_csv(df, fp_out)
# for fp_mxd, fig_name in zip(fp_mxds, fig_names):
#     utilities.mxd_inventory(fp_mxd, fig_name, fp_MP_base)

# # 5c) One file inventory - KRRC Feasibility
# fp_krrc_requests = 'C://Users//uhlmann//Box//GIS//Project_Based//Klamath_River_Renewal_MJA//GIS_Request_Tracking//GIS_Requests_KRRC'
# krrc_mxd = os.path.join(fp_krrc_requests, 'Feasibility_RFP.mxd')
# krrc_pdf = os.path.join(fp_krrc_requests, 'Feasibility_RFP_v2')
# utilities.mxd_inventory(krrc_mxd, krrc_pdf, fp_krrc_requests)


# 6) Merge multiple files
# Juvenile Salmanoid
# attrocious folder setup.  within p12 are gdbs one or two per loc
fp_salmon = os.path.join(fp_new_data_dl, 'juvenille_salmamoid_RES_MP//p12')
# then a feature database
fp_salmon = [os.path.join(fp_salmon, gdb, 'Placemarks') for gdb in os.listdir(fp_salmon)]
monitoring_point_list = []
poly_list = []
line_list = []
loc_list = []
for loc in fp_salmon:
    walk = arcpy.da.Walk(loc)
    for fp, _, feat_name in walk:
        if 'monitoring_area' in fp:
            # # normalize for operating system
            # fp_norm = os.path.normpath(fp)
            # # split by os separatory
            # fp_norm_components = loc_name.split(os.sep)
            # # get gdb base name
            # loc_name = [component[:-3] for component in fp_norm_components if 'gdb' in component]
            # loc_list.append(loc_name)
            # if 'Points' in feat_name:
            #     point_list.append(os.path.join(fp, 'Points'))
            if 'Polygons' in feat_name:
                poly_list.append(os.path.join(fp, 'Polygons'))
            # if 'Polylines' in feat_name:
            #     line_list.append(os.path.join(fp, 'Polylines'))
fp_merged_pts = os.path.join(fp_working, 'monitoring_areas_poly_salmanoid_MP')
arcpy.Merge_management(poly_list, fp_merged_pts)


# COMMAND LINE TRICKS
# reload
# utilities = imp.load_source('utilities', 'C:/Users/uhlmann/code/utilities.py')
    
