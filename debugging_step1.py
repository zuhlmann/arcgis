import sys
sys.path.append('c:/users/uhlmann/code')
sys.path.append('c:/users/uhlmann/code/arcpy_script_tools_uhlmann')
import importlib
import spyder_arcgis_oop as agolZ
importlib.reload(sys.modules['utilities'])
importlib.reload(sys.modules['spyder_arcgis_oop'])


# DATA MANAGEMENT PATHS2
fp_pathlist = r"C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Maps\DLA\devel\path_list_updated.csv"
prj_file = r"C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\prj_files\CA_sp_II_nad83_ft_esri102642.prj"
subproject = 'greengen_ferc_v2'

agol_obj = agolZ.commonUtils()
agol_obj.dbase_init(prj_file,subproject,fp_pathlist, use_item_desc=False)

agol_obj.selection_idx('df', target_action= 'copy')
for i, n in zip(agol_obj.indices_iloc, agol_obj.indices):
    print('{}:  {}'.format(i,n))

agol_obj.take_action('df', 'copy_replace', target_col = 'DATA_LOCATION_MCMILLEN',

                     dry_run = False, save_df = True,
                     offline_source=False, offline_target=False)

