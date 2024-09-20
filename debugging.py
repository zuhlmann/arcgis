# import pro_project_oop
# importlib.reload(sys.modules['pro_project_oop'])
fp_aprx=r'C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Maps\DLA\devel\greengen_ferc\greengen_ferc.aprx'
csv_lyR_inv = r"C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Maps\DLA\devel\greengen_ferc_aprx_lyR_inv_devel.csv"
csv_maestro = r"C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Maps\DLA\devel\greengen_ferc_maestro_v2.csv"
prj_file = r"C:\Box\MCM USERS\3.0 - Employees\zuhlmann\python_df_docs\prj_files\CA_sp_II_nad83_ft_esri102642.prj"
subproject = 'greengen_ferc_v2'
fp_pathlist = r"C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Maps\DLA\devel\path_list_updated.csv"


# TOLT
import spyder_arcgis_oop as agolZ
import importlib
importlib.reload(sys.modules['spyder_arcgis_oop'])

# A) Load Project
pro_obj = agolZ.proProject()
pro_obj.dbase_init(prj_file,subproject,fp_pathlist, use_item_desc=False)
pro_obj.add_aprx(fp_aprx, csv_lyR_inv, target_col='DATA_LOCATION_MCMILLEN')

# # B) Transfer Action from df to df_aprx
# aprx_str = 'aprx_greengen_ferc'
# merge_cols = ['DATA_LOCATION_MCMILLEN','ACTION']
# pro_obj.df_to_df_transfer_v2('df', 'df_greengen_ferc_lyR', r'ACTION',r'ACTION',r'copy',
#                      'DATA_LOCATION_MCM_ORIGINAL', 'DATA_LOCATION_MCMILLEN', merge_cols,
#                      merge_cols_dict={'DATA_LOCATION_MCMILLEN':'DATA_LOCATION_MCM_RESOURCE'})
# # Save
# pro_obj.df_greengen_ferc_lyR_matched.to_csv(r"C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Maps\DLA\devel\greengen_ferc_aprx_lyR_inv_devel2.csv")

# C) Add ReSource info
pro_obj.selection_idx('df_greengen_ferc_lyR', target_action='copy')
pro_obj.format_lyR_inv_datasource_standard('aprx_greengen_ferc')