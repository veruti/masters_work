import argparse
import textract
import stanza
import nltk
import re
import os

from typing import List
from textparser import Parser

from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

SYMBOLS = ["\n", "\r", "\t", "", u"\xa0"]


def create_extension_from_file_path(file_path: str) -> str:
    file_name_start_index = file_path.rfind(os.sep)
    file_name = file_path[file_name_start_index + 1:]

    extension_index = file_name.rfind(".")
    extension = file_name[extension_index + 1:]

    return extension


def get_text_from_file(file_path: str, language: str) -> List[str]:
    extension = create_extension_from_file_path(file_path)
    encoding = "utf-8"

    text = textract.process(file_path, extension=extension, encoding=encoding)
    text = text.decode(encoding)

    for symbol in SYMBOLS:
        text = text.replace(symbol, " ")

    nlp = stanza.Pipeline(lang="ru", processors='tokenize', use_gpu=True)
    text = nlp(text)

    sentences = []
    for sentence in text.sentences:
        sentences.append(sentence.text)

    return text


def read_text_from_pdf(input_path: str) -> str:

    output_string = StringIO()
    with open(input_path, 'rb') as in_file:
        parser = PDFParser(in_file)
        document = PDFDocument(parser)
        resource_manager = PDFResourceManager()
        device = TextConverter(resource_manager, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(resource_manager, device)
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)

    text = output_string.getvalue()

    return text

def main():
    # try:
    #     nltk.data.find('tokenizers/punkt')
    # except LookupError:
    #     nltk.download('punkt')
    # stanza.download('en') 
    # stanza.download('ru') 

    file_path = '/home/max/masters_work/data/raw/rus/rus_2.pdf'
    text = get_text_from_file(file_path, "english")

    print(text)


if __name__ == '__main__':
    main()