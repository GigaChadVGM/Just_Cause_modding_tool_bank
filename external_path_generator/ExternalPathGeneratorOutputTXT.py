import sys
from ExternalPathGenerator import ExternalPathGenerator as EPG
from folder_analyzer import FolderAnalyzer

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"


def save_as_file(path):
    try:
        text = EPG(path)
        with open('output external paths.txt', 'w', encoding='utf-8') as fichier:
            fichier.write(text)
        print(f"The file was saved successfully in the file's directory.")
    except Exception as e:
        print(f"Une erreur est survenue lors de la sauvegarde : {e}")


if __name__ == "__main__":
    paths = sys.argv[1:]
    if FolderAnalyzer(paths).exists:
        try:
            save_as_file(paths)
            input(GREEN + "\nProcess Successful, press enter to exit." + RESET)
        except Exception as e:
            print(RED + f"\nError : {e}" + RESET)
            input(RED + "Process Failed, press enter to exit." + RESET)
