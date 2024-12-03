import os
import sys
import xml.etree.ElementTree as ET
from folder_analyzer import FolderAnalyzer

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def ExternalPathGenerator(paths: list):
    """
    Generates a string including the selected file_path as well as its size for multiple paths.
    :param paths: list of file or directory paths
    """
    target_folder = "/dropzone/"
    return_text = ""

    for full_file_path in paths:
        normalized_path = full_file_path.replace('\\', '/').lower()
        if target_folder.lower() in normalized_path:
            index = normalized_path.find(target_folder) + len(target_folder)
            relative_path = full_file_path[index:].replace('\\', '/')
        else:
            raise ValueError(
                f"The directory '{target_folder.strip('/')}' cannot be found in '{full_file_path}'")

        file_size = os.path.getsize(full_file_path) - 128

        file_element = ET.Element("file")
        file_element.set("name", relative_path)
        file_element.set("size", str(file_size))

        xml_string = ET.tostring(file_element, encoding="unicode")
        print(xml_string)

        return_text += xml_string + '\n'
    return return_text


if __name__ == "__main__":
    paths = sys.argv[1:]
    paths_auto = FolderAnalyzer(paths)
    if paths_auto.exists:
        try:
            ExternalPathGenerator(paths_auto.file_list)
            input(GREEN + "\nProcess Successful, press enter to exit." + RESET)
        except Exception as e:
            print(RED + f"\nError : {e}" + RESET)
            input(RED + "Process Failed, press enter to exit." + RESET)
