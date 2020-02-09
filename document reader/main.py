import io

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
import wordninja
import nltk


def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()


    converter.close()
    fake_file_handle.close()

    if text:
        return text


if __name__ == '__main__':
    text = extract_text_from_pdf('../data/raw/example1.pdf')
    texts = text.split('.')
    lm = wordninja.LanguageModel("dictionary.tar.gz")

    for i in texts:
            d = lm.split(i)
            if d != []:
                print(d)
