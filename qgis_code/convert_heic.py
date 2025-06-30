from PIL import Image
import pillow_heif
import os

# From here 20250425
# https://stackoverflow.com/questions/63866180/how-to-convert-from-heic-to-jpg-in-python-on-windows
dir_in=r'C:\Users\ZacharyUhlmann\Documents\staging\2025-06-16'
fnames=[fn for fn in os.listdir(dir_in) if os.path.splitext(fn)[-1]=='.HEIC']
print(fnames)
files=[os.path.join(dir_in, fn) for fn in fnames]
for fp, fn in zip(files, fnames):
    heif_file = pillow_heif.read_heif(fp)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
    )
    fp_out=os.path.join(dir_in, 'converted',fn.replace('HEIC','png'))
    print(fp_out)
    image.save(fp_out, format("png"))