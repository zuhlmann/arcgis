import zipfile
import os
import pandas as pd
import numpy as np

#20230807

# A) UNZIP
# unzipping zip files with tiles of Tiff and accessories
# mccloud 20230804

dir_in = r'E:\box_offline\temp\script_devel\hillshade'
dir_in = r'E:\box_offline\projects\ringe\lidar\2016_lidar_tiles_full'
dir_in = r'E:\box_offline\temp\mth_home_AFT_tifs'

inv_name = 'tile_inventory'
file_ext = r'tif'
# remove period, since this will be passed as arg
if file_ext[0]=='.':
    file_ext = file_ext[1:]

#
#import zipfile
#for z in os.listdir(dir_in):
#    fname, ext = os.path.splitext(z)
#    if ext =='.zip':
#        dir_out = os.path.join(dir_in, fname)
#        fp_in = os.path.join(dir_in, z)
#        with zipfile.ZipFile(fp_in,"r") as zip_ref:
#            zip_ref.extractall(dir_out)
#    else:
#        pass
#        
## B) Create index file
## assumes that dir structure = path/to/main/deliv/tile<n>/tile<<n>.tif
tile_name_list, fp_tile_list = [],[]
for f in os.scandir(dir_in):
    if (f.is_dir()) & (f.name[-4]!='.zip'):
        tile_name = r'{}.{}'.format(f.name, file_ext)
        fp_tile_list.append(os.path.join(f.path, tile_name))
        tile_name_list.append(tile_name)
    elif f.name[-4:]=='.tif':
        fp_tile_list.append(f.path)
        tile_name_list.append(f.name)

# Create csv inventory for reference
df = pd.DataFrame(np.column_stack([tile_name_list,fp_tile_list]), 
                                    columns = ['file_name','file_path'])
df.to_csv(os.path.join(dir_in, '{}.csv'.format(inv_name)))
#
# C) create text file
big_str = '\n'.join(fp_tile_list)
with open(os.path.join(dir_in, '{}.txt'.format(inv_name)),'w') as txt:
    txt.write(big_str)

# D) gdal_tile











            
            