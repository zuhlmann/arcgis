import pandas as pd
import numpy as np

# Used to process bathymetry data for Boundary Dam for Andrew Lehman
# ZU 20240801


txt_in=r"E:\box_offline\projects\boundary_dam\091316_WASH-North_MBE_01ft_grid_CUBE_ENZ\091316_WASH-North_MBE_01ft_grid_CUBE_ENZ.txt"
csv =r"E:\box_offline\projects\boundary_dam\091316_WASH-North_MBE_01ft_grid_CUBE_ENZ\subset_091316.csv"
txt_out = r"E:\box_offline\projects\boundary_dam\091316_WASH-North_MBE_01ft_grid_CUBE_ENZ\091316_WASH-North_MBE_01ft_grid_CUBE_ENZ_sorted.txt"

# Save smaller test subset
txt_in_subset = r"E:\box_offline\projects\boundary_dam\BoundaryDam_Blueview__cleaned_2016\BoundaryDam_Blueview__cleaned_2016.asc"
txt_subset =r"E:\box_offline\projects\boundary_dam\BoundaryDam_Blueview__cleaned_2016\BoundaryDam_Blueview__cleaned_2016_subset.asc"
csv =r"E:\box_offline\projects\boundary_dam\BoundaryDam_Blueview__cleaned_2016\BoundaryDam_Blueview__cleaned_2016.csv"

# f_save = open(txt_subset, 'w')
# with open(txt_in_subset, 'r') as f_open:
#     for i, line in enumerate(f_open):
#         if i < 10000:
#             f_save.write(line)
#         else:
#             break
# f_save.close()

# Format properly for gdal: 1) sort values by Y then X
# Requirement to sort for recognition / opening in cloudcompare (and others)
x,y,z = [],[],[]
with open(txt_in_subset, 'r') as t:
    for i, line in enumerate(t):
        xt, yt, zt, scalar = line.split()
        x.append(float(xt))
        y.append(float(yt))
        z.append(float(zt))
df = pd.DataFrame(np.column_stack([x,y,z]), columns = ['X','Y','Z'])
df = df.sort_values(['Y','X'])
df.to_csv(csv)
# np.savetxt(txt_out, df.values, fmt='%0.3f')