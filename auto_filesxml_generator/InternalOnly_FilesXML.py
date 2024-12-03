# this script is free to use and edit
import os
import sys
import xml.etree.ElementTree as ET

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def AutoFiledXMLInternalOnly_FilesXML(folder_path: str):
    """
    This function generates one xml file @files.xml used to create an epe.
    In this file, there are all the relative paths of each files from a certain folder.

    :param folder_path: path of the folder for the @files.xml generation
    :return:
    """
    if not os.path.isdir(folder_path):
        raise NotADirectoryError(RED + f"The provided path '{folder_path}' is not a valid directory." + RESET)

    file_list = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if not file.endswith('.xml'):

                relative_path = os.path.relpath(os.path.join(root, file), start=folder_path)
                file_list.append(relative_path.replace('\\', '/'))

    epe_files = [file for file in file_list if str(file).endswith('.epe')]
    if len(epe_files) > 1:
        raise FileExistsError(
            RED + f"more than one .epe file found associated to the directory external or internal: {epe_files}.\nOnly one can exist in the directory" + RESET)

    priorites = {
        ".ddsc": 0,
        ".hmddsc": 1,
        ".rbm": 2,
        ".lod": 3,
        ".epe": 4
    }

    def sort(path: str):
        for ext, prio in priorites.items():
            if path.endswith(ext):
                return 1, prio
        return 0, 0


    file_list = sorted(file_list, key=sort)

    root = ET.Element("files", extension='.ee')

    for file in file_list:
        file_element = ET.Element("file", name=file)
        file_element.text = file.replace('/', '\\')
        root.append(file_element)

    ET.indent(root, space="  ", level=0)
    tree = ET.ElementTree(root)
    output_path = os.path.join(folder_path, '@files.xml')
    try:
        tree.write(output_path, encoding="utf-8", xml_declaration=True)
    except IOError as e:
        raise IOError(RED + f"Failed to write XML file '@files.xml': {e}" + RESET)


if __name__ == "__main__":
    folder_path = sys.argv[1] if len(sys.argv) > 1 else None
    try:
        AutoFiledXMLInternalOnly_FilesXML(folder_path)
        input(GREEN + "\nProcess Successful, press enter to exit." + RESET)
    except Exception as e:
        print(RED + f"\nError : {e}" + RESET)
        input(RED + "Process Failed, press enter to exit." + RESET)
