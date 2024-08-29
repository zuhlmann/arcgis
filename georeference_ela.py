from osgeo import gdal
import xml.etree.ElementTree as ET
import sys
sys.path.append('c:/users/uhlmann/code')
import raster_from_array
import numpy as np
import pandas as pd

# 1) CREATE INVENTORY or UPDATE INV
csv = r'C:\Box\MCM Projects\Mainspring Conservation Trust\24-092 Ela Dam Removal PDB\4.0 Data Collection\Aerials\ela_imagery_inventory.csv'
# csv_out = r'C:\Box\MCM Projects\Mainspring Conservation Trust\24-092 Ela Dam Removal PDB\4.0 Data Collection\Aerials\data_inv.csv'
df = pd.read_csv(csv)
idx = df[df['complete']==False].index

create=False
n, s, e, w = [], [], [], []
pub_date_list = []
for xml in df.loc[idx,'xml_path']:
    print(xml)
    tree = ET.parse(xml)
    root = tree.getroot()
    idinfo = root.find('idinfo')
    t1 = idinfo.find('citation')
    t2 = t1.find('citeinfo')
    pub_date = t2.find('pubdate')
    pub_date = pub_date.text
    spdom = idinfo.find('spdom')
    for x in spdom.findall('bounding'):
        west = x.find('westbc')
        north =  x.find('northbc')
        east = x.find('eastbc')
        south = x.find('southbc')
        w.append(west.text)
        n.append(north.text)
        e.append(east.text)
        s.append(south.text)
    pub_date_list.append(pub_date)
# if create:
#     col_names = ['xml_path','west','north','east','south']
#     cols = np.column_stack([xml_list,w,n,e,s])
#     df = pd.DataFrame(cols,columns=col_names)
#     df.to_csv(csv_out)
# else:
#     df.loc[idx, 'west']=w
#     df.loc[idx, 'north']=n
#     df.loc[idx, 'east']=e
#     df.loc[idx, 'south']=s
# df.to_csv(csv_out)

# # 2) TRANSLATE (Georeference)
# df = pd.read_csv(csv)
# idx = df[df['complete']==False].index
# dir_out = r"C:\Box\MCM Projects\Mainspring Conservation Trust\24-092 Ela Dam Removal PDB\4.0 Data Collection\Aerials\nir\processed"
# idx_list, fp_georeferenced_list=[],[]
# for idx, row in df.iterrows():
#     # ot = 'GTiff'
#     ot = 'GTiff'
#     ext = {'GTiff':'tif','JPEG':'jpg'}
#     ext = ext[ot]
#     if not row['complete']:
#         bounds = [row['west'],row['north'],row['east'],row['south']]
#         options_translate = gdal.TranslateOptions(format=ot, outputBounds=bounds)
#
#         path_tif = row['associated_tif']
#         fname_orig = os.path.split(path_tif)[-1]
#         fname = r'{}_georeferenced.tif'.format(fname_orig[:-4])
#         tgt_dset = os.path.join(dir_out, fname)
#
#         print(tgt_dset)
#         print(path_tif)
#         # gdal.Warp(tgt_dset, src_dset, options = options)
#         gdal.Translate(tgt_dset, path_tif, options = options_translate)
#         idx_list.append(idx)
#         fp_georeferenced_list.append(tgt_dset)
# df.iloc[idx_list,df.columns.get_loc('fp_georeferenced')]=fp_georeferenced_list
# df.to_csv(csv)
#
# # 3) ROTATE

def rotate_90(fp_orig, fp_out, rotation):
    dict_rot={90:1,180:2,270:3}
    try:
        num_rot = dict_rot[rotation]
    except KeyError:
        print('passed incorrect rotation value, used default of 270')
        num_rot=3
    ds1 = gdal.Open(fp_orig)
    arr_orig = ds1.ReadAsArray()
    if num_rot==1:
        arr_new = np.rot90(arr_orig)
    elif num_rot==2:
        arr_new = np.rot90(np.rot90(arr_orig))
    elif num_rot==3:
        arr_new = np.rot90(np.rot90(np.rot90(arr_orig)))
    gt = ds1.GetGeoTransform()
    ul = (gt[0], gt[3])
    res = [gt[1], gt[5]]
    nd = 0
    gdal_dtype = gdal.GDT_Float32
    wkid = 4326
    driver='GTiff'
    raster_from_array.numpy_array_to_raster(fp_out,
                              arr_new,
                              ul,
                              res,
                              nband = 1,
                              no_data = nd,
                              gdal_data_type = gdal_dtype,
                              spatial_reference_system_wkid = wkid,
                              driver = driver)

# df = pd.read_csv(csv)
# dir_out = r"C:\Box\MCM Projects\Mainspring Conservation Trust\24-092 Ela Dam Removal PDB\4.0 Data Collection\Aerials\nir\processed"
# fp_out_list =[]
# idx_list = []
# for idx, row in df.iterrows():
#     if not row['complete']:
#         fp_orig = row['fp_georeferenced']
#         fname_orig = os.path.split(fp_orig)[-1]
#         fname = r'{}_rotated.tif'.format(fname_orig[:-4])
#         fp_out = os.path.join(dir_out, fname)
#         rotate_90(fp_orig,fp_out, row['rotation'])
#         fp_out_list.append(fp_out)
#         idx_list.append(idx)
#
# df.iloc[idx_list,df.columns.get_loc('fp_rotated')]=fp_out_list
# df.to_csv(csv)

