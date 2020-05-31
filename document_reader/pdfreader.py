import stanza
from typing import List
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


from copy import copy

SYMBOLS = ["-", "\n", "\r", "\t", "", u"\xa0"]


def preprocess_text(text: str) -> str:
    text = copy(text)

    for symbol in SYMBOLS:
        text = text.replace(symbol, " ")

    return text


def tokenize_text(text: str) -> List[str]:

    nlp = stanza.Pipeline(lang="ru", processors='tokenize', use_gpu=True)
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
    input_path = '/home/max/masters_work/data/raw/rus/rus_2.pdf'
    output_path = '/home/max/masters_work/data/raw/rus/rus_2.txt'

    text = read_text_from_pdf(input_path)
    text = preprocess_text(text)
    tokenized_text = tokenize_text(text)
    save_txt_file(output_path, tokenized_text)

    print(tokenized_text)
