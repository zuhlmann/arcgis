# append and field mapping script
import os
import utilities


fp_working = utilities.get_path(18)
fp_gis_data = utilities.get_path(23)
fp_cdm = utilities.get_path(6)
fp_in = os.path.join(fp_cdm, 'Project_Data//Disposal_60_Design')
fp_out = os.path.join(fp_gis_data, 'compare_vers//field_mapping_tables/Disposal_60_Design.csv')
utilities.return_fields(fp_in, fp_out)
