import pandas as pd
import numpy as np
import os
import copy

csv_fs = r'C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\Cultural_Resources\CUL2_data\tables\staging\20250904_draftHPMP_table_FS.csv'
csv_prim = r'C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\Cultural_Resources\CUL2_data\tables\staging\20250904_draftHPMP_table_PRIMARY.csv'
csv_trin = r'C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\Cultural_Resources\CUL2_data\tables\staging\20250904_draftHPMP_table_TRINOMIAL.csv'

csv=copy.copy(csv_trin)
csv_out = csv.replace('.csv','_fmt.csv')
df_prim=pd.read_csv(csv)

# # A) remove empty rows from specific num type
# df_fmt = df_prim[~pd.isnull(df_prim['ForestService'])]
# df_fmt.to_csv(csv_out)

# # Remove commas
# df =pd.read_csv(csv_out)
# for idx in df.index:
#     refNum=df.iloc[idx, 1]
#     refNum = refNum.strip()
#     refNum = refNum.replace(',','')
#     df.iat[idx,1]=refNum
# df.to_csv(csv_out)

# # create join table HPMP_RefNum
# df=pd.read_csv(csv_fs)
# df.drop_duplicates(['HPMP_RefNum'], inplace=True)
# csv_out = r'C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\Cultural_Resources\CUL2_data\tables\staging\20250904_draftHPMP_table_RefNum.csv'
# df.to_csv(csv_out)

# # Extra step to strip preceeding zero from trinomial
# # i.e. CA-AMA-0667 to CA_AMA-667
# df=pd.read_csv(csv_out)
# for idx in df.index:
#     orig = df.loc[idx, 'Trinomial']
#     try:
#         comps = orig.split('-')
#         print(comps[-1][0])
#         if comps[-1][0]=='0':
#             comps[-1]=comps[-1][1:]
#             updated = '-'.join(comps)
#             df.at[idx, 'Trinomial']=updated
#     except AttributeError:
#         pass
# df.to_csv(csv_out)

# Formatting dbasse
import collections
csv_tri = r"C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\Cultural_Resources\CUL2_data\tables\staging\20250904_draftHPMP_table_TRINOMIAL_fmt.csv"
df_tri = pd.read_csv(csv_tri)
t1 = df_tri[df_tri.duplicated(subset = ['Trinomial'],keep=False)]
t1a = t1.drop_duplicates(subset = ['HPMP_RefNum', 'Trinomial'])


print(2)

