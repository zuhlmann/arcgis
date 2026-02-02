import pandas as pd
import os

# copy and paste a column (ORDER) in dbeaver and generate tuple to select rows in selection.sql

dir_out = r'C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\sharepoint\templates\SCL_data_package_devel\staging'
csv = os.path.join(dir_out, "sql_select.csv")
df = pd.read_csv(csv)
t = list(df['row'])
t = ','.join([str(v) for v in t])
t=f"({t})"
text_out = os.path.join(dir_out,'sql_text.txt')
with open(text_out, 'w') as txt:
    txt.write(t)
