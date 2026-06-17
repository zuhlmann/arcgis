import numpy as np
# tried this with leaburg for la crew demo, quit when realized data was moved anyways, may still work, but quit
# 20260617

def bulk_reSource(fp_aprx, fp_key):
    df_key = pd.read_excel(fp_key, index_col='BASE_DIR_SRC')

    aprx = arcpy.mp.ArcGISProject(fp_aprx)
    map_list = aprx.listMaps()
    for l in aprx.listLayers():
        try:
            fp_orig = copy.copy(os.path.normpath(lyr.dataSource))
            if idx_key in fp_orig:
                fp_fixed = fp_orig.replace(idx_key, df.loc[idx_key, 'BASE_DIR_TGT'])

                comps = os.path.split(fp_fixed)
                if '.gdb' in fp_fixed:
                    if comps[-2]=='.gdb':
                        dbase_connection = comps[-2]
                        feature_dataset = np.nan
                    else:
                        dbase_connection = comps[-3]
                        feature_dataset = comps[-2]
                    wsf = 'FileGDB'
                    dataset = comps[-1]
                elif os.path.splitext(fp_fixed)[-1]=='.shp':
                    wsf = 'Shapefile'
                    feature_dataset = np.nan
                    dataset = comps[-1]
                    dbase_connection = f"{os.sep}".join(comps[:-1])
                else:
                    resource = False
                if resource:
                    lyr_cim = lyr.getDefinition('V3')
                    # https://community.esri.com/t5/python-questions/updating-the-data-source-of-a-feature-class-in-a/m-p/1116155#M62964
                    dc = arcpy.cim.CreateCIMObjectFromClassName('CIMStandardDataConnection', 'V3')
                    dc.workspaceConnectionString = f"DATABASE={dbase_connection}"
                    dc.workspaceFactory = wsf
                    dc.dataset = dataset
                    # check for feature dataset
                    if not pd.isnull(feature_dataset):
                        dc.featureDataset = feature_dataset
                    # Different object structure with Raster
                    if wsf == 'Raster':
                        lyr_cim.dataConnection = dc
                    elif wsf in ('Shapefile', 'FileGDB'):
                        lyr_cim.featureTable.dataConnection = dc
                    lyr.setDefinition(lyr_cim)
        except Attributerror:
            pass