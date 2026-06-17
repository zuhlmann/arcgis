from PIL import Image
import pandas as pd
import numpy as np
import os

# # Jan 2026 for Tolt QAQC figs
# # https://stackoverflow.com/questions/27327513/create-pdf-from-a-list-of-images
# study=['TR04']
# # study = [r'TR0{}'.format(i) for i in range(1,8)]
# image_dir = [f"E:/tolt/ISR/{s}" for s in study]
#
# # Step 1 CREATE INVENTORY
# # Ceate inventory of file names to copy manually into master list w/page num, caption, etc.
# # Make column name for fname = Fname
# file_ext = ['.png','.jpg']
# flist=[]
# study_list=[]
# for id, st in zip(image_dir, study):
#     flist_temp = [fn for fn in os.listdir(id) if os.path.splitext(fn)[1] in file_ext]
#     flist.extend(flist_temp)
#     study_list.extend([st]*len(flist_temp))
# df = pd.DataFrame(np.column_stack([study_list, flist]), columns=['study','Fname'])
# # Line 1 for basic, Line 2 for TR
# df.to_csv(os.path.join(image_dir[0], 'Initial_Image_List.csv'))
#
# # Step 2 CREATE THE WHOLE THING FROM FORMATTED ABOVE
# pdf_path = f"E:/tolt/ISR/{study[0]}/{study[0]}_ISR_Figures.pdf"
# csv = f"E:/tolt/ISR/{study[0]}/{study[0]}_ISR_Figure_Inventory.csv"
# # # If TR Study, uncomment
# # pdf_path = r"E:\tolt\ISR\TR_ISR_Figures.pdf"
# # csv = r"E:\tolt\ISR\TR_ISR_Figure_Inventory.csv"
# df_format=pd.read_csv(csv)

# Initially NOT function; Generalized after Tolt (April 2026 for Nuyakuk)
# Need to constrain aspect ratio in future
def generate_pdf(df, image_dir,pdf_path):
    images = []
    fname = []
    page_num = []
    for n, idx in enumerate(df.index):
        fp_image = os.path.join(image_dir, df.loc[idx, 'Fname'])
        # # For Tolt (archive)
        # # If normal
        # fp_image = os.path.join(image_dir[0], df.loc[idx, 'Fname'])
        # # # If TR
        # # image_dir = f"E:/tolt/ISR/{df_format.loc[idx, 'Study']}"
        # # fp_image = os.path.join(image_dir, df_format.loc[idx, 'Fname'])
        size = (1800,1350)
        if os.path.splitext(fp_image)[-1]=='.jpg':
            image = Image.open(fp_image)
            if image.size[0]<image.size[0]:
                image = image.rotate(90, PIL.Image.NEAREST, expand=1)
            else:
                pass
            image = image.resize(size)
            images.append(image)
            fname.append(df.loc[idx, 'Fname'])
            page_num.append(n)
        elif os.path.splitext(fp_image)[-1]=='.png':
            image = Image.open(fp_image)
            image = image.convert('RGB')
            # Maintain Aspect Ratio
            # https://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio
            base_width = 1800
            wpercent = (base_width / float(image.size[0]))
            hsize = int(float(image.size[1]) * float(wpercent))
            if image.size[0] < image.size[0]:
                image = image.rotate(90, PIL.Image.NEAREST, expand=1)
            else:
                pass
            image = image.resize((base_width, hsize), Image.Resampling.NEAREST)
            images.append(image)
            fname.append(df.loc[idx, 'Fname'])
            page_num.append(n)
    images[0].save(pdf_path, "PDF", resolution=180, save_all=True, append_images=images[1:])
    # df = pd.DataFrame(np.column_stack([page_num, fname]), columns = ['page_num','file_name'])
    # df.to_csv(csv)

csv = r"C:\Box\MCMGIS\Project_Based\Nuyakuk_Hydro\Maps\DLA_Maps\references\FERC_Figs\FERC_Figs_inv.csv"
df_format = pd.read_csv(csv)
image_dir = r"C:\Box\MCMGIS\Project_Based\Nuyakuk_Hydro\Maps\DLA_Maps\references\FERC_Figs"
pdf_path = r"C:\Box\MCMGIS\Project_Based\Nuyakuk_Hydro\Maps\DLA_Maps\references\FERC_Figs\DLA_Figs_aspect.pdf"
generate_pdf(df_format, image_dir, pdf_path)