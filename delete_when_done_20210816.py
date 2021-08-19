df_item = df.loc[index]
      fp_fcs_current = os.path.normpath(df_item[target_col])
      # create new filename components
      fc_new_name = df_item['RENAME']
      fp_components = fp_fcs_current.split(os.sep)
      # all but original file name
      fp_base = os.sep.join(fp_components[:-1])
      # full path to new fcs
      fp_fcs_new = os.path.join(fp_base, fc_new_name)
