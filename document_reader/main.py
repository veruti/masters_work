import textract
import nltk

SYMBOLS = ["\n", "\x0c", "\x0b", "\r", "\t", ""]


def get_text_from_pdf(filepath):
    text_ = str(textract.process(filepath), encoding="utf8")
    for symbol in SYMBOLS:
        text_ = text_.replace(symbol, " ")

    text_ = text_.lower()
    return text_


if __name__ == '__main__':
    nltk.download("punkt")
    text = get_text_from_pdf('../data/raw/example1.pdf')

    print(nltk.sent_tokenize(text, language='english'))
