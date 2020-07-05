from os import sep
from os import listdir
import re
from copy import copy
import xml.etree.ElementTree as ET

# Typings
from typing import Tuple
from typing import List


# Main constants

DATA_PATH = "/home/developer/Desktop/masters_work/data/scisumm-corpus/data/Training-Set-2018/"
REFERENCE_FILE_NAME = "Reference_XML"
SUMMARY_FILE_NAME = "summary"


def read_string_from_xml(filepath: str) -> str:
    tree = ET.parse(filepath)
    string = ET.tostring(tree.getroot(), encoding='utf-8', method='text').decode("utf-8")
    string = " ".join(string.split())

    return string


def read_summary(fileapth: str) -> str:
    with open(fileapth, 'r') as file:
        summary = ""
        for string in file:
            index_start = string.find(">") + 1
            index_end = string.rfind("<")

            summary += string[index_start: index_end] + " "

        return summary


def read_original_text_and_reference_from_filepath(filepath: str) -> Tuple[str, str]:
    local_filepath = copy(filepath)
    if filepath.endswith(sep):
        filename = local_filepath.split(sep)[-2]
        local_filepath = local_filepath[:-1]
    else:
        filename = local_filepath.split(sep)[-1]

    summary_filename = f"{filename}.community"
    summary_filenames = listdir(local_filepath + sep + SUMMARY_FILE_NAME)

    for name in summary_filenames:
        if summary_filename in name:
            summary_filename = name
            break

    reference_filename = f"{filename}.xml"

    summary_filepath = sep.join([local_filepath, SUMMARY_FILE_NAME, summary_filename])
    reference_filepath = sep.join([local_filepath, REFERENCE_FILE_NAME, reference_filename])

    summary = read_summary(summary_filepath)
    reference = read_string_from_xml(reference_filepath)

    summary = re.sub(r'\<.*?\>', '', summary)
    reference = re.sub(r'\<.*?\>', '', reference)

    return summary, reference


def get_folderpaths(datapath: str) -> List:
    list_dir = listdir(datapath)
    list_paths = []

    for folder_name in list_dir:
        list_paths.append(datapath + folder_name + sep)

    return list_paths


if __name__ == '__main__':
    # summary, reference = read_original_text_and_reference_from_filepath(DATA_PATH)
    for path in get_folderpaths(DATA_PATH):
        try:
            print(read_original_text_and_reference_from_filepath(path))
        except:
            pass