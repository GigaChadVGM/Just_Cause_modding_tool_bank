import os
from colors import *

class FolderAnalyzer:
    def __init__(self, paths, paths_type: str, is_xml_generator: bool = False):
        """
        Class that gives all the files without folders in a selection of folders
        :param paths: path of one or many folders
        """
        if not paths:
            raise Exception(RED + "No files or directories were provided." + RESET)
        else:
            if paths_type == "folder":
                if not os.path.isdir(paths):
                    self.exists = False
                    raise NotADirectoryError(RED + "The provided path is not a directory." + RESET)

            elif paths_type == "file":
                if not os.path.isfile(paths):
                    self.exists = False
                    raise FileNotFoundError(RED + "The provided path is not a file." + RESET)

            elif paths_type == "multiple":
                # means that all the provided paths are files and folders, the check will always be true
                pass

        paths = paths if isinstance(paths, list) else [paths]

        self.folder = []

        list_paths = []
        for element in paths:
            if os.path.isdir(element):
                self.folder.append(element)
                if element in list_paths:
                    list_paths.remove(element)
                for root_dir, _, files in os.walk(element):
                    for file in files:
                        if is_xml_generator:
                            if not file.endswith('.xml'):
                                relative_path = os.path.relpath(os.path.join(str(root_dir), file), start=element)
                                list_paths.append(relative_path.replace('\\', '/'))
                        else:
                            list_paths.append(os.path.join(root_dir, file))
            else:
                list_paths.append(element)

            self.file_list = list_paths

            for sub_element in list_paths:
                self.final_file = sub_element
