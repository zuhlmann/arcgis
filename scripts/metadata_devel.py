import xml.etree.ElementTree as ET

fp_xml = "C:\Box\MCMGIS\Project_Based\RsrcDistSantaMonicaMtns\SouthLACoConnectivityPlan\data\metadata\OwnrKing_KingCo_LandOwn_XML_scratch.xml"
tree = ET.parse(fp_xml)
# root is the root ELEMENT of a tree
root = tree.getroot()
# remove the mess in root
# Parent for idPurp
eainfo = root.find('eainfo')
eainfo.find()


fc = parameters[0]
processing_dir = r'C:\Box\MCMGIS\Project_Based\RsrcDistSantaMonicaMtns\SouthLACoConnectivityPlan\data\metadata\scratch'
xml_csv = r"C:\Box\MCMGIS\Project_Based\RsrcDistSantaMonicaMtns\SouthLACoConnectivityPlan\data\metadata\scratch\ecotopes_gis.xlsx"

fp_xml = r"C:\Box\MCMGIS\Project_Based\RsrcDistSantaMonicaMtns\SouthLACoConnectivityPlan\data\metadata\scratch\SoLaCo_Ecotopes_20260225.shp.xml"
df_xml_trans = pd.read_excel(xml_csv, index_col='attrlabl')
tree = ET.parse(fp_xml)
root = tree.getroot()
# Main nodes
eainfo = root.find('eainfo')
detailed = eainfo.find('detailed')
# If more nodes requiring updates from df add to tgt_nodes list
attr_child = detailed.findall('attr')

for c in attr_child:
if c.find('attrlabl').text == 'ECOTOP2026':
    try:
        found = []
        attrdomv_list = attr_child.findall('attrdomv')
        # This means there were no attrcomv elements
        if len(attrdomv_list)>0:
            for attrdomv in attrdomv_list:
                edomv_orig = attrdomv.find('edomv').text
                found.append(edomv_orig)
                v =df_xml_trans.loc[edomv_orig, 'edomvd']
                if not pd.isnull(v):
                    domv = ET.Element(c, 'attrdomv')
                    edom = ET.SubElement(domv,'edom')
                    edomv = ET.SubElement(edom, 'edomv')
                    edomv_val = ET.SubElement(edomv, index)
                    edomvd = ET.SubElement(edom, 'edomvd')
                    edomvd_val = ET.SubElement(edomv, v)
                    edomvds = ET.SubElement(edom, 'edomvds')
                    edomvds_val = ET.SubElement(edomvds, 'McMillen, Inc.')
                    ET.dump(domv)
            not_found = list(set(df_xml_trans.index) - set(found))
        else:
            not_found = copy.copy(df_xml_trans.index)
        for index in not_found:
            v = df_xml_trans.loc[index, 'edomvd']
            if not pd.isnull(v):
                domv = ET.Element(c, 'attrdomv')
                edom = ET.SubElement(domv, 'edom')
                edomv = ET.SubElement(edom, 'edomv')
                edomv_val = ET.SubElement(edomv, index)
                edomvd = ET.SubElement(edom, 'edomvd')
                edomvd_val = ET.SubElement(edomv, v)
                edomvds = ET.SubElement(edom, 'edomvds')
                edomvds_val = ET.SubElement(edomvds, 'McMillen, Inc.')
                # ET.dump(domv)

    except KeyError:
        logging.info('Key: {} not present in dataframe'.format(attrlabl))
        continue
    except AttributeError:
        # if NoneType --> tgt_node needs to be created and populated in xml
        print('not sure!!')
except KeyError:
    logging.info('The following Key does not have attrlabl: {}'.format(c.tag, c.attr))

tree.write(fp_xml)