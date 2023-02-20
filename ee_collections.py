#import ee
#from ee_plugin import Map

# FOLLOW TUTORIAL HERE
# https://www.youtube.com/watch?v=hJuUU-hqLqg&t=452s

#aoi = ee.Geometry.Point([-117.25,48.75])
#
#Map.addLayer(aoi, {'color':'red'}, 'AOI')

collection = ee.ImageCollection('LANDSAT/LC09/C02/T1_L2')\
.filterBounds(aoi)\
.filterDate('2022-05-01','2022-08-15')\
.filterMetadata('CLOUD_COVER','less_than',5)\
#.first()

#def applyScaleFactors(image):
#  opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2)
#  thermalBand = image.select('ST_B.*').multiply(0.00341802).add(149.0)
#  return(image.addBands(srcImg = opticalBands, overwrite = True) \
#                .addBands(srcImg = thermalBand, overwrite = True))
                
#collection = collection.map(applyScaleFactors) 

#collection = collection.first()
              
              
#print('Total Images:', collection.size().getInfo())
#print(dir(collection))

#style = {
#    'bands': ['SR_B4', 'SR_B3', 'SR_B2'],
#    'min': 0.0,
#    'max': 0.5
#}
#
#Map.addLayer(collection, style, 'Landsat_19_scaled')

print(collection.getInfo())
