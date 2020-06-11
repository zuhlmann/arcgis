# python examples

#1)  nested list comprehension
# this was used to add loc1 and loc2 to a dataframe with 13 rows - why loc_vals * 26 (2 x 13)
fp_project_inventory = get_path('fp_project_inventory_working')
df_read = pd.read_csv(fp_project_inventory, skipfooter=2, index_col = 0)
# print(df_read.index.values)
print('index values')
print(df_read.index.values)
df_read = df_read.loc[[itm2 for itm in df_read.index.values for itm2 in [itm, itm]]]
# ser = pd.Series({'Locations':['loc1', 'loc1'] * (len(df_read)/2)})
# df_read['Locations'] = [item2 for iter in range(len(df_read)/2) for item2 in ['loc1', 'loc2']]
loc_vals = ['loc1', 'loc2'] * len(df_read)
df_read.insert(0, 'Locations', loc_vals)
# pd.DataFrame.to_csv(df_read, path_out)
