import os
import platform
import xml.dom.minidom as xmldom


class XMLManager:

    @classmethod
    def xml_parse(cls, xml_path):
        xml_result_list = []
        dom_obj = xmldom.parse(xml_path)
        element_obj = dom_obj.documentElement
        box_element_obj = element_obj.getElementsByTagName("bndbox")
        for i in range(len(box_element_obj)):
            xmin = int(element_obj.getElementsByTagName("xmin")[i].firstChild.data)
            ymin = int(element_obj.getElementsByTagName("ymin")[i].firstChild.data)
            xmax = int(element_obj.getElementsByTagName("xmax")[i].firstChild.data)
            ymax = int(element_obj.getElementsByTagName("ymax")[i].firstChild.data)
            xmin = (xmin if 0 < xmin < 1920 else 0) / 1.5
            ymin = (ymin if 0 < ymin < 1080 else 0) / 1.5
            xmax = (xmax if 0 < xmax < 1920 else 1920) / 1.5
            ymax = (ymax if 0 < ymax < 1080 else 1080) / 1.5

            xml_result_list.append((xmin, ymin, xmax - xmin, ymax - ymin))
        if platform.system() == 'Windows':
            os.sep = '\\'
        return {xml_path.split(os.sep)[-1]: xml_result_list}







