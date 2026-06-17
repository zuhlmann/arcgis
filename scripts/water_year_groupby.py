# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 21:14:31 2026

@author: ZacharyUhlmann
"""

import pandas as pd
import calendar
import matplotlib.pyplot as plt
import numpy as np

# # NOTE - renamed files in direcotries
# # also copied here: C:\Box\MCM Projects\EWEB\25-074 Leaburg Canal Near Term Risk Reduction Support\6.0 Plans and Specs\6.4 Design\6.4.2 Civil\gage_ht
# csv = r"E:\tolt\add_2026\gage_8300\gage_12148300_2020thru2026.csv"
csv_groupby = r"E:\tolt\add_2026\gage_8300\gage_12148300_2020thru2026_mean_daily.csv"
#
# # function returns days in year (365 or 366 for leapyear)
# def days_in_year(year):
#     return 365 + calendar.isleap(year)
#
# years = list(range(2019,2026))
# days_dict = {y:days_in_year(y) for y in years}
#
# # Read in Big dataset
# df=pd.read_csv(csv, usecols = ['time','value','approval_status'], parse_dates=['time'])
# df['time']=pd.to_datetime(df.time, format='mixed')
# # df.drop_duplicates(subset = ['time'],inplace=True)
# df.set_index('time', inplace=True)
# df['day']=pd.to_datetime("1900-10-01", format="%Y-%m-%d")
#
# # Save data flagged as provisional (just do once)
# df_provisional = df[df.approval_status=='Provisional']
# df_provisional.to_csv(r"E:\projects\USGS_dataRetreival\data_mckenzie_2007thru2025_PROVISIONAL.csv")
#
# # A) Heavy Lift
# # aa) Add days for groupby i.e. 20250701 for all 96 potential rows in that day
# idx1 = []
# idx2 = []
# missed=[]
# ct=0
# for n, y in enumerate(years):
#     idx_st1 = f"{y}-10-01 00:00:00"
#     for i in range(days_dict[y]):
#         start_time = pd.to_datetime(idx_st1, format="%Y-%m-%d %H:%M:%S")
#         idx1.append(start_time + i*pd.to_timedelta(1, "d"))
#         idx2.append(start_time + i*pd.to_timedelta(1, "d") + pd.to_timedelta(23*60+45, "m"))
#         try:
#             df.loc[idx1[ct]:idx2[ct],'day']=start_time + i*pd.to_timedelta(1, "d")
#         except KeyError:
#             missed.append(start_time + i*pd.to_timedelta(1, "d"))
#         ct+=1
#
# df.to_csv(r"E:\tolt\add_2026\gage_8300\df_days.csv")
# # cc) Mean Daily
# group = df.groupby('day')[['value']].mean()
# group['value']=[round(v,2) for v in group.value]
# group.to_csv(csv_groupby)
# # dd) create spreadsheet with days missed - i.e. USGS data retreival did not exist
# missed = pd.DataFrame(missed)
# missed.to_csv(r"E:\tolt\add_2026\gage_8300\missed.csv")

# # B) Max in Wateryear
# years = list(range(2019,2026))
# csv_annual_idx = r"E:\tolt\add_2026\gage_8300\idx_annual_max.csv"
#
# # TEMP - to create index
# idy1 = [r"{}-10-01 00:00:00".format(y) for y in years]
# idy2 = [r"{}-09-30 00:00:00".format(y+1) for y in years]
# dft = pd.DataFrame(np.column_stack([idy1, idy2]), columns=['start','stop'])
# dft.to_csv(csv_annual_idx)
#
# dft = pd.read_csv(csv_annual_idx, usecols=['start','stop'], parse_dates=['start','stop'])
# df_group=pd.read_csv(csv_groupby, usecols = ['day','value'], parse_dates=['day'],index_col='day')
#
# mx = []
# for iy1, iy2 in zip(dft.start, dft.stop):
#     mx.append(round(max(df_group.loc[iy1:iy2,'value']),2))
# years_map = [y+1 for y in years]
# df_max = pd.DataFrame(np.column_stack([years_map, mx]), columns = ['year', 'max'])
# df_max.to_csv(r"E:\tolt\add_2026\gage_8300\test_annual.csv")
#
#
# C) Shitty plot after generating df
# PLOT
df=pd.read_csv(csv_groupby, usecols = ['day','value'], parse_dates=['day'])
df['day']=pd.to_datetime(df.day, format='mixed')

fig, ax = plt.subplots(figsize = (12,2))
ax.plot(df.day, df.value, color='darkgoldenrod')

ax.tick_params(axis='both', labelsize=4)

fig.tight_layout()
fig.savefig(r"E:\tolt\add_2026\gage_8300\test.png")
plt.show()