from osgeo import gdal
import pandas as pd
import math
import copy
from datetime import datetime
import os


# 20250507 Interpolating rainfall points into grid, then zonal statsing into vector and csv
# San Antonio

in_file=r"C:\Box\MCM Projects\MCWRA (Monterey County)\25-001_San Antonio Spillway Design\6.0 Plans and Specs\6.4 Design\6.4.4 Hydraulics\2025 PMF update\IDW_Precip\UPDATED_stations\base_data\1995_storm_all_updated.shp"
basins=r"C:\Box\MCM Projects\MCWRA (Monterey County)\25-001_San Antonio Spillway Design\6.0 Plans and Specs\6.4 Design\6.4.4 Hydraulics\2025 PMF update\IDW_Precip\base_data\sanantonio_subbasins_nad83_2011_utm11n.shp"
df_dates = pd.read_csv(r"C:/Box/MCM Projects/MCWRA (Monterey County)/25-001_San Antonio Spillway Design/6.0 Plans and Specs/6.4 Design/6.4.4 Hydraulics/2025 PMF update\IDW_Precip\1995_DATES.csv")
# for idx in df_dates.index[0:2]:
#     dt=df_dates.loc[idx,'DATE']
#     out_file=f"C:/Box/MCM Projects/MCWRA (Monterey County)/25-001_San Antonio Spillway Design/6.0 Plans and Specs/6.4 Design/6.4.4 Hydraulics/2025 PMF update/IDW_Precip/UPDATED_stations/results/raster/pwr2smooth0/1995_fixed/{dt}_pwr2smooth0.tif"
#     gdal.Grid(out_file, in_file, format='GTiff', width=500, height=500, outputBounds=[87630,4025300, 164900, 3947300],
#               noData=-9999, algorithm='invdist:power=2.0:smoothing=0.0', zfield=str(dt))
#     print('debug')

# Vector Products
import geopandas as gpd
geodf = gpd.GeoDataFrame.from_file(basins)
dates=[str(d) for d in df_dates['DATE']]
out_file_fmt="C:/Box/MCM Projects/MCWRA (Monterey County)/25-001_San Antonio Spillway Design/6.0 Plans and Specs/6.4 Design/6.4.4 Hydraulics/2025 PMF update/IDW_Precip/UPDATED_stations/results/raster/pwr2smooth0/1995_fixed/{dt}_pwr2smooth0.tif"
out_file_list = [out_file_fmt.format(dt=dt) for dt in dates]
for out_file, date in zip(out_file_list, dates):
    import rasterio
    with rasterio.open(out_file) as src:
        transform = src.meta['transform']
        array = src.read(1)

    transform=(87630, 154.54,0,4025300,0,-156)
    from rasterstats import zonal_stats
    stats = zonal_stats(geodf, array, transform=transform)

    new_geodf = geodf.join(pd.DataFrame(stats))
    gdf_format=new_geodf[['name','mean','geometry']]
    gdf_format['mean']=round(gdf_format['mean'],2)
    gdf_format.rename(columns={'mean': date}, inplace=True)
    if not 'gdf_joined' in locals():
        gdf_joined = copy.copy(gdf_format)
    else:
        t = gdf_format[['name', date]]
        gdf_joined = pd.merge(gdf_joined, t, left_on='name', right_on='name')
gdf_joined.to_file(r"C:/Box/MCM Projects/MCWRA (Monterey County)/25-001_San Antonio Spillway Design/6.0 Plans and Specs/6.4 Design/6.4.4 Hydraulics/2025 PMF update/IDW_Precip/UPDATED_stations/results/1995_storm_idwPwr2Smth0_updated.shp", driver="ESRI Shapefile")


# # BEFORE ABOVE; Generate time range and format to 10 digit string for shapefile field name
# start = '2023010701'
# end = '2023011223'
# start_strf = pd.to_datetime(start, format = '%Y%m%d%H')
# end_strf = pd.to_datetime(end, format = '%Y%m%d%H')
# d1995 = pd.date_range(start_strf, end_strf, freq="H").tolist()
# delta=datetime.timedelta(hours=1)
# # Used math.ceil to convert from float to int(89.0 to 89)
# date_generated = [start_strf + delta * x for x in range(0, math.ceil((end_strf-start_strf)/pd.Timedelta(1,'h'))+1)]
# # Format back to initial string
# fmt=[d.strftime('%Y%m%d%H') for d in date_generated]
#
# df=pd.DataFrame(fmt)
# df.to_csv(r'C:\Box\MCM Projects\MCWRA\25-001_San Antonio Spillway Design\6.0 Plans and Specs\6.4 Design\6.4.4 Hydraulics\2025 PMF update\IDW_Precip\2023_DATES.csv')

# MET STATIONS
# aa) Base Paths
nc_dir = r'C:\Box\MCM Projects\MCWRA (Monterey County)\25-001_San Antonio Spillway Design\6.0 Plans and Specs\6.4 Design\6.4.4 Hydraulics\2025 PMF update\Gridded Rainfall\1998'
csv_dates = r"C:\Box\MCM Projects\MCWRA (Monterey County)\25-001_San Antonio Spillway Design\6.0 Plans and Specs\6.4 Design\6.4.4 Hydraulics\2025 PMF update\IDW_Precip\1998_DATES.csv"
csv_grid = r"C:\Box\MCM Projects\MCWRA (Monterey County)\25-001_San Antonio Spillway Design\6.0 Plans and Specs\6.4 Design\6.4.4 Hydraulics\2025 PMF update\IDW_Precip\validate_nc\nc_inventory_1998.csv"
csv_rainfall = r'C:\Box\MCM Projects\MCWRA (Monterey County)\25-001_San Antonio Spillway Design\6.0 Plans and Specs\6.4 Design\6.4.4 Hydraulics\2025 PMF update\IDW_Precip\validate_nc\rainfall_matched_1998.csv'

# 1) Create .nc inventory --> manually-ish with write_folder_content, use pandas os.path.split to add FNAME column
# import sys
# sys.path.append('c:/users/ZacharyUhlmann/code/arcgis')
# import utilities
# # A) create as txt
# utilities.write_folder_contents(nc_dir, filepath=True, filetype='.nc')

# # B) manually copy to csv (see next line) and finish formatting
# # Open .txt file, copy into csv, format with FNPATH for path col name, save to csv_grid path.
# csv_grid = r"C:\Box\MCM Projects\MCWRA (Monterey County)\25-001_San Antonio Spillway Design\6.0 Plans and Specs\6.4 Design\6.4.4 Hydraulics\2025 PMF update\IDW_Precip\validate_nc\nc_inventory_2023.csv"
# df=pd.read_csv(csv_grid)
# df['FNAME']=[os.path.split(fp)[-1] for fp in df.FPATH]
# df.to_csv(csv_grid)

# # 2) Create Matching .nc csv
# # bb) Add datestring to csv_grid
# df_dates=pd.read_csv(csv_dates)
# df_grid=pd.read_csv(csv_grid)
# date_str=[''.join(os.path.splitext(fn)[0].split('_')[-2:]) for fn in df_grid.FNAME]
# df_grid['DATE_STR']=date_str
# df_grid.to_csv(csv_grid)
#
# # cc) MATCH rainfall gage hourly to closest gridded/modeled file
# # 20250513
# # .nc files had date format in filename, but at irregular, not usually hourly timestep incrments
# df_dates=pd.read_csv(csv_dates)
# df_grid=pd.read_csv(csv_grid)
# # df_grid['DATE_STR']=[int(dt) for dt in df_grid['DATE_STR']]
# nc_dt_list = [datetime.strptime(str(date_str), '%Y%m%d%H%M%S') for date_str in df_grid.DATE_STR]
# matched=[]
# for idx_dates in df_dates.index:
#     tgt_dt=datetime.strptime(str(df_dates.loc[idx_dates, 'DATE']),'%Y%m%d%H')
#     diff_list = [abs(tgt_dt - nc_dt) for nc_dt in nc_dt_list]
#     idx_min = diff_list.index(min(diff_list))
#     match_fp = df_grid.loc[idx_min, 'FPATH']
#     matched.append(match_fp)
# df_dates['MATCHED_NC']=matched
# df_dates['FNAME']=[os.path.split(fp)[-1] for fp in df_dates.MATCHED_NC]
# df_dates.to_csv(csv_rainfall)

# 3) Copy to directory
# first create emtpy directory in {nc_dir}\selected to copy nc files
import shutil
df_rainfall=pd.read_csv(csv_rainfall)

for idx in df_rainfall.index:
    fname=df_rainfall.loc[idx, 'FNAME']
    shutil.copyfile(os.path.join(nc_dir,fname), os.path.join(nc_dir, f"selected\\{fname}"))


