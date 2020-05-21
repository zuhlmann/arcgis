#  Utilities
# needs to become class

def add_path_multiIndex(df, layer, loc_idx, new_path, append):
    '''
    Fix hacky if/else to be vararg or something better.  Also should be a class
    ZRU 5/14/2020
    ARGS:
    df          dataframe
    layer       layer name string
    loc_idx     either 1 or 2 (int) to be formatted to "loc1" or "loc2"
    new_path    path to be addes
    append      True or False.  False will print dataframe
    '''
    try:
        isinstance(loc_idx, int)
    except:
        print('loc varible must be an integer, either 1 or 2')

    level_idx = 'loc{}'.format(loc_idx)
    try:
        if append == True:
            df.loc[(layer, level_idx), 'Original_Location'] = new_path
            return df
        else:
            print(df.loc[(layer, level_idx), 'Original_Location'])
    except KeyError:
        print('layer key does not exist i.e. FERC Boundary.  Check spelling')
