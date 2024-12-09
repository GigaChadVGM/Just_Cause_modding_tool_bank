# this script is free to use and edit
import os
import xml.etree.ElementTree as ET
from colors import *

class AutoFilesXML:
    """
    Class that uses different functions to build a fully custom @files.xml.
    """
    def __init__(self):

        priorities = {
            ".fmod_guids": 0,
            ".ddsc": 1,
            ".hmddsc": 2,
            ".rbm": 3,
            ".lod": 4,
            ".epe": 5
        }

        def check(check_type: list, folder, files):
            if "folder content" in check_type:
                if not os.path.isdir(folder):
                    raise NotADirectoryError(RED + f"The provided path '{folder}' is not a valid directory." + RESET)

            if "single epe" in check_type:
                epe_files = [file for file in files if str(file).endswith('.epe')]
                if len(epe_files) > 1:
                    raise FileExistsError(
                        RED + f"more than one .epe file found associated to the directory external or internal: {epe_files}.\nOnly one can exist in the directory" + RESET)

            if "existing file" in check_type:
                if not files:
                    raise FileNotFoundError(
                        RED + f'Missing existing @tocFiles.xml or @files.xml, cannot proceed.' + RESET
                    )

        def main_return(files: str, og_folder: str, files_to_save: dict):
            """
            This function generates @files.xml used to create an epe.
            In this file, there are all the relative paths of each files from a certain folder.

            :param files: list of all files present in the folder.
            :param og_folder: original path of the folder.
            :param files_to_save: specifies how many files has to be saved and with which name and which extensions,
            Usage = {file_name.xml: archive_extension, ...}.
            :return: give the final files list as xml elements
            """
            global file_list_xml
            check(["folder_content", "single epe"], og_folder, files)

            def sort(path: str):
                for ext, prio in priorities.items():
                    if path.endswith(ext):
                        return 1, prio
                return 0, 0

            file_list = sorted(files, key=sort)

            for output_file, extension in files_to_save.items():
                file_list_xml = []
                root = ET.Element("files", extension=extension)

                for file in file_list:
                    file_element = ET.Element("file", name=file)
                    file_element.text = file.replace('/', '\\')
                    root.append(file_element)

                for elem in root.iter():
                    if elem.attrib.get("name"):
                        file_list_xml.append((elem.attrib.get("name", ""), elem))

                if extension:
                    ET.indent(root, space="  ", level=0)
                    tree = ET.ElementTree(root)
                    output_path = os.path.join(og_folder, output_file)

                    try:
                        tree.write(output_path, encoding="utf-8", xml_declaration=True)
                    except Exception as e:
                        raise e

            return file_list_xml


        def external_return(og_folder):
            """
            Extracts all the external paths from @files.xml and @tocFiles.xml
            
            :param og_folder: original folder_path
            :return: external paths as xml elements.
            """
            check(["folder_content"], og_folder, None)
            files_to_check = ['@tocFiles.xml', '@files.xml']
            existing_files = [file_name for file_name in files_to_check if file_name in os.listdir(og_folder)]
            check(["existing file"], None, existing_files)

            source_file = existing_files[0]
            source_file_path = os.path.join(og_folder, source_file)
            external_entries = []
            try:
                tree = ET.parse(source_file_path)
                root = tree.getroot()
                for elem in root.iter():
                    if 'size' in elem.attrib:
                        external_entries.append((elem.attrib.get("name", ""), elem))
                first_elements = [entry[0] for entry in external_entries]
                check(["single epe"], None, first_elements)
            except ET.ParseError:
                raise ValueError(RED + f"Error parsing {source_file}, ensure it is a valid XML file." + RESET)

            return external_entries


        def both_return(files, og_folder: str, files_to_save: dict):
            """
            Uses the two function above to make a @files.xml that contains everything at once.
            
            :param files: list of all files present in the folder.
            :param og_folder: original path of the folder.
            :param files_to_save: specifies how many files has to be saved and with which name and which extensions,
            Usage = {file_name.xml: archive_extension, ...}.
            """
            check(["folder_content"], og_folder, None)

            external_content = external_return(og_folder)
            internal_content = main_return(files, og_folder, {'None': None})

            global_content = external_content + internal_content

            elements = [entry[0] for entry in global_content]
            check(["single epe"], None, elements)

            def sort(entry):
                path, elem = entry
                for ext, prio in priorities.items():
                    if path.endswith(ext):
                        return 1, prio, path
                return 0, 0, path

            global_content = sorted(global_content, key=sort)

            for output_file, extension in files_to_save.items():
                root = ET.Element("files", extension=extension)
                for path, elem in global_content:
                    if elem is not None:
                        new_elem = ET.Element(elem.tag, attrib=elem.attrib)
                        new_elem.text = elem.text
                        root.append(new_elem)
                    else:
                        file_element = ET.Element("file", name=path)
                        file_element.text = path.replace('/', '\\')
                        root.append(file_element)

                ET.indent(root, space="  ", level=0)
                tree = ET.ElementTree(root)
                output_path = os.path.join(og_folder, output_file)

                try:
                    tree.write(output_path, encoding="utf-8", xml_declaration=True)
                except Exception as e:
                    raise e

        self.internal = main_return
        self.external = external_return
        self.both = both_return
