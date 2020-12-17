import os
import arcpy

# merge example 12/6/2020
fp_restoration = r'C:\Users\uhlmann\Box\GIS\Project_Based\Klamath_River_Renewal_MJA\GIS_Data\McmJac_KRRP_GIS_data\working.gdb\restoration'
# Note - pound signs turn lines into comments that are for notes NOT executing
# os.path.join will create a file path by adding the CESO_KRC_Interim21_2019 string to the restoration dataset path:
# i.e.  fp_ceso = ...\working.gdb\restoration\CESO_KRC_Interim21_2019'
fp_ceso = os.path.join(fp_restoration, 'CESO_KRC_Interim21_2019')
fp_taca = os.path.join(fp_restoration, 'TACA_KRC_Interim21_2019')
fp_weeds_misc = os.path.join(fp_restoration, 'MISC_Weeds_KRC_Interim21_2019')
fp_out = os.path.join(fp_restoration, 'select_klamath_invasive_weeds_NISIMS')
arcpy.Merge_management([fp_ceso, fp_taca, fp_weeds_misc], fp_out)


# copy all shapefiles
