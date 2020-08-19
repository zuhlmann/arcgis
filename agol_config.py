import spyder_arcgis_oop as agolZ

# INITIATE
agol_obj = agolZ.AgolAccess('something')

# # GROUP
# agol_obj.get_group('krrp_geospatial')
# print(agol_obj.krrp_geospatial)

# # SEARCH FILES ONLINE
# itemType = 'shapefile'
# agol_obj.identify_items_online(itemType, tags = 'eagles')
# print(agol_obj.user_content_eagles_shapefile)

# zip_test = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Data\\AGOL_DataUploads\\2020_08_13\\2020_08_13'
# agol_obj.zip_agol_upload(zip_test)

# select by tags
agol_obj.selection_idx(target_tag = ['eagles', 'test'])
print(agol_obj.indices)

# # select by indices
# agol_obj.selection_idx(indices = [1,2,3,5,9,21])
# print(agol_obj.indices)

# publish
snip = 'testing if my class works'
agol_obj.add_agol_upload(snippets = snip)


This shapefile represents the proposed FERC Project Boundary for the Lower Klamath Project as shown in the Transfer Application.The boundary is composed of the Federal Energy Regulatory Commision (FERC) approved boundaries for JC Boyle, Copco, and Iron Gate developments of the Klamath Hydroelectric Project.