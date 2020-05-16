import argparse
import textract
import nltk
import re
import os
from typing import List

SYMBOLS = ["\n", "\r", "\t", "", u"\xa0"]


def create_extension_from_file_path(file_path: str) -> str:
    file_name_start_index = file_path.rfind(os.sep)
    file_name = file_path[file_name_start_index + 1:]

    extension_index = file_name.rfind(".")
    extension = file_name[extension_index + 1:]

    return extension


def get_text_from_file(file_path: str, language: str) -> List[str]:
    extension = create_extension_from_file_path(file_path)

    text = textract.process(file_path, extension=extension)
    text = text.decode("utf8")

    for symbol in SYMBOLS:
        text = text.replace(symbol, " ")

    text = text.lower()
    text = nltk.sent_tokenize(text, language=language)

    for num in range(len(text)):
        text[num] = re.sub(r'\(*\)', '', text[num])
        text[num] = re.sub(r'\[*\]', '', text[num])

    return text


def main():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

    file_path = '/home/max/masters_work/data/raw/example.doc'

    text = get_text_from_file(file_path, "english")

    print(type(text))


if __name__ == '__main__':
    main()