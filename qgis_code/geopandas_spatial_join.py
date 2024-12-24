import geopandas as gpd
import sys
sys.path.append('c:/users/uhlmann/code')
import importlib
import utilities2
importlib.reload(sys.modules['utilities2'])

 # left spatial join to get Sections 
 # intersecting project features at Mokelumne for table.
 # 20241212
 csv_joined=r'C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\Cultural_Resources\HDMP_2024_25\PLSS_ownership_table\Mokelumne_HPMP_2025_PLSS_owner_step1.csv'
 fp_proj_feats=r"C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\Cultural_Resources\HDMP_2024_25\PLSS_ownership_table\shp\HDMP_proj_lyt_attributes_20241212.shp"
 fp_PLSS_sections=r"C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\Cultural_Resources\HDMP_2024_25\PLSS_ownership_table\shp\PLSS_Sections_Mokelumne_AOI_CAII.shp"
 gdf_feats=gpd.read_file(fp_proj_feats)
 gdf_sections=gpd.read_file(fp_PLSS_sections)

 gdf_joined=gdf_feats.sjoin(gdf_sections, how="left")
 gdf_joined=gdf_joined[['descriptio','HDMP_RefNu','MTRS']]
 gdf_joined.to_csv(csv_joined)

## Aggregate by MTRS
#cf=[r'HDMP_RefNu']
#csv_agg=r'C:\Box\MCMGIS\Project_Based\GreenGen_Mokelumne\Data\Cultural_Resources\HDMP_2024_25\PLSS_ownership_table\Mokelumne_HPMP_2025_PLSS_owner_step2.csv'
#utilities2.aggregate_rows2(csv_joined, csv_agg, r'descriptio', r'MTRS', carry_fields=cf)