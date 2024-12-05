import pandas as pd

# A) Field Calculator.
# River Miles were out of order, this populated with correct values
# from list2 and somehow sorted as well (?)

# # TOLT RMs
# RMs = 'tolt_mainstem_kingCo_wtrcrs_SP_split'
# layer = iface.activeLayer()
# layer.startEditing()
# features = layer.getFeatures()
# list1 = list(range(1,9))
# list2 = [8,5,3,4,0,1,2,6,7]
# rm_order = dict(zip(list1,list2))
# print(rm_order)
# for ct, feature in enumerate(features):
#     feature['river_mile']=list2[ct]
#     layer.updateFeature(feature)
# layer.commitChanges()

#WALLOWA sheet num
layer_name = 'wallowa_indices_v2'
layer = QgsProject.instance().mapLayersByName(layer_name)[0]
layer.startEditing()
features = layer.getFeatures()
csv = r"C:\Box\MCMGIS\Project_Based\Wallowa_Dam\gis_data\wallowa_inundation_indices2.csv"
df = pd.read_csv(csv,index_col='row_num')
for ct, feature in enumerate(features):
    feature['rotation']=int(df.loc[feature['row_num'],'rotation'])
    layer.updateFeature(feature)
layer.commitChanges()
