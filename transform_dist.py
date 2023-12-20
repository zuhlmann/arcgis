from scipy import stats
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# 20231010
# Note - ran in conda env python_gis
# From RoadDrainPoint graip analysis.  Sediment Production had an approximately exponential distribution.
# Transformed with boxcox in order to derive standard deviation, etc. from gaussian
# https://stackoverflow.com/questions/53315215/transform-some-kind-of-exponential-distribution-into-normal-distribution

# csv = r"C:\Users\UhlmannZachary\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\GRAIP\graip_data_prep\DP_vals_run2.csv"
csv = r"C:\Users\UhlmannZachary\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\GRAIP\graip_data_prep\DP_vals_run_20231115.csv"
df = pd.read_csv(csv)
ey = df.sediment_delivered
arr = ey.to_numpy()


# final - work with zeros and merge
arr_pos = arr[arr>0]
no,_ = stats.boxcox(arr_pos)
no_trans = np.empty_like(arr)
no_trans[arr>0]=no
no_trans[arr==0]=-9999
no_trans = no_trans.reshape(-1,1)

# flag zeros
flag = np.empty_like(arr,dtype='<U4')
flag[arr>0]='pos'
flag[arr==0]='zero'
flag = flag.reshape(-1,1)

# Plot
plt.subplot(2,2,1)
plt.hist(arr, bins='auto')
plt.subplot(2,2,2)
plt.hist(no)
plt.show()

df['zero_DelProb']=flag
df['SedDel_trans']=no_trans
df.to_csv(csv)
