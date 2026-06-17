# Run utilities_oop
# 20240926
# STEP 1: Create Initial Inventory / Updated Inventory to MERGE into existing

import sys
sys.path.append('c:/users/ZacharyUhlmann/code/arcgis')
import os
import importlib
import utilities_oop
importlib.reload(sys.modules['utilities_oop'])
import pandas as pd

tc = 'DATA_LOCATION_MCMILLEN'
parent_dir = r"C:\Box\MCMGIS\Project_Based\AEL_P\Snettisham\Data\Data_Original"
subdir_inv_obj = utilities_oop.utilities(parent_dir, tc)

# Add as second argument if excluding subdir
exclude = []
just_dir_list = []
exclude = [os.path.join(parent_dir, subd) for subd in exclude]
just_dir_list = [os.path.join(parent_dir, subd) for subd in just_dir_list]

# # a) no filetype filter
# csv_inv = r"C:\Box\MCM Projects\City of Tacoma\24-068_CTH Remodel\4.0 Data Collection\4.3 As-Builts Dwg\CTH_doc_inventory_AsBuilt.csv"
# subdir_inv_obj.subdir_inventory(exclude,new_inventory = csv_inv)

# b) filter filetype
ft_filt = ['.gdb','.cpg','.dbf','.idx','.shx','.xml']
ft_filt = ['.cpg','.dbf','.idx','.sbn','.sbx','.shx','.xml','.prj','.ipynb','.atbx','GpMessages','.qmd','ovr,','.las']
csv_new=os.path.join(parent_dir, 'snetts_exist_data_inv.csv')
csv_existing = r"C:\Box\MCMGIS\Izzy_Croteau_GIS\Izzy_Croteau_GIS_Dir_Inv.csv"
subdir_inv_obj.subdir_inventory(ft_filt, new_inventory = csv_new)
# subdir_inv_obj.subdir_inventory(ft_filt, exclude, just_dir_list, new_inventory = csv_new)
# subdir_inv_obj.subdir_inventory(ft_filt, exclude_dir_list=exclude, just_dir_list = [], new_inventory = csv_new, parse_gdb=True)
# subdir_inv_obj.subdir_inventory(ft_filt, update_inventory = csv_existing)

# c) add link
# in excel, wherein C2=cell with path    =HYPERLINK(C2,CHOOSECOLS(TEXTSPLIT(C2,"\"),-1))
