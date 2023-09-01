# A) Field Calculator.  
# River Miles were out of order, this populated with correct values
# from list2 and somehow sorted as well (?)
RMs = 'tolt_mainstem_kingCo_wtrcrs_SP_split'
layer = iface.activeLayer()
layer.startEditing()
features = layer.getFeatures()
list1 = list(range(1,9))
list2 = [8,5,3,4,0,1,2,6,7]
rm_order = dict(zip(list1,list2))
print(rm_order)
for ct, feature in enumerate(features):
    feature['river_mile']=list2[ct]
    layer.updateFeature(feature)
layer.commitChanges()