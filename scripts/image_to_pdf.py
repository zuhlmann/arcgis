from PIL import Image
import pandas as pd
import numpy as np
import os

# Jan 2026 for Tolt QAQC figs
# https://stackoverflow.com/questions/27327513/create-pdf-from-a-list-of-images
study=['TR04']
# study = [r'TR0{}'.format(i) for i in range(1,8)]
image_dir = [f"E:/tolt/ISR/{s}" for s in study]

# Step 1 CREATE INVENTORY
# Ceate inventory of file names to copy manually into master list w/page num, caption, etc.
# Make column name for fname = Fname
file_ext = ['.png','.jpg']
flist=[]
study_list=[]
for id, st in zip(image_dir, study):
    flist_temp = [fn for fn in os.listdir(id) if os.path.splitext(fn)[1] in file_ext]
    flist.extend(flist_temp)
    study_list.extend([st]*len(flist_temp))
df = pd.DataFrame(np.column_stack([study_list, flist]), columns=['study','Fname'])
# Line 1 for basic, Line 2 for TR
df.to_csv(os.path.join(image_dir[0], 'Initial_Image_List.csv'))

# Step 2 CREATE THE WHOLE THING FROM FORMATTED ABOVE
pdf_path = f"E:/tolt/ISR/{study[0]}/{study[0]}_ISR_Figures.pdf"
csv = f"E:/tolt/ISR/{study[0]}/{study[0]}_ISR_Figure_Inventory.csv"
# # If TR Study, uncomment
# pdf_path = r"E:\tolt\ISR\TR_ISR_Figures.pdf"
# csv = r"E:\tolt\ISR\TR_ISR_Figure_Inventory.csv"

df_format=pd.read_csv(csv)
images = []
fname = []
page_num = []
for n, idx in enumerate(df_format.index):
    # If normal
    fp_image = os.path.join(image_dir[0], df_format.loc[idx, 'Fname'])
    # # If TR
    # image_dir = f"E:/tolt/ISR/{df_format.loc[idx, 'Study']}"
    # fp_image = os.path.join(image_dir, df_format.loc[idx, 'Fname'])
    if os.path.splitext(fp_image)[-1]=='.jpg':
        image = Image.open(fp_image)
        images.append(image)
        fname.append(df_format.loc[idx, 'Fname'])
        page_num.append(n)
    elif os.path.splitext(fp_image)[-1]=='.png':
        image = Image.open(fp_image)
        image = image.convert('RGB')
        images.append(image)
        fname.append(df_format.loc[idx, 'Fname'])
        page_num.append(n)
images[0].save(pdf_path, "PDF", resolution=240, save_all=True, append_images=images[1:])
# df = pd.DataFrame(np.column_stack([page_num, fname]), columns = ['page_num','file_name'])
# df.to_csv(csv)