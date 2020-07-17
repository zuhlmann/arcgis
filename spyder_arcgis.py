# play around with spyder, arcgis package, etc.
# ZRU 7/13/20

from arcgis.gis import GIS
from arcgis.gis import Group

gis = GIS(username = 'uhlmann@mcmjac.com', password = 'Gebretekle24!')
print('Connected to {} as {}'.format(gis.properties.portalHostname, gis.users.me.username))
# query_str = 'owner:'.format(gis.users.me.username)
# my_content = gis.content.search(query = query_str, item_type = 'shapefile', max_items = 15)
# to get group info use group id from html 'html?id-<HERE IS ID #>'
krrp_geospatial = Group(gis, 'a6384c0909384a43bfd91f5d9723912b')
# print content
krrp_geospatial.content()
