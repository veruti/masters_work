import textract


if __name__ == '__main__':
    text = str(textract.process('../data/raw/example1.pdf'), encoding="utf8")

    print(text)