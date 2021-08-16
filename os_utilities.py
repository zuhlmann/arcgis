from os.path import dirname, abspath
import os
# formatting file names it appears

def format_names(indir):
    # https://stackoverflow.com/questions/37467561/renaming-multiple-files-in-a-directory-using-python
    fnames = os.listdir(indir)
    for fn in fnames:
        fp_in = str(os.path.join(indir, fn))
        replace_dict = {' ':'_','(2)':'','-':'_'}
        for k,v in replace_dict.items():
            fn = fn.replace(k, v)
            os.rename(fp_in, os.path.join(indir, fn))
