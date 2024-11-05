# E) ONE-OFF lyR Inv for MULTIPLE aprx from script
# Created Input CSV in dir_use_inv inventory, to list all aprx used in PAD/PSP and agglomerate
csv_aprx=r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\map_documents\map_documents_aprx_inventory.csv"
csv_aprx_lyR_2=r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\sharepoint\templates\SCL_data_package_devel\SFT_lyR_deliverable_devel_v3_2.csv"
# pro_obj.aprx_map_inv2(csv_aprx, csv_aprx_lyR_2)
#
# E2) Concatenate Aggregate
csv_aprx_lyR_1=r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\sharepoint\templates\SCL_data_package_devel\SFT_lyR_deliverable_devel_v3_1.csv"
cf = ['ITEM','IS_RASTER','IS_BROKEN']
# pro_obj.concatenate_aggregate(csv_aprx_lyR_2, csv_aprx_lyR_1, 'APRX', 'DATA_LOCATION_MCMILLEN', 'MAP_NAME', carry_fields=cf)
# A. Agglomerate with aprx and map_name

# # B. Aggregate Map_Name from Data_Location;  could have potentially skipped step 2.
# df1=pd.read_csv(csv_aprx_lyR_1)
# df2 = pro_obj.aggregate_rows(df1, 'DATA_LOCATION_MCMILLEN','APRX',carry_fields=cf)
# csv_aprx_lyR_0=r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\sharepoint\templates\SCL_data_package_devel\SFT_lyR_deliverable_inv2_v3_0.csv"
# df2.to_csv(csv_aprx_lyR_0)