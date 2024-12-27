import os
import re
from hash_to_byte import *


def UsageExtractor(file, string: str):
    """
    Made to extract usage values in epes
    :param file: unique epe file to use
    :param string: Jenkins Lookup3 hash string to target in the epe
    :return: list of extracted usage values
    """
    if not file.endswith(".epe"):
        raise Exception("the provided file is not an epe")

    with open(file, "rb") as epe:
        epe_bytes = bytes(epe.read())
        epe_bytes = epe_bytes.hex().upper()

    matches = [match.start() for match in re.finditer(re.escape(string), epe_bytes)]
    results = []
    usages = []

    for index in matches:
        target = index + len(string)
        len_pos = target + 2
        lenght = int(hash_to_byte(epe_bytes[len_pos:len_pos+4]), 16)*2
        pos = target + 6
        if pos + lenght <= len(epe_bytes):
            results.append(epe_bytes[pos:pos + lenght])

        for text in results:
            usages.append(bytes.fromhex(text).decode("utf-8"))

    return usages


if __name__ == "__main__":
    final_list = []
    for root, _, files in os.walk("../epe"):   # browse through the folder
        for file in files:
            path = os.path.join(root, file)
            final_list.extend(UsageExtractor(path, "6124C74F"))   # Jenkins lookup3 hash of "Usage"

    final_list = list(set(final_list))

    for usage in final_list:
        print(usage)
