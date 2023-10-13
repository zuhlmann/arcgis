import numpy as np
import pandas as pd
# Note this original script was for symbolizing raster for Eklutna Geomorph
# Check below dir for applying to rasters.
# C:\Users\UhlmannZachary\Box\MCMGIS\Project_Based\Eklutna\Data\geomorphology
# This is for GRAIP 2023
# C:\Users\UhlmannZachary\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\GRAIP

csv = r"C:\Users\UhlmannZachary\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\GRAIP\graip_data_prep\DP_vals.csv"
df = pd.read_csv(csv, index_col = 'order')

# Find sed production value matching (closest) to std dev from transformed distribution
d = df.sediment_production
df.sed_trans

# Get list of std from cim
csv_bounds = r"C:\Users\UhlmannZachary\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\GRAIP\graip_data_prep\upper_bounds_3rd_std.csv"
df_bounds = pd.read_csv(csv_bounds)

upper_bounds = df_bounds.upper_bounds.to_list()
ub_matched=[]
for ub in upper_bounds:
    # https://stackoverflow.com/questions/30112202/how-do-i-find-the-closest-values-in-a-pandas-series-to-an-input-number
    ser = df.iloc[(df['sed_trans']-ub).abs().argsort()[0]]
    temp = ser.sediment_production
    ub_matched.append(temp)

df_bounds['bounds_matched'] = ub_matched
df_bounds.to_csv(csv_bounds)
