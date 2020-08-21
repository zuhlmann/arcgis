import spyder_arcgis_oop as agolZ
#
# # 1) Basic upload
# # INITIATE
# agol_obj = agolZ.AgolAccess('something')
#
# # # GROUP
# # agol_obj.get_group('krrp_geospatial')
# # print(agol_obj.krrp_geospatial)
#
# # # SEARCH FILES ONLINE
# # itemType = 'shapefile'
# # agol_obj.identify_items_online(itemType, tags = 'eagles')
# # print(agol_obj.user_content_eagles_shapefile)
#
# # zip_test = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Data\\AGOL_DataUploads\\2020_08_13\\2020_08_13'
# # agol_obj.zip_agol_upload(zip_test)
#
# # select by tags
# agol_obj.selection_idx(target_tag = ['eagles', 'test'])
# print(agol_obj.indices)
#
# # # select by indices
# # agol_obj.selection_idx(indices = [1,2,3,5,9,21])
# # print(agol_obj.indices)
#
# # publish
# snip = 'testing if my class works'
# agol_obj.add_agol_upload(snippets = snip)

# 2) Example of adding new metadata
# agol_obj = agolZ.metaData()
agol_obj = agolZ.AgolAccess('something')
# agol_obj.selection_idx(indices = [21,22])
# # agol_obj.zip_agol_upload()
# snips = ['FERC boundaries from 2017.  Still valid as of Aug 2020. However will' +
#         'be edited soon', 'Limit of Work 60Design for KRRP']
# agol_obj.add_agol_upload(snippets = snips)
agol_obj.email_group()



# # 3) testing oop
# import testClass as oop
# object1 = oop.inheritanceClass()
# print('my name is {} my bday is {}'.format(object1.name, object1.bday))
# print(object1.square(5))
