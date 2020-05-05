# Use this script to save to pandas dataframe within python

import arcpy
import pandas as pd

# Base Paths
path_to_base = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Request_Tracking/GIS_Requests_Kleinshmidt'
path_to_data_received = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath/DataReceived/'
path_out = 'C:/Users/uhlmann/Box/GIS/Project_Based/Klamath_River_Renewal_MJA/GIS_Request_Tracking/GIS_Kleinshmidt_scratch'

# gdb paths
path_to_kleinshmidt = os.path.join(path_to_base, 'Kleinshmidt.gdb')
path_to_kleinshmidt_send = os.path.join(path_to_base, '2020_04_16/Kleinshmidt_p2.gdb')
path_to_cdm_20191004 = os.path.join(path_to_data_received, 'AECOM/100719/WetlandAndBio_GISData_20191004/Klamath_CDM_20191004.gdb')
path_to_vector= os.path.join(path_to_data_received, 'Klamath_Vector_Data.gdb')

# Choose workspaces and features
path_working=copy.copy(path_to_kleinshmidt_send)
# set workspace
arcpy.env.workspace=copy.copy(path_working)

# manually list features as opposed to ListFeatureClasses of entire gdb
feat_names_vector=['Protected_Areas', 'ProtectedAreas_CA', 'ProtectedAreas_OR', 'Public_Lands', 'Wildlife_Refuge_NRPC_National', 'Wildlife_Refuges_CA', 'National_Forest', 'State']
feat_names_cdm_20191004=['WFC_Observations', 'WPT_Historical_Habitat', 'WPT_Observations_2018']

# get paths to features
# Method 1
# Manually from desired feature names list
feat_names = copy.copy(feat_names_vector)
# Method 2
# list feature classes from working env
feat_names=arcpy.ListFeatureClasses()

# PROTOCOL 1. CREATE Reference CSV for gdb
# Generate Paths to features
path_to_feat=[]
[path_to_feat.append(os.path.join(path_working, feat)) for feat in feat_names]

# Make a datafar
df = pd.DataFrame({'Feature':feat_names})

# iterate through feature classes in gdb and add column with field names
fields_out=[]
for path_to_ind_feat in path_to_feat:
    # path_to_feat = '{}/{}'.format(path_to_gdb, feat_name)
    fields = arcpy.ListFields(path_to_ind_feat)
    fields_temp=[]
    for field in fields:
        fields_temp.append(field.name)
    fields_out.append(', '.join(fields_temp))

df['Fields']=fields_out

# Add feature count for each feature class
num_feat=[]
for path_to_ind_feat in path_to_feat:
    temp_ct = arcpy.GetCount_management(path_to_ind_feat)
    num_feat.append(int(temp_ct[0]))
df['Num_Features']=num_feat
# Save
pd.DataFrame.to_csv(df, os.path.join(path_to_base,'2020_04_16/KRRP_data_inventory__20200416.csv')

# POTPOURI.
rec_features = ['Recreational_Areas_Points', 'Recreational_Areas_Poly', 'RecreationSites_Proposed']
rec_field = ['REC_NM', 'REC_NM', 'label']
rec1 = ['Topsy Campground', 'Pioneer Park', 'Spring Island River Access', 'Mallard Cove', 'Copco Cove', 'Fall Creek',
'Jenny Creek', 'Wanaka Springs', 'Camp Creek', 'Juniper Point', 'Mirror Cove', 'Overlook Point', 'Long Gulch',
'Iron Gate Fish Hatchery']

['Klamath', 'Fremont Winema', 'fremont_winema', 'winema', 'fremont', 'Six', 'Rivers', 'Six_rivers', 'six rivers', 'Modoc', 'Redwood', 'Lava Beds', 'lave_beds', 'lava', 'Cascade-Siskiyou', 'Siskiyou', 'Crater Lake', 'crater_lake', 'crater', 'Klamath Marsh', 'klamath_marsh', 'Tule Lake', 'tule_lake', 'tule', 'Lower Klamath', 'lower_klamath', 'Upper Klamath', 'upper_klamath']
test_target=['Klamath', 'Fremont Winema', 'fremont_winema', 'winema', 'fremont']
idx = 1

# POTPOURI 1. Get unique values from a field and save as cxv
def unique_values(table , field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})

my_values = unique_values('{}/{}'.format(path_to_gdb, rec_features[idx]) , rec_field[idx])

df = pd.DataFrame({'unique_vals':my_values})
out_path = '{}/{}_unique_values.csv'.format(path_to_base, rec_features[idx])
pd.DataFrame.to_csv(df, out_path)

# POTPOURI 2. find substrings in list
src_fields=['REC_NM']
src_list=['Klamath', 'Fremont Winema', 'fremont_winema', 'winema', 'fremont']
tgt_list = ['Klamath_p', 'Fremont', 'wine']
match=[]
for src in src_list:
    for idx, tgt in enumerate(tgt_list):
        if src.lower() in tgt.lower():
            match.append(idx)
# get unique vals I believe
set(sort(match))

# POTPORI 3. Used to explore and subset data SEARCH CURSOR
temp_id=[]
temp_acre=[]
with arcpy.da.SearchCursor(rec_poly, ['OBJECTID','acres']) as cursor:
    for idx, row in enumerate(cursor):
        # row[idx] will select based on second arg da.SearchCursor list
        if row[1]>3:
            temp_id.append(idx)
            temp_acre.append(row[1])
df = pd.DataFrame({'OBJECTID':temp_id, 'acre':temp_acre})

# POTPORI 4 Search Cursor selected Rows
import arcpy

fields = ["OBJECTID"]

mxd = arcpy.mapping.MapDocument("CURRENT")
lyr = arcpy.mapping.Layer("polygon_from_polyline4")

bCursor = arcpy.da.SearchCursor(lyr,fields)

lst_msg = []
for row in bCursor:
    print(row[0])
    lst_msg.append(row[0])
print(lst_msg)

# list comprehension for all fields
# get path_to_feat from top of script
nm_field = ['loc_nm', 'unit_name', 'p_des_nm'] # or try 'unit_nm' for pos 0 (Protected_Areas)
idx_feat=0
atts = []
[atts.append(str(f.name)) for f in arcpy.ListFields(path_to_feat[idx_feat])]
# [atts.append(str(f.name)) for f in arcpy.ListFields(path_to_feat[0], field_type='String')]
atts_stripped=[]
# remove quotation marks
atts_stripped.append(', '.join(atts))

my_values = unique_values(path_to_feat[idx_feat], nm_field[idx_feat])
my_values_stripped, my_values_stripped_lower = [], []
for val_str in my_values:
    try:
        my_values_stripped_lower.append(val_str.encode('utf-8').lower())
        my_values_stripped.append(val_str.encode('utf-8'))  # to use in dataframe
    except AttributeError:
        pass
df = pd.DataFrame({'name':my_values_stripped, 'name_lc':my_values_stripped_lower})
tgt_locs = ['Klamath', 'winema', 'fremont', 'Six', 'Modoc', 'Redwood', 'Lava Beds', 'Siskiyou', 'Crater Lake', 'Klamath Marsh', 'Tule Lake']
for tgt_loc in tgt_locs:
    print((df['name'][df['name_lc'].str.contains(tgt_loc.lower())]))
print('Just searched this feature: ', feat_names[idx_feat])
pd.DataFrame.to_csv(df, os.path.join(path_out, '{0}_{1}{2}'.format(feat_names[idx_feat], 'unitName','.csv')))
