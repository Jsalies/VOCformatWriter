from xml.etree import ElementTree as ET

from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def writeXML(folder,filename,path,width,height,depth,liste):
    root = ET.Element("annotation", verified="yes")
    ET.SubElement(root, "folder").text = folder
    ET.SubElement(root, "filename").text = filename
    ET.SubElement(root, "path").text = path
    source=ET.SubElement(root, "source")
    ET.SubElement(source, "database").text = "Unknown"
    size=ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = str(depth)
    ET.SubElement(root, "segmented").text = '0'

    nb_objets=len(liste)//5
    for i in range(nb_objets):
        object=ET.SubElement(root, "object")
        ET.SubElement(object, "name").text=liste[i*5]
        ET.SubElement(object, "pose").text="Unspecified"
        ET.SubElement(object, "truncated").text='0'
        ET.SubElement(object, "difficult").text='0'
        bndbox=ET.SubElement(object, "bndbox")
        ET.SubElement(bndbox, "xmin").text=str(int(liste[i*5+1]))
        ET.SubElement(bndbox, "ymin").text=str(int(liste[i*5+2]))
        ET.SubElement(bndbox, "xmax").text=str(int(liste[i*5+3]))
        ET.SubElement(bndbox, "ymax").text=str(int(liste[i*5+4]))

    return(prettify(root))