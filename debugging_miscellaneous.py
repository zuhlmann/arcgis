#  DETERMINE mxd version
# https://gis.stackexchange.com/questions/62090/using-arcpy-to-determine-arcmap-document-version
import os
import glob
import sys
sys.path.append('c:/Users/uhlmann/code')
import utilities

# ESRI  ---> set python exe (ctl Alt S; settings, find in list)
# # 1_esri) GET ARC VERSION for mxd
# 20241022
# import mxd_utiltiies
# folder = r'C:\Users\UhlmannZachary\Documents\staging\testing'
# mxdFiles = glob.glob(os.path.join(folder, '*.mxd'))
# for mxdFile in mxdFiles:
#     fileName = os.path.basename(mxdFile)
#     version = mxd_utiltiies.getMXDVersion(mxdFile)
#     print(version, fileName)

# # 2_esri) INVENTORY MXD
# # 20241022
# base_dir=r'C:\Box\MCMGIS\Project_Based\Nuyakuk_Hydro\Maps\ISR_Maps'
# utilities.mxd_inventory_csv(base_dir, 'ISR_mxd_layer_inv.csv')

# Inventory Dir
# INVENTORY DIRECTORY
# 20240722
# from cowlitz_dbase notebook
sys.path.append('c:/users/uhlmann/code')
import importlib
import utilities_oop
importlib.reload(sys.modules['utilities'])
importlib.reload(sys.modules['utilities_oop'])
import pandas as pd
import copy

# tc = 'DATA_LOCATION_MCMILLEN'
# parent_dir = r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\map_documents"
# csv_lyt_inv = r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\map_documents\map_documents_aprx_inv.csv"
# subdir_inv_obj = utilities_oop.utilities(parent_dir, tc)

# # a) no filetype filter
# subdir_inv_obj.subdir_inventory(new_inventory = csv_lyt_inv)

# # b) filetype fileter
# ft_filt = ['.gdb','.cpg','.dbf','.idx','.shx','.xml','.shp','.ipynb']
# exclude_sd = ['aprx_inventories','archive','backups']
# subdir_inv_obj.subdir_inventory(ft_filt, exclude_sd, new_inventory = csv_lyt_inv)

# # b2) filter filetype
# projects = ['geosyntec_pad_H20_p2', 'recreation_PAD_p2','SFT_common_maps','terrrestrial_PAD']
# subdir = r'C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\sharepoint\templates\SCL_data_package_devel\map_documents\{}\{}'
# project_dir = [r'Index', r'GpMessages']
# exclude_sd = [os.path.normpath(subdir.format(pn, prd)) for pn in projects for prd in project_dir]
# exclude_sd.append(r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\sharepoint\templates\SCL_data_package_devel\map_documents\backups")
# subdir_inv_obj.subdir_inventory(ft_filt, exclude_sd, new_inventory = csv_lyt_inv)

# # Klamath Buoys ADD search_str
# buoy_str = [f"buoy_{v}" for v in list(range(14))]
# buoy_str2 = [f"buoy{v}" for v in list(range(14))]
# buoy_str.extend(buoy_str2)
# df = pd.read_csv(csv_lyt_inv)
# df['BUOY'] = df['BUOY'].astype(str)
# for idx in df.index:
#     for buoy in buoy_str:
#         if buoy in df.loc[idx, 'ITEM']:
#             t = copy.copy(buoy)
#             t = t.replace('buoy_','').replace('buoy','')
#             df.at[idx, 'BUOY'] = t
# df.to_csv(csv_lyt_inv)

# # Klamath Buoys cont..
# # 20241022 Aggregate Rows
# df = pd.read_csv(csv_lyt_inv)
# csv_folders = r'C:\Box\MCM Projects\Klamath River Renewal Corp\4.0 Data Collection\Crescent City Harbor Data\Unzipped Files\unzipped_folders_buoyID.csv'
# subdir_inv_obj.aggregate_rows(csv_lyt_inv, csv_folders, 'FINAL_SUBDIR', 'BUOY', data_type='integer')

# # ela_dam
# # 20241113
# import sys
# sys.path.append('c:/users/uhlmann/code')
# import spyder_arcgis_oop as agolZ
# import importlib
# importlib.reload(sys.modules['spyder_arcgis_oop'])
# pro_obj = agolZ.proProject()
# csv=r"C:\Box\MCM Projects\Mainspring Conservation Trust\24-092 Ela Dam Removal PDB\6.0 Plans and Specs\6.6_GIS\gis_requests\20241112_survey_parcels\Ela_XSections_Endpoints_joined_v3.csv"
# df=pd.read_csv(csv)
#
# keep_fld = ['OBJECTID_12', 'Shape', 'StreamOrd', 'TYPE', 'Reach', 'OBJECTID', 'Join_Count',
#               'TARGET_FID', 'OBJECTID_1', 'PIN', 'FCODE', 'DEED_ACRE', 'DATE_OF_ED', 'TYPE_OF_ED',
#               'COMMENTS', 'PARCEL_ID', 'PIN_Lease', 'SubName', 'LotNumb', 'PlatRefere', 'ParcelNumb',
#               'AccountNum', 'Name1', 'Name2', 'Address1', 'Address2', 'City', 'State', 'ZipCode',
#               'TownshipCo', 'Improvemen', 'ParcelBuil', 'ParcelObxf', 'ParcelLand', 'ParcelSpec',
#               'ParcelDefe', 'TotalAsses', 'TotalMarke', 'HouseNumbe', 'UnitNumber', 'StreetDire',
#               'StreetName', 'StreetType', 'StreetSuff', 'Parcel_Cit','ParcelAddr', 'PclNmbStr']
#
# d={'right':'R','left':'L'}
# df['XSection_ID']=[r'{}_{}'.format(v['StreamOrd'],d[v['bank']]) for i, v in df.iterrows()]
# df['XSection_ID']
# df_agg=pro_obj.aggregate_rows(df, 'PARCEL_ID','XSection_ID',carry_fields=keep_fld)
# df_agg.to_csv(r"C:\Box\MCM Projects\Mainspring Conservation Trust\24-092 Ela Dam Removal PDB\6.0 Plans and Specs\6.6_GIS\gis_requests\20241112_survey_parcels\Ela_XSections_endpoints_groubpy.csv")


# PDF selection
import utilities2
csv=r"C:\Box\MCM Projects\Seattle City Light\23-024_South Fork Tolt Relicensing\11.0 Supplemental Files\Figures\PSP\figure_list_PSP.csv"
df=pd.read_csv(csv)
pdf_in=r"C:\Box\MCM Projects\Seattle City Light\23-024_South Fork Tolt Relicensing\11.0 Supplemental Files\Figures\PSP\PUBLIC_P-2959_SFT_PSP.pdf"
pdf_out=r"C:\Box\MCM Projects\Seattle City Light\23-024_South Fork Tolt Relicensing\11.0 Supplemental Files\Figures\PSP\PUBLIC_P-2959_SFT_PSP_figures.pdf"
flag='MAP'
utilities2.subset_PDF(df,flag,pdf_in,pdf_out)




