# Startup script to link Anaconda python environment with ArcGIS
#
# Author: Curtis Price, cprice@usgs.gov

# NOTE: these instructions came from here: https://my.usgs.gov/confluence/display/EGIS/Using+Anaconda+modules+from+the+ESRI+python+environment
# ZRU 4/20/20
# 1. Install Anaconda, setup environment to match your ArcGIS version
#    example environment setup:
#      set ARCLIST=python=2.7.10 numpy=1.9.2 matplotlib=1.4.3 scipy=0.16.0 pandas pyparsing xlrd xlwt
#      conda install -n arc1041 %ARCLIST% jupyter spyder
#
# 2. Edit the paths below
#
# 3. Test this script for issues (IMPORTANT)
#    With debug = False, the script will print the sys.path
#    From ArcGIS, you should see the Conda site-packages at the end
#    From Anaconda, you should see the ArcGIS site-packages at the end
#
#    a. from ArcGIS python prompt
#    > C:\Python27\ArcGIS10.4\python.exe usercustomize.py
#
#    b. from Conda (open Anaconda x32 window)
#    > conda activate arc1041
#    > python usercustomize.py
#
#    c. from ArcMap
#    >>> sys.path.append(<path to usercustomize.py folder>)
#    >>> import usercustomize
#
#    d. from ArcGIS Pro Python prompt
#    > c:\ArcGIS\Pro\bin\Python\Scripts\propy.bat usercustomize.py
#
# 3. Edit script to set debug = False
#
# 4. Place this startup script in the startup folder
#    Startup folder can be found with: "C:\Python27\ArcGIS10.2\python -m site --user-site"
#    Usually will be:
#    C:\Users\%USERNAME%\AppData\Roaming\Python\Python27\site-packages

import os
import sys

###########################################
# Edit here match your setup
# These paths must match your Anaconda setup exactly.

# Anaconda home folders
conda_arcmap_home = r"D:\Users\uhlmann\Miniconda2"

# anaconda environments set up to match Desktop and Pro
conda_arcmap_env = "arc1061"

# change to false after testing done
debug = False

# do not edit below this line
###########################################

conda_arcmap = r"{}\envs\{}".format(conda_arcmap_home,
                                    conda_arcmap_env)

# sys.executable paths for arcmap, arcmap64, pro
# and desktop version
arcmap_path = os.environ["AGSDESKTOPJAVA"]
pp = arcmap_path.find("Desktop")
arcver = arcmap_path[pp+7:pp+11] # "10.4"
arcmap_exe = os.path.join(arcmap_path, "bin", "ArcMap.exe")

# conda root folders
conda32_exe = os.path.join(conda_arcmap, "python.exe")

# conda site_packages folders
conda32_sp = os.path.join(conda_arcmap, "Lib", "site-packages")

# arcpy root folders
arcver = arcver[:4]
arcpy32_exe = r"C:\Python27\ArcGIS{}\python.exe".format(arcver)

# arcpy site_packages folders
def getpth(pthfile):
    """Unpack .pth file to list of paths"""
    try:
        sp = os.path.dirname(pthfile)
        return [sp] + [p.strip() for p in open(pthfile, "r")]
    except:
        if debug:
            print("could not open {}".format(pthfile))

arcpy32_sp =  r"C:\Python27\ArcGIS{0}\Lib\site-packages\Desktop{0}.pth".format(arcver)
arcpy32_sp = getpth(arcpy32_sp)

# look at current sys.executable and modify path based on what is found
pexec = sys.executable.lower()

if debug:
    print("sys.executable: {}".format(pexec))

# add arcgis libs to conda python instances
if pexec == conda32_exe.lower():
    if os.path.exists(conda32_exe):
        sys.path += arcpy32_sp

# add conda libs to arcgis python instances:
#   - app python window (app .exe)
#   - ArcGIS standalone Python (C:\Python27\ArcGIS10.4\python.exe)
#   - IDLE (C:\Python27\ArcGIS10.4\pythonw.exe)
elif pexec in [arcmap_exe.lower(),
               arcpy32_exe.lower(),
               arcpy32_exe.lower().replace("python.exe", "pythonw.exe")]:
    if os.path.exists(conda32_sp):
        sys.path.append(conda32_sp)

if debug:
    print("sys.path: ")
    print("\n".join(sys.path))
