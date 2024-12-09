import sys
from core.AutoFilesXML import AutoFilesXML
from folder_analyzer import FolderAnalyzer
from colors import *

if __name__ == "__main__":
    folder_path = sys.argv[1] if len(sys.argv) > 1 else None
    folder_path_auto = FolderAnalyzer(folder_path, True)
    if folder_path:
        try:
            AutoFilesXML().both(folder_path_auto.file_list, folder_path_auto.folder[0], {"@files.xml": '.ee'})
            input(GREEN + "\nProcess Successful, press enter to exit." + RESET)
        except Exception as e:
            print(RED + f"\nError : {e}" + RESET)
            input(RED + "Process Failed, press enter to exit." + RESET)
