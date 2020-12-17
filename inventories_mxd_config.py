# configuration workspace for pumping out mxds
import utilities
import copy
import os
import pandas as pd

fp_camas = (r'C:\Users\uhlmann\Box\GIS\Project_Based\Klamath_River_Renewal_MJA'
            '\GIS_Request_Tracking\GIS_Requests_Management_Plans\Camas_MPs\MP1')

fp_base = copy.copy(fp_camas)
fp_csv = os.path.join(fp_camas, 'camas_figures_delivered//draft3_20201211/draft3_20201211.csv')
utilities.create_df_inventory(fp_base, fp_csv, 'final')

df = pd.read_csv(fp_csv)
indices = list(range(4,12))
for idx in indices:
    dir = df.iloc[idx].base_dir
    fp_mxd = os.path.join(dir, df.iloc[idx].mxd_filename)
    fp_pdf = os.path.join(dir, df.iloc[idx].pdf_filename)
    range_str = 'ALL'
    print('export_ddp for: {}'.format(os.path.split(fp_mxd)[-1]))
    utilities.export_ddp(fp_mxd, fp_pdf, range_str)
