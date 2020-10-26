# Get params
# script used for custom tools.  Probably will delete since can just do this
# in GUI we discovered
import os
mxd = arcpy.GetParameterAsText(0)
fp_pdf = arcpy.GetParameterAsText(1)
file_name = arcpy.GetParameterAsText(2)
file_name = '{}.pdf'.format(file_name)
page_range = arcpy.GetParameterAsText(3).upper()

# get doc and ddp objects
mxd_doc = arcpy.mapping.MapDocument(mxd)
ddp = mxd_doc.dataDrivenPages

if page_range.upper() == 'ALL':
    page_range_type = 'ALL'
    ddp.exportToPDF(os.path.join(fp_pdf, file_name), page_range_type, 'PDF_MULTILE_FILES_PAGE_INDEX')
# if seleting range
else:
    page_range_type = 'RANGE'
    ddp.exportToPDF(os.path.join(fp_pdf, file_name), page_range_type, page_range, 'PDF_MULTIPLE_FILES_PAGE_INDEX')

del mxd, mxd_doc,file_name, fp_pdf
