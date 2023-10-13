import scipy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# 20231010
# Note - ran in conda env python_gis
# From RoadDrainPoint graip analysis.  Sediment Production had an approximately exponential distribution.
# Transformed with boxcox in order to derive standard deviation, etc. from gaussian
# https://stackoverflow.com/questions/53315215/transform-some-kind-of-exponential-distribution-into-normal-distribution

csv = r"C:\Users\UhlmannZachary\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\GRAIP\graip_data_prep\DP_vals.csv"
df = pd.read_csv(csv)
ey = df.sediment_production
arr = ey.to_numpy()

# box cox
no,_ = scipy.stats.boxcox(arr)
no = no.reshape(-1,1)

plt.subplot(2,2,1)
plt.hist(arr, bins='auto')
plt.subplot(2,2,2)
plt.hist(no)
plt.show()
df['transformed'] = no
df.to_csv(csv)