mcmjac_gis = GIS(username = 'uhlmann@mcmjac.com', password = 'Gebretekle24!')
print('Connected to {} as {}'.format(mcmjac_gis.properties.portalHostname, mcmjac_gis.users.me.username))
# # query_str = 'owner:'.format(gis.users.me.username)
# # my_content = gis.content.search(query = query_str, item_type = 'shapefile', max_items = 15)
# to get group info use group id from html 'html?id-<HERE IS ID #>'
krrp_geospatial = Group(mcmjac_gis, 'a6384c0909384a43bfd91f5d9723912b')
# fc_item.share(groups = 'a6384c0909384a43bfd91f5d9723912b')
print('ct = {} \\n fc_item {} '.format(idx, fc_item))
