import pandas as pd
import os

# # Adding 0 to improper NV5 index for 2023
# csv = r"C:\Users\ZacharyUhlmann\Documents\staging\tolt\AQ07\gcd\2023\2023_Tiles_GCD_test.csv"
# df=pd.read_csv(csv)
#
# for idx in df.index:
#     orig = df.loc[idx, 'Tile_ID']
#     p1, p2 = orig.split('_')
#     new = f"{p1}_0{p2}"
#     df.at[idx, 'Tile_ID_new'] = new
# df.to_csv(csv)

# #  basically write_folder_contents to csv
# las_dir = r'C:\Users\ZacharyUhlmann\Documents\staging\tolt\2024_LiDAR\2024_LAS\2024_LAS\Full_Classification\Full_Classification'
# csv = r"C:\Users\ZacharyUhlmann\Documents\staging\tolt\AQ07\gcd\2024_las_inv.csv"
# las_files = [f for f in os.listdir(las_dir) if f[-4:]=='.las']
# df = pd.DataFrame(las_files, columns = ['las_name'])

# Add las_name from path
csv_inv = r'C:\Users\ZacharyUhlmann\Documents\staging\tolt\AQ07\gcd\2024\2024_las_inv.csv'
df = pd.read_csv(csv_inv)
Tile_ID = [os.path.split(fp)[-1][:-4] for fp in df['las_path']]
df['las_name']=Tile_ID
df.to_csv(csv_inv)
