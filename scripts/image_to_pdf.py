from PIL import Image
import pandas as pd
import numpy as np
import os

# # # Jan 2026 for Tolt QAQC figs
# # # https://stackoverflow.com/questions/27327513/create-pdf-from-a-list-of-images
# # study=['TR04']
# # # study = [r'TR0{}'.format(i) for i in range(1,8)]
# # csv = os.path.join(image_dir, 'Initial_Image_List.csv')
# image_dir = r"C:\Box\MCM Projects\City of Seattle\Seattle City Light\23-024_South Fork Tolt Relicensing\11.0 Supplemental Files\Figures\USR\CR02\20261016"
# csv =  r"C:\Box\MCM Projects\City of Seattle\Seattle City Light\23-024_South Fork Tolt Relicensing\11.0 Supplemental Files\Figures\USR\CR02\20261016\CR02_Fig_Inv.csv"
# pdf_path =  r"C:\Box\MCM Projects\City of Seattle\Seattle City Light\23-024_South Fork Tolt Relicensing\11.0 Supplemental Files\Figures\USR\CR02\20261016\CR02_Figs_Compiled.pdf"
#
# # # Step 1 CREATE INVENTORY
# # fn = [fn for fn in os.listdir(image_dir) if os.path.splitext(fn)[1] in ['.jpg','.png']]
# # fp = [os.path.join(image_dir, png) for png in fn]
# # df = pd.DataFrame(np.column_stack([fn, fp]), columns=['Fname','Fpath'])
# # df.to_csv(csv)
#
# # Initially NOT function; Generalized after Tolt (April 2026 for Nuyakuk)
# # Need to constrain aspect ratio in future
# def generate_pdf(df, pdf_path):
#     images = []
#     fname = []
#     page_num = []
#     for n, idx in enumerate(df.index):
#         fp_image = df.loc[idx,'Fpath']
#         size = (1800,1350)
#         if os.path.splitext(fp_image)[-1]=='.jpg':
#             image = Image.open(fp_image)
#             if image.size[0]<image.size[0]:
#                 image = image.rotate(90, PIL.Image.NEAREST, expand=1)
#             else:
#                 pass
#             image = image.resize(size)
#             images.append(image)
#             fname.append(df.loc[idx, 'Fname'])
#             page_num.append(n)
#         elif os.path.splitext(fp_image)[-1]=='.png':
#             image = Image.open(fp_image)
#             image = image.convert('RGB')
#             # Maintain Aspect Ratio
#             # https://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio
#             base_width = 1800
#             wpercent = (base_width / float(image.size[0]))
#             hsize = int(float(image.size[1]) * float(wpercent))
#             if image.size[0] < image.size[0]:
#                 image = image.rotate(90, PIL.Image.NEAREST, expand=1)
#             else:
#                 pass
#             image = image.resize((base_width, hsize), Image.Resampling.NEAREST)
#             images.append(image)
#             fname.append(df.loc[idx, 'Fname'])
#             page_num.append(n)
#     images[0].save(pdf_path, "PDF", resolution=180, save_all=True, append_images=images[1:])
#     df = pd.DataFrame(np.column_stack([page_num, fname]), columns = ['page_num','file_name'])
#     df.to_csv(csv)
#
# # csv = os.path.join(image_dir, 'Initial_Image_List.csv')
# df_format = pd.read_csv(csv)
# # df_format = df_format[df_format['GIS_Fig']]
# # df_format.sort_values(by=['order'],inplace=True)
# # pdf_path = r"C:\Box\MCM USERS\3.0 - Employees\Hurson_Max\AQ06-Writing\Figures\ALL_zu\AQ06_Figs_PNG_Compiled.pdf"
# generate_pdf(df_format, pdf_path)

# NO RESIZE WITH TIF
# INCORPORATE SOMEDAY
# 20261023
dir_in = r"C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\data_received\project_data\ExhibitG_1984"
fp_images = [os.path.join(dir_in, f) for f in os.listdir(dir_in) if f[-4:]=='.tif']
pdf_path = r'C:\Box\MCMGIS\Project_Based\South_Fork_Tolt\data\data_received\project_data\ExhibitG_1984\renamed\test2.pdf'
images=[]

for fp_image in fp_images:
    # size = (1800,1350)
    image = Image.open(fp_image)
    # if image.size[0]<image.size[0]:
    #     image = image.rotate(90, PIL.Image.NEAREST, expand=1)
    # else:
    #     pass
    # image = image.resize(size)
    images.append(image)
images[0].save(pdf_path, "PDF", resolution=180, save_all=True, append_images=images[1:])
