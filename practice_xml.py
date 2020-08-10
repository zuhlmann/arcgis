import pandas as pd
import utilities
import glob
import datetime

# Editing Item Descriptions in XML
# 8/6/2020
# MAKE CLASS FOR ALL THIS!
#
# # 1)  Create Purpose string for Item Description, add to dataframe
fp_new_purp = 'C:\\Users\\uhlmann\\code\\xml_practice.txt'
fp_new_purp_csv = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Data\\item_descriptions.csv'
#
# index_col = <name of column in csv with row names i.e. filenames
df = pd.read_csv(fp_new_purp_csv, index_col = 'ITEM', na_values = 'NA')

# create string from columns with \n delimeters
purp = []
for rw in df.iterrows():
    # rw = tuple of len 2 - rw[0] = row index beginning with 0. rw[1] = series of particular row
    # so this is a series
    dict = rw[1].dropna().to_dict()
    # If purpose already created i.e. messing around with Item Description, then delete and create anew
    try:
        del(dict['PURPOSE'])
    except KeyError:
        pass
    # create list of strings i.e. ['key1: val1', 'key2: val2']
    purp_indiv = ['{}: {}'.format(key, val) for key, val in zip(dict.keys(), dict.values())]
    print(purp_indiv)
    # make string from list with \n between items
    purp_indiv = '\n'.join(purp_indiv)
    purp.append(purp_indiv)
df['PURPOSE'] = purp
pd.DataFrame.to_csv(df, fp_new_purp_csv)

# 2) Loop through XML files and update/add Purpose
import xml.etree.ElementTree as ET
p1 = 'C:\\Users\\uhlmann\\code\\practice_xml.xml'
p2 = 'C:\\Users\\uhlmann\\Box\\GIS\\Project_Based\\Klamath_River_Renewal_MJA\\GIS_Data\\McmJac_KRRP_GIS_data\\FERC_Project_Footprint_scratch2_copy2_backup.shp.xml'

df = pd.read_csv(fp_new_purp_csv)
# create file paths to shape
fp_base = df['DATA_LOCATION']
item_names = df['ITEM']
glob_strings = ['{}\\{}*.xml'.format(fp_base, item_name) for fp_base, item_name in zip(fp_base, item_names)]
fp_xml_orig = [glob.glob(glob_string)[0] for glob_string in glob_strings]
purpose_new = df['PURPOSE']

ct = 0
# fp_xml_orig = [p2]
for idx, fp_xml in enumerate(fp_xml_orig):
    print('count {}. path {}'.format(ct, fp_xml))# refer to notes below for diff betw trees and elements
    ct+=1
    tree = ET.parse(fp_xml)
    # root is the root ELEMENT of a tree
    root = tree.getroot()
    # remove the mess in root
    # Parent for idPurp
    dataIdInfo = root.find('dataIdInfo')
    # search for element <idPurp> - consult python doc for more methods. find
    # stops at first DIRECT child.  use root.iter for recursive search
    # if doesn't exist.  Add else statements for if does exist and update with dict
    purp = dataIdInfo.find('idPurp')
    if purp is not None:
        purp.text = purpose_new[idx]
        purp.set('updated', 'ZRU_{}'.format(datetime.datetime.today().strftime('%d, %b %Y')))
        print('if')
        tree.write(fp_xml)
    elif purp is None:
        # purp = purpose.text
        purp = ET.SubElement(dataIdInfo, 'idPurp')
        purp.text = purpose_new[idx]
        ET.dump(dataIdInfo)
        # OPTIONAL: this adds an attribute - a key, val pair
        purp.set('updated', 'ZRU_{}'.format(datetime.datetime.today().strftime('%d, %b %Y')))
        print('elif')
        tree.write(fp_xml)
    # # used to remove subelements made messing arounc
    # el_list = ['idTestZRU', 'idPurp']
    # for el_str in el_list:
    #     el_remove = root.find(el_str)
    #     try:
    #         root.remove(el_remove)
    #     except TypeError:
    #         pass
    # tree.write(fp_xml)

# XML NOTES
# 1) ATTRIBUTTES are useful for metadata (data about data)
# 8/6/2020
# Use attributes for Metadata (https://www.w3schools.com/xml/xml_attributes.asp):
# SEE the id="501".  GOOD IDEA
# <messages>
#     <note id="501">
#         <to>bnasty</to>
#         <from>zach</from>
#     </note>
#     note id="502">
#         <to>mom</to>
#         <from>zach</from>
#     </note>
# </messages>

# 2) TREES and ELEMENTS
# 8/6/2020
# from here: https://docs.python.org/2/library/xml.etree.elementtree.html
# XML is an inherently hierarchical data format, and the most natural way to represent it is
# with a tree. ET has two classes for this purpose - ElementTree represents the whole XML document
# as a tree, and Element represents a single node in this tree. Interactions with the whole
# document (reading and writing to/from files) are usually done on the ElementTree level.
# Interactions with a single XML element and its sub-elements are done on the Element level.

# 3)  RANDOM
# dir from ET object
# root iterates with [child for child in root] to datatype xml.etree.ElementTree.Element with dir of each element or child
# ['__class__', '__copy__', '__deepcopy__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
# '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__len__',
#'__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__setstate__',
# '__sizeof__', '__str__', '__subclasshook__', 'append', 'attrib', 'clear', 'extend', 'find', 'findall', 'findtext', 'get',
# 'getchildren', 'getiterator', 'insert', 'items', 'iter', 'iterfind', 'itertext', 'keys', 'makeelement', 'remove', 'set', 'tag', 'tail', 'text']
