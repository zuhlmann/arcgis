import arcpy
import pandas as pd
import copy
import numpy as np
#20261009

df_all = pd.read_excel(r"D:\projects\snettisham\add_box\AGOL\snett_gdb_attachment_files.xlsx", index_col='FEATURE')
# df_select = df_all.loc[['CoverEstimate_Feature','CoverEstimate_TABLE']]
# for idx in df_select.index:
#     df_cover = pd.read_csv(df_all.loc[idx,'PATH_INV'])
#     # df_field_obs = pd.read_csv(df_all.loc[idx,'PATH_INV'])
#     # df_plot = pd.read_csv(df_all.loc[idx,'PATH_INV'])
#     # df_cover_table = pd.read_csv(df_all.loc[idx[3],'PATH_INV'])
#     # df_species = pd.read_csv(df_all.loc[idx,'PATH_INV'])
#     cols_init = df_cover.columns
#     vals_bool = [True]*len(cols_init)
#     if 'df_matrix' not in locals():
#         df_matrix = pd.DataFrame(np.array([vals_bool]), columns = cols_init.to_list(), index = [idx])
#     else:
#         df_row = pd.DataFrame(np.array([vals_bool]), columns=cols_init.to_list(), index=[idx])
#         df_matrix = pd.concat([df_matrix, df_row], ignore_index=False, sort=False)
# df_matrix.to_csv(r'D:\projects\snettisham\add_box\AGOL\snett_matrix_cover.csv')

# # Create Single COVER Inv
# csv_cover_concat = r'D:\projects\snettisham\add_box\AGOL\extracted\Snettisham_2026_Cover_Estimate_EDIT_v1_20261008\CoverEstimate_Formatted.csv'
# csv_cover_concat2 = r'D:\projects\snettisham\add_box\AGOL\extracted\Snettisham_2026_Cover_Estimate_EDIT_v1_20261008\CoverEstimate_Formatted2.csv'
# df_all = pd.read_excel(r"D:\projects\snettisham\add_box\AGOL\snett_gdb_attachment_files.xlsx", index_col='FEATURE')

# # STEP 1   ----Join FEature and Attach Table
# df_cover = pd.read_csv(df_all.loc['CoverEstimate_Feature','PATH_INV'])
# df_cover_table = pd.read_csv(df_all.loc['CoverEstimate_TABLE','PATH_INV'])
# df_cover_concat = pd.concat([df_cover, df_cover_table], sort=False)
# df_cover_concat.to_csv(csv_cover_concat)

# # STEP 2   -----Concat VegPlot
# # intermediary step to Add SiteID field to CoverInv above (PlotID minus "A" "B", etc)
# df_cover_concat = pd.read_csv(csv_cover_concat)
# df_plots = pd.read_csv(df_all.loc['Plots_Feature','PATH_INV'])
# df_cover_concat = pd.concat([df_cover_concat, df_plots], sort=False)
# df_cover_concat.to_csv(csv_cover_concat2)

# # Create Single SPECIES Inv
# df_all = pd.read_excel(r"D:\projects\snettisham\add_box\AGOL\snett_gdb_attachment_files.xlsx", index_col='FEATURE')
# csv_spp_concat = r"D:\projects\snettisham\add_box\AGOL\extracted\Snettisham_2026_Species_Inventory_EDIT_v1_20261008\SpeciesInventory_Formatted.csv"
#
# # ----Join FEature and Attach Table
# df_species = pd.read_csv(df_all.loc['SpeciesInventory_TABLE','PATH_INV'])
# df_plots = pd.read_csv(df_all.loc['Plots_Feature','PATH_INV'])
# df_species_concat = pd.concat([df_species, df_plots], sort=False)
# df_species_concat.to_csv(csv_spp_concat)

# SUBSET VEG PLOT THAT ARE NOT IN SPP OR COVER
df_all = pd.read_excel(r"D:\projects\snettisham\add_box\AGOL\snett_gdb_attachment_files.xlsx", index_col='FEATURE')
csv_plot_ONLY = r'D:\projects\snettisham\add_box\AGOL\extracted\FieldObs_2026\VegPlot_Formatted.csv'

df_plots = pd.read_csv(df_all.loc['Plots_Feature','PATH_INV'])
sites_both = [r'AS-10A', r'AWS-1A', r'WH-109A', r'YC-123A']
idx_both = [idx for idx in df_plots.index if df_plots.loc[idx, 'PlotID'] in sites_both]
df_subset = df_plots.loc[idx_both]
df_subset.to_csv(csv_plot_ONLY)
print(df_subset)

# ARCHIVE
# # Get shp to pull into postgres
# feat = r'D:\projects\snettisham\add_box\AGOL\gdb\Snettisham_2026_Species_Inventory_EDIT_v1_20261008\Snettisham_2026_Species_Inventory_EDIT_v1_20261008.gdb\SpeciesInventory'
# feat_out = r'SpeciesInventory'
# out_dir = r'D:\projects\snettisham\add_box\AGOL\gdb\shp'
# arcpy.FeatureClassToFeatureClass_conversion(feat, out_dir, feat_out)

# then used QGIS ExportToPostGres (ogr2ogr essentially) to add to snettisham postgres dbase
# ensured postgis extentsion added to dbase
# NOTE - never used the product of all this work.
# Realized that I could just join the feature layer to the table for SpeciesDetails and get it all
# then redid the photolog

# # Create string of committed / ommited from both si and sdt (the variables in postgres assiged to each table)
# # removed fields (see last comment) and copied into postgres sql as select si.col1, si.col2, ...etc
# # note that quotes were required for source ( or target?) table.
# feat = r'D:\projects\snettisham\add_box\AGOL\gdb\Snettisham_2026_Species_Inventory_EDIT_v1_20261008\Snettisham_2026_Species_Inventory_EDIT_v1_20261008.gdb\SpeciesInventory'
# s3 = set([f.name for f in arcpy.ListFields(feat)])
# csv1 = r"D:\projects\snettisham\add_box\AGOL\extracted\Snettisham_2026_Species_Inventory_EDIT_v1_20261008\SpeciesDetails_TABLE.csv"
# csv2 = r"D:\projects\snettisham\add_box\AGOL\extracted\Snettisham_2026_Species_Inventory_EDIT_v1_20261008\SpeciesDetails_photo_log.csv"
# df1 = pd.read_csv(csv1)
# df2 = pd.read_csv(csv2)
# s1 = set(df1.columns)
# s2 = set(df2.columns)
# c_match = (s3.intersection(s1))
# l1 = [r'si.{}'.format(c[:10]) for c in list(s3)]
# l2 = [r'sdt."{}"'.format(c) for c in list(s1 - c_match)]
# col_str1 = ', '.join(l1)
# col_str2 = ', '.join(l2)
# with open(r'D:\projects\snettisham\add_box\AGOL\extracted\Snettisham_2026_Species_Inventory_EDIT_v1_20261008\SpeciesInventory_cols_unique.txt','w') as txt:
#     txt.write(f"Columns exclusively in feature class\n: {col_str1}\n")
#     txt.write(f"Columns exclusively in table\n: {col_str2}")
#
# # Needed to delete si.objectid, si.shape and add si.wkb_geometry
