import argparse
import docx2txt
import logging

from src.preprocessing import preprocess_text, tokenize_text
from src.saver import save_txt_file


LANGUAGES = ['ru', 'en']


def read_text_from_doc_file(input_path: str):
    text = docx2txt.process(input_path)

    return text


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description='Read and save text to txt')

    parser.add_argument('--input_path', help='Path to pdf file', default=None)
    parser.add_argument('--output_path', help='Path to txt result file', default=None)
    parser.add_argument('--lang', help="Language of text", default='en')

    arguments = parser.parse_args()

    input_path = arguments.input_path
    output_path = arguments.output_path
    language = arguments.lang

    if input_path is None:
        raise Exception("input_path is None")
    if output_path is None:
        raise Exception("Output_path is None")
    logging.info("Read text from pdf")
    text = read_text_from_doc_file(input_path)

    logging.info("Preprocess text")
    text = preprocess_text(text)

    logging.info("Tokenize text")
    if language in LANGUAGES:
        tokenized_text = tokenize_text(text, language)
    else:
        raise Exception(f"{language} language is not supported")

    logging.info("Save files")
    save_txt_file(output_path, tokenized_text)
    logging.info(f"File saved to {output_path}")