import re
import pandas as pd

# GET RID OF REMOVAL IN TEXT
# quick deal to remove "removal from name"
fp_csv = r'C:\Users\uhlmann\Box\GIS\Project_Based\Klamath_River_Renewal_MJA\GIS_Data\new_data_downloads\labelset_creation_MPs\labelset_inventory_90Des_ga.csv'
df = pd.read_csv(fp_csv)
text = df.text.tolist()

t = text[0]
text_replace = []
search_str = ['Removal and Restoration', 'Removal']
for t in text:
    idx_list = [m.start() for m in re.finditer('Removal and Restoration', t)]
    try:
        temp = idx_list[0]
        text_replace.append(t[:temp])
    except IndexError:
        text_replace.append(t)

text_replace2 = []
for t in text_replace:
    idx_list = [m.start() for m in re.finditer('Removal', t)]
    try:
        temp = idx_list[0]
        text_replace2.append(t[:temp])
    except IndexError:
        text_replace2.append(t)

df['text2'] = pd.Series(text_replace2)
fp_out = fp_csv[:-4] + '_temp.csv'
pd.DataFrame.to_csv(df, fp_out)
