#  DETERMINE mxd version
# https://gis.stackexchange.com/questions/62090/using-arcpy-to-determine-arcmap-document-version
import os
import glob
import sys
sys.path.append('c:/Users/ZacharyUhlmann/code/arcgis')
import utilities
import importlib
import utilities_oop
importlib.reload(sys.modules['utilities'])
importlib.reload(sys.modules['utilities_oop'])
import pandas as pd
import copy
import numpy as np

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


# # PDF selection
# import utilities2
# csv=r"C:\Box\MCM Projects\Seattle City Light\23-024_South Fork Tolt Relicensing\11.0 Supplemental Files\Figures\PSP\figure_list_PSP.csv"
# df=pd.read_csv(csv)
# pdf_in=r"C:\Box\MCM Projects\Seattle City Light\23-024_South Fork Tolt Relicensing\11.0 Supplemental Files\Figures\PSP\PUBLIC_P-2959_SFT_PSP.pdf"
# pdf_out=r"C:\Box\MCM Projects\Seattle City Light\23-024_South Fork Tolt Relicensing\11.0 Supplemental Files\Figures\PSP\PUBLIC_P-2959_SFT_PSP_figures.pdf"
# flag='MAP'
# utilities2.subset_PDF(df,flag,pdf_in,pdf_out)

# #  MOKELUMNE FORMAT
# # Expand_csRow
# parent_dir = r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\map_documents"
# tc = r"whatever"
# utils_obj = utilities_oop.utilities(parent_dir, tc)
#
# fnames=['PRIMARY','TRINOMIAL','USFS']
# split_keys=['primary_num','trinomial','FS_num']
# fnames=[f"Mokelumne_HPMP_Site_Table_2024_20240116_{v}.csv" for v in fnames]
# table_dir=r'C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\Cultural_Resources\CUL2_data\tables'
# fps=[os.path.join(table_dir, fn) for fn in fnames]
#
# # Create initial table and generate counts
# for csv_out, sk in zip(fps,split_keys):
#     csv_orig=r"C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\Cultural_Resources\CUL2_data\tables\Mokelumne_HPMP_Site_Table_20240116.csv"
#     df=pd.read_csv(csv_orig)
#     utils_obj.expand_csRow(df, csv_out, r'FERC_14794_ref',sk)
#     df=pd.read_csv(csv_out)
#     df=df[~pd.isna(df[sk])]
#     t = df.FERC_14794_ref.to_list()
#     if 'count_list' not in locals():
#         count_list=copy.copy(t)
#     else:
#         count_list.extend(t)
# v, c = np.unique(count_list, return_counts=True)
# v=list(v)
# c=list(c)
#
# # Add counts to each
# # When done, delete the two columns not split
# df.sort_values(by=['FERC_14794_ref'], inplace=True)
# for csv_out, sk in zip(fps,split_keys):
#     df=pd.read_csv(csv_out)
#     df = df[~pd.isna(df[sk])]
#     # Issue with try/except not working; use this instead
#     bandaid=df['FERC_14794_ref'].to_list()
#     df=df.set_index('FERC_14794_ref')
#     for idx, ct in zip(v,c):
#         if idx in bandaid:
#             df.at[idx, 'Count']=ct
#         else:
#             pass
#     df.sort_values(by=['FERC_14794_ref'], inplace=True)
#     df.reset_index()
#     df.to_csv(csv_out)

# # Find Duplicates missed during QGIS join
# # 20250124
# base_dir=r"C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\Cultural_Resources\CUL2_data\tables"
# utils_obj = utilities_oop.utilities(base_dir, 'whatever')
# fp_list=[f'{base_dir}\Mokelumne_HPMP_Site_Table_2024_20240116_{ap}.csv'.format(ap) for ap in ['PRIMARY','TRINOMIAL','USFS']]
# tc_list=['primary_num','trinomial','FS_num']
# for fp, tc in zip(fp_list, tc_list):
#     dft=pd.read_csv(fp)
#     csv=r'C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\Cultural_Resources\CUL2_data\tables\intermediary\duplicated_nums_{}.csv'.format(tc)
#     utils_obj.aggregate_rows(dft, csv, tc, r'FERC_14794_ref')

# # add ITEM to df
# csv = r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\sharepoint\templates\SCL_data_package_devel\SFT_lyR_reSourcing.csv"
# df = pd.read_csv(csv, index_col='ROW_ID')
# item = [os.path.split(fp)[-1] for fp in df.DATA_LOCATION_MCMILLEN]
# df['ITEM'] = item
# df.to_csv(csv)

feat_name = r"E:\projects\LA_River\intermediary\eSoLACo_ecotopes_20260126_multi.shp"
fp_csv = r"C:\Box\MCMGIS\Project_Based\RsrcDistSantaMonicaMtns\SouthLACoConnectivityPlan\requests\20260126\SoLACo_ecotopes_multi.csv"
utilities.update_field(feat_name, {'feat':r'ECOTOPE_19','csv_idx_col':'ECOTOPE_19'}, 'ORIG_FID', 1, False, fp_csv)

