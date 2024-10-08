# Run utilities_oop
# 20240926
# STEP 1: Create Initial Inventory / Updated Inventory to MERGE into existing

import sys
sys.path.append('c:/users/uhlmann/code')
import os
import importlib
import utilities_oop
importlib.reload(sys.modules['utilities_oop'])

tc = 'DATA_LOCATION_MCMILLEN'
parent_dir = r'C:\Box\MCM Projects\Chugach Electric\24-057_Hydro Site Evaluation\6.0 Plans and Specs\6.4 Design\6.4.3 Mechanical'
subdir_inv_obj = utilities_oop.utilities(parent_dir, tc)

# Add as second argument if excluding subdir
exclude = [r'_regulatory']
exclude = [os.path.join(parent_dir, subd) for subd in exclude]

# # a) no filetype filter
# csv_inv = r"C:\Box\MCM Projects\City of Tacoma\24-068_CTH Remodel\4.0 Data Collection\4.3 As-Builts Dwg\CTH_doc_inventory_AsBuilt.csv"
# subdir_inv_obj.subdir_inventory(exclude,new_inventory = csv_inv)

# b) filter filetype
ft_filt = ['.gdb','.cpg','.dbf','.idx','.shx','.xml','.shp','.ipynb','.txt']
ft_filt = ['.gdb','.cpg','.dbf','.idx','.shx','.xml']
csv_new=os.path.join(parent_dir, '643mechanical_dir_inv.csv')
subdir_inv_obj.subdir_inventory(ft_filt, exclude, new_inventory = csv_new)

# c) add link
# in excel, wherein C2=cell with path    =HYPERLINK(C2,CHOOSECOLS(TEXTSPLIT(C2,"\"),-1))