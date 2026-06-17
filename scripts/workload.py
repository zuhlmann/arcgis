import pandas as pd
import copy

# Formatting Project Workload Spreadsheet for whoever
# 20260616

xlsx = r"C:\Users\ZacharyUhlmann\Downloads\Project Workload Planning 06.03.2026 (1).xlsx"
xlsx_out = r"C:\Box\MCMGIS\GIS_Standardization\workload_test.xlsx"
sheets = ['June-26','July-26','August-26','September-26','October-26','November-26','December-26','January-27','February-27','March-27']
cols = ['No.','Active Project','Whitney T.','Zach U.']

for s in sheets:
    df=pd.read_excel(xlsx, sheet_name=s, header=[2], usecols = cols)
    d = {co:co.replace('.','').replace(' ','_') for co in cols}
    df.rename(columns = d, inplace=True)
    idx = df[df['Active_Project']=='Future Project'].index.values[-1]
    df = df.iloc[:idx]
    idx_wt = df[~pd.isnull(df.Whitney_T)].index
    idx_zu = df[~pd.isnull(df.Zach_U)].index
    idx_all = idx_wt.values.tolist() + idx_zu.values.tolist()
    df_sub = df.iloc[idx_all]
    df_sub['month']=s.replace('-','_')
    df_sub = df_sub.reset_index(drop=True).set_index('month')
    if 'df_final' not in locals():
        df_final = copy.copy(df_sub)
    else:
        df_final = pd.concat([df_final, df_sub])

sf_list = [s.replace('-','_') for s in sheets]
with pd.ExcelWriter(xlsx_out) as writer:
    for sf in sf_list:
        df_temp = df_final.loc[sf]
        df_temp.to_excel(writer, sheet_name = sf)
        # print('z')