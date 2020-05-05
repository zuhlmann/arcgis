# Attempt at a script (copied from https://community.esri.com/thread/71358)
# to order gdb and print out

import os
import time
import glob
gdb = 'C:/Users/uhlmann/GIS/West_Kaui_Energy_Project/Easements/Easements_Digitize.gdb'
for file_name in glob.glob(gdb + "/*"):
    file_time = os.path.getctime(file_name)
    print(type(file_time))
    file_time = time.localtime(file_time)
    print(type(file_time))
    # file_time = time.strftime("%c", time.localtime(file_time))
    print('{}\n{}'.format(file_name, file_time))
