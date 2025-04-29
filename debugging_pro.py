import os
import pandas as pd
import sys
import arcpy
import copy
sys.path.append('c:/users/uhlmann/code')
sys.path.append('c:/users/uhlmann/code/arcpy_script_tools_uhlmann')
import importlib

# DATA MANAGEMENT PATHS2
fp_pathlist = r'C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\df_utility_csvs\path_list_updated.csv'
pl = pd.read_csv(fp_pathlist, index_col = 'gdb_str')
fp_offline = r'C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\df_utility_csvs\offline_lookup_table.csv'
olt = pd.read_csv(fp_offline, index_col = 'gdb_str')
prj_dir = r'C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\prj_files'

subproject = 'sitka_inundation'

gdb_str = '{}_gdb'.format(subproject)
gdb_pro = pl.loc[gdb_str, 'fp_gdb']
prj_file = os.path.join(prj_dir, pl[pl.subproject == subproject].prj_file.values[0])

# TOLT
import spyder_arcgis_oop as agolZ
importlib.reload(sys.modules['utilities'])
importlib.reload(sys.modules['spyder_arcgis_oop'])
agol_obj = agolZ.commonUtils()
agol_obj.dbase_init(prj_file,subproject,fp_pathlist, use_item_desc=False)

# # INDICES
# agol_obj.selection_idx('df', indices = [18])
agol_obj.selection_idx('df', target_action= 'delete')

print('nothing')

agol_obj.take_action('df', 'delete', target_col = 'DATA_LOCATION_MCMILLEN',
                     dry_run = True, save_df = True,
                     offline_source=False, offline_target=False)

fp_aprx=r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\map_documents\PSP_2024\PSP_2024.aprx"
csv=r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\sharepoint\templates\SCL_data_package_devel\SFT_lyR_deliverable_inv2_v3_0.csv"
df_lyR_inv_aprx=pd.read_csv(csv, index_col='DATA_LOCATION_MCMILLEN')
aprx = arcpy.mp.ArcGISProject(fp_aprx)
maps=aprx.listMaps('SA_geomorphic_process_flows')[0]
# Remove maps not in Use i.e. not in present in indices
layers = maps.listLayers()
idx=r'C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\map_documents\PSP_2024\PSP_2024.gdb\aquatics\SA_aquatic_sediment'
for lyr in layers:
    try:
        if lyr.dataSource==idx:
            resource = True
        else:
            resource=False
    except AttributeError:
        # does not have dataSource attribute (i.e. map server or...something)
        resource = False
    if resource:
        idx = copy.copy(os.path.normpath(lyr.dataSource))
        wsf = df_lyR_inv_aprx.loc[idx, 'workspace_factory']
        dbase_connection = df_lyR_inv_aprx.loc[idx, 'dbase_connection']
        dataset = df_lyR_inv_aprx.loc[idx, 'dataset']
        feature_dataset = df_lyR_inv_aprx.loc[idx, 'feature_dataset']

        lyr_cim = lyr.getDefinition('V3')
        # https://community.esri.com/t5/python-questions/updating-the-data-source-of-a-feature-class-in-a/m-p/1116155#M62964
        dc = arcpy.cim.CreateCIMObjectFromClassName('CIMStandardDataConnection', 'V3')
        dc.workspaceConnectionString = f"DATABASE={dbase_connection}"
        dc.workspaceFactory = wsf
        dc.dataset = dataset
        # check for feature dataset
        if not pd.isnull(feature_dataset):
            dc.featureDataset = feature_dataset
        # Different object structure with Raster
        if wsf=='Raster':
            lyr_cim.dataConnection = dc
        elif wsf in ('Shapefile', 'FileGDB'):
            lyr_cim.featureTable.dataConnection = dc
        lyr.setDefinition(lyr_cim)
        aprx.save()