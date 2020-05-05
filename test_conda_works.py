import arcview
import arcpy
import pandas as pd
import copy
import os
import numpy as np

#NOTE: Testing Conda is good tutorial and guie

# Base Paths
path_to_base = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Request_Tracking/GIS_DataReceived_Descriptions'
path_to_data_received = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/'
path_out = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Request_Tracking/GIS_Kleinshmidt_scratch'

# gdb paths
path_to_kleinshmidt = os.path.join(path_to_base, 'Kleinshmidt.gdb')
path_to_kleinshmidt_send = os.path.join(path_to_base, '2020_04_16/Kleinshmidt_p2.gdb')
path_to_cdm_20191004 = os.path.join(path_to_data_received, 'AECOM/100719/WetlandAndBio_GISData_20191004/Klamath_CDM_20191004.gdb')
path_to_vector= os.path.join(path_to_data_received, 'Klamath_Vector_Data.gdb')
path_to_benji = os.path.join(path_to_data_received, 'Stantec', '20191204_ToBenji_CurrentLoWs', 'CurrentLoWs_20191204.gdb')

# Choose workspaces and features
path_working=copy.copy(path_to_benji)
# set workspace
arcpy.env.workspace=copy.copy(path_working)

test = np.reshape(np.arange(3*3*3), (3,3,3))
print(test)
