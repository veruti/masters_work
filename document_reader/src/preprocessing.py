import stanza

from copy import copy
from typing import List

SYMBOLS = ["-", "\n", "\r", "\t"]
REPLACES = ["", "", "", ""]


def preprocess_text(text: str) -> str:
    text = copy(text)

    for symbol, replace in zip(SYMBOLS, REPLACES):
        text = text.replace(symbol, replace)

    return text


def tokenize_text(text: str, language: str = "ru") -> List[str]:

    nlp = stanza.Pipeline(lang=language, processors='tokenize', use_gpu=True)
    stanza_text = nlp(text)

    tokenized_text = []
    for sentence in stanza_text.sentences:
        tokenized_text.append(sentence.text)

    return tokenized_text