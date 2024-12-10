import arcpy
import os

def update_box_path(fp_base, username, append_str, **kwargs):
    '''
    Fix mxd's containing ol box path.
    ZU 20240812.

    Args:
        fp_base:        base directory containing mxd files
        username:       ie. zuhlmann, ljohnson, etc.  This will be used to dientify and replace old Box root directory fof individual users.
        append_str:     for the end of new mxd filename
        **kwargs:       currently just select_mxd; provide a list of mxd with extenstions

    Returns:

    '''
    old_path = r'C:\Users\{}\Box\GIS'.format(username)
    new_path = r'C:\Box\MCMGIS'
    try:
        mxd_list = kwargs['select_mxds']
        if not isinstance(mxd_list, list):
            mxd_list = [mxd_list]
    except KeyError:
        mxd_list = [item for item in os.listdir(fp_base) if '.mxd' in item]
    fp_mxd_list = [os.path.join(fp_base, fname_mxd) for fname_mxd in mxd_list]
    for m in fp_mxd_list:
        mxd = arcpy.mapping.MapDocument(m)
        print('UPDATING WORKSPACE: {}'.format(m))
        mxd.findAndReplaceWorkspacePaths(old_path,new_path)
        mxd_out = '{}_{}.mxd'.format(os.path.splitext(m)[0], append_str)
        mxd.saveACopy(mxd_out)
        del mxd