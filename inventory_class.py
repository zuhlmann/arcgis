

class metaData(object):
    def __init__(self, fp_csv):
        self.item_descriptions = pd.read_csv(fp_csv, index_col = 'ITEM', na_values = 'NA', dtype='str')
    def sync_matching_items(fp_target_csv, bool_field, target_field, source_field):
        df_source = pd.read_csv(fp_csv, index_col = 'ITEM', na_values = 'NA', dtype = 'str')
        df_target = self.item_descriptions
        # index name for True rows.  Index name is the feature name
        index_source = df_target.index[getattr(df_target, bool_field) == True]
        # format text
        index_source = [idx.encode('utf8') for idx in index_copy]
        # Kim changed layer names.  This finds feature or shapefile orig names
        # also Kim used AGOL uploads folders a lot.  I will skip CDM when possible
        str_search = 'AGOL_DataUploads'
        fp_mcmillen_source = df_source.loc[index_source].DATA_SOURCE_MCMILLEN_JACOBS
        for index, fp in zip(index_source, fp_mcmillen_source):
            index_target = []
            if str_search in fp:
                # find feature name or shapefile name from data source mcmillen
                # still includes .shp
                shp_name = os.path.split(fp)[-1]
                # remove .shp
                feat_name = os.path.splittext[shp_name][0]
                index_target.append(feat_name)
            else:
                index_target.append(index)
        fp_copy_working = df_target.loc[index_target].DATA_SOURCE_MCM_ORIGINAL

                

# ADD NEW ROWS
# line 62 utilities
