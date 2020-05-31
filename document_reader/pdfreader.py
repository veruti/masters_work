import stanza
import logging
import argparse

from copy import copy
from typing import List
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


SYMBOLS = ["-", "\n", "\r", "\t", u"\xa0"]
LANGUAGES = ['ru', 'en']


def preprocess_text(text: str) -> str:
    text = copy(text)

    for symbol in SYMBOLS:
        text = text.replace(symbol, " ")

    return text


def tokenize_text(text: str, language: str = "ru") -> List[str]:

    nlp = stanza.Pipeline(lang=language, processors='tokenize', use_gpu=True)
    stanza_text = nlp(text)

    tokenized_text = []
    for sentence in stanza_text.sentences:
        tokenized_text.append(sentence.text)

    return tokenized_text


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


def save_txt_file(output_path: str, tokenized_text: List[str]) -> None:

    with open(output_path, "w") as file:
        for sentence in tokenized_text:
            file.write(sentence)
            file.write("\n")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser(description='Read and save text to txt')
    parser.add_argument('--input_path', help='Path to pdf file', default=None)
    parser.add_argument('--output_path', help='Path to txt result file', default=None)
    parser.add_argument('--lang', help = "Language of text", default='en')

    arguments = parser.parse_args()

    input_path = arguments.input_path
    output_path = arguments.output_path
    language = arguments.lang

    if input_path is None:
        raise Exception("input_path is None")
    if output_path is None:
        raise Exception("Output_path is None")
    logging.info("Read text from pdf")
    text = read_text_from_pdf(input_path)

    logging.info("Preprocess text")
    text = preprocess_text(text)

    logging.info("Tokenize text")
    if language in LANGUAGES:
        tokenized_text = tokenize_text(text)
    else:
        raise Exception(f"{language} language is not supported")

    logging.info("Save files")
    save_txt_file(output_path, tokenized_text)