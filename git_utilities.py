import pandas as pd
import os

# Used during tolt_agol_obj cleanup
# first definiation does something
# script pointless because TIME_MODIFIED did ont correspond to last branch commit

def parse_git_status_csv(csv, basepath):
    '''
    Use command git diff --name-status master from branch of interest to determine
    changes on macro-file level.  Copy and paste to csv.  use this to parse output into
    coherent csv. 20241204.  Used during merging tolt_agol_obj situation.
    Args:
        csv:

    Returns:

    '''
    df=pd.read_csv(csv)
    for idx in df.index:
        r = df.loc[idx].values[0]
        code, fname = r.split()
        e = os.path.splitext(fname)[-1]
        df.at[idx, 'CODE'] = code
        df.at[idx, 'FNAME']=fname
        df.at[idx, 'FPATH']=os.path.join(basepath, fname)
        df.at[idx, 'EXTENSION']=e
    df.to_csv(csv)

def format_git_diff_csv_1(csv1, csv2, csv_log, branch1_name, branch2_name, join_col, csv_out):
    df1=pd.read_csv(csv1)
    df2=pd.read_csv(csv2)
    df_log=pd.read_csv(csv_log)
    # normalize path
    df1[join_col]=[os.path.normpath(fp) for fp in df1[join_col]]
    df2[join_col]=[os.path.normpath(fp) for fp in df2[join_col]]
    df_log[join_col] = [os.path.normpath(fp) for fp in df_log[join_col]]
    df_log = df_log.set_index(join_col)
    df1=df1[[join_col, 'TIME_MODIFIED']]
    df1=df1.rename(columns={'TIME_MODIFIED':'TIME_MODIFIED_{}'.format(branch1_name)})
    df1=df1.set_index(join_col)
    df2=df2[[join_col, 'TIME_MODIFIED']]
    df2=df2.rename(columns={'TIME_MODIFIED':'TIME_MODIFIED_{}'.format(branch2_name)})
    df2=df2.set_index(join_col)
    df_log = df_log.merge(df1, how='left', left_index=True,right_index=True)
    df_log = df_log.merge(df2, how='left', left_index=True,right_index=True)
    df_log.to_csv(csv_out)

# # 1) Run these twice; once for branch, once for master
# import utilities_oop
# tc = 'DATA_LOCATION_MCMILLEN'
# parent_dir='path/to/inv/dir'
# subdir_inv_obj = utilities_oop.utilities(parent_dir, tc)
# e='list of paths to exclude'
# csv_new=r"C:\Box\MCM USERS\3.0 - Employees\zuhlmann\code_subdir_inv_master.csv"
# subdir_inv_obj.subdir_inventory([], e, new_inventory = csv_new)
#
# # path to csv created from
# # git diff --name-status <branch or master>
# # use branch or master if on master or branch resepctively - check gists
# csv=r"C:\Box\MCM USERS\3.0 - Employees\zuhlmann\git_branch_changes_master.csv"
# parse_git_status_csv(csv, bp)

csv1=r"C:\Box\MCM USERS\3.0 - Employees\zuhlmann\code_subdir_inv.csv"
csv2=r"C:\Box\MCM USERS\3.0 - Employees\zuhlmann\code_subdir_inv_master.csv"
csv_log=r"C:\Box\MCM USERS\3.0 - Employees\zuhlmann\git_branch_changes_branch.csv"
csv_out=r"C:\Box\MCM USERS\3.0 - Employees\zuhlmann\git_branch_changes_joined.csv"
tc = 'DATA_LOCATION_MCMILLEN'
format_git_diff_csv_1(csv1, csv2, csv_log, r'tolt_agol_obj', r'master', tc, csv_out)
