from test_delete import test_feat_methods
from utilities import *

fp_in = get_path('fp_translines_2019_11_reclassified')
test_feat_methods(fp_in)
feat_lyr = ['layer_make_feature', 'in_memory/in_memory_feature']
for lyr in feat_lyr:
    print('')
    print('From {}'.format(lyr))
    with arcpy.da.SearchCursor(lyr, ['layer_camas']) as cursor:
        row = [row[0] for row in cursor]
        print(row)
