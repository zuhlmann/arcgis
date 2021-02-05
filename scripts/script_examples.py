import os
import arcpy
import numpy as np
import sys
sys.path.append('C:/Users/uhlmann/code')
import utilities

#https://gis.stackexchange.com/questions/26369/get-all-the-points-of-a-polyline
#Inputs from user parameters
# InFc  = arcpy.GetParameterAsText(0) # input feature class
fp_orders = utilities.get_path(27)
InFc = os.path.join(fp_orders, 'MP_CAM_g_anno_vfrm//c2410_vfrm')

# Spatial reference of input feature class
SR = arcpy.Describe(InFc).spatialReference

# Create NumPy array from input feature class
arr = arcpy.da.FeatureClassToNumPyArray(InFc,["SHAPE@XY"], spatial_reference=SR, explode_to_points=True)
e1 = arr[0][0][0]
e2 = arr[1][0][0]
e3 = arr[2][0][0]
e4 = arr[3][0][0]

n1 = arr[0][0][1]
n2 = arr[1][0][1]
n3 = arr[2][0][1]
n4 = arr[3][0][1]

def get_hypotenuse(opp_len, adj_len):
    rad = np.arctan(opp_len/adj_len)
    return(rad)

delt_e1 = abs(e1 - e2)
delt_n1 = abs(n1 - n2)
rad1 = get_hypotenuse(delt_e1, delt_n1)

delt_e2 = abs(e2 - e3)
delt_n2 = abs(n2 - n3)
rad2 = get_hypotenuse(delt_e2, delt_n2)

len1_e = delt_e1 / np.sin(rad1)
len2_e = delt_e2 / np.sin(rad2)
len1_n = delt_n1 / np.cos(rad1)
len2_n = delt_n2 / np.cos(rad2)

print(len1_e, len2_e, len1_n, len2_n)
for vert in arr[:-1]:
    if 'min_e' not in locals():
         min_e = vert[0][0]
         max_e = vert[0][0]
         min_n = vert[0][1]
         max_n = vert[0][1]
    else:
        min_e = min(min_e, vert[0][0])
        max_e = max(max_e, vert[0][0])
        min_n = min(min_n, vert[0][1])
        max_n = max(max_n, vert[0][1])


extents = [min_e - len2_e / 2, max_e - len2_e / 2,min_n - (len1_n /2) / 0.8, max_n - (len1_n/2) / 0.8]
rotate = np.degrees(rad1)

print('{}\n{}\n{}\n{}\n'.format(min_e, max_e, min_n, max_n))
print(extents)
print(rotate)
