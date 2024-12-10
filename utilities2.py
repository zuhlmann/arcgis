import os
import pandas
import PyPDF2

def aggregate_rows(self, csv_in, csv_out, group_by_field, agg_field, **kwargs):
    '''
    Groupby a field (group_by_field), aggregate all unique values in another field (agg_field)
    as a new field with values being unique values as string with commas separating values.
    20240904
    Args:
        csv_in:             path/to/csv source
        csv_out:            path/to/csv_out; can be same as csv_in
        group_by_field:     field to groupby
        agg_field:          field to create unique value comma-separated string
        kwargs:             count = include field with number of values for agg_field in csv_out

    Returns:

    '''
    df = pd.read_csv(csv_in)

    def join_list(v):
        vn = v.to_list()
        vn = list(set(vn))
        vn = ', '.join(vn)
        return (vn)

    groupby_source = df.groupby(group_by_field).agg({agg_field: join_list})
    # pulls groupby_field out of index and replaces with numbers (iloc)
    groupby_source = groupby_source.reset_index()

    try:
        # use if group_by_field is a file path and you want filename
        kwargs['extract_filename']
        fnames = [os.path.splitext(ntpath.basename(fp))[0] for fp in groupby_source[group_by_field]]
        groupby_source[group_by_field] = fnames
    except KeyError:
        pass
    try:
        kwargs['count']
        for idx in groupby_source.index:
            t = groupby_source.loc[idx, agg_field]
            t = t.split(',')
            groupby_source.loc[idx, 'NUMBER_OCCURRENCES'] = len(t)
    except KeyError:
        pass
    groupby_source = groupby_source.set_index(group_by_field)
    groupby_source.to_csv(csv_out)

def subset_PDF(df, flag,pdf_in, pdf_out):
    # https://stackoverflow.com/questions/51567750/extract-specific-pages-of-pdf-and-save-it-with-python
    from PyPDF2 import PdfFileReader, PdfFileWriter
    pdfReader = PdfFileReader(pdf_in)
    pdfWriter = PdfFileWriter()
    df_subset = df[getattr(df, flag)]

    for idx in df_subset.index:
        page_num = int(df_subset.loc[idx, 'PAGE_PDF'])
        pdfWriter.addPage(pdfReader.getPage(page_num - 1))
    with open(pdf_out, 'wb') as out:
        pdfWriter.write(pdf_out)

def images_2_pdf(image_dir, fp_pdf, ext):
    # https://stackoverflow.com/questions/27327513/create-pdf-from-a-list-of-images
    # second answer
    from PIL import Image
    if ext[0]!='.':
        ext=f".{ext}"
    else:
        pass
    fname_list = [fn for fn in os.listdir(image_dir) if os.path.splitext(fn)[-1]==ext]
    images = [Image.open(os.path.join(image_dir,f)) for f in fname_list]

    images[0].save(
        fp_pdf, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
    )