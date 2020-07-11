# Metrics
from rouge import Rouge

# Sumy imports
from sumy.summarizers.lsa import LsaSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

# xml_reader
from document_reader.summary_reference_reader import read_string_from_xml
from document_reader.summary_reference_reader import DATA_PATH
from document_reader.summary_reference_reader import read_original_text_and_reference_from_filepath
from document_reader.summary_reference_reader import get_folderpaths

# Typings
from typing import Dict

# Progress bar
from progressbar import progressbar

# Errors
from xml.etree.ElementTree import ParseError


LANGUAGE = "english"
SENTENCES_COUNT = 15

scorer = Rouge()


if __name__ == '__main__':
    summary_references = []
    summaries = []

    folder_paths = get_folderpaths(DATA_PATH)
    n_folders = len(folder_paths)

    for n_paper in progressbar(range(n_folders)):
        path = folder_paths[n_paper]

        try:
            summary_reference, reference = read_original_text_and_reference_from_filepath(path)
        except ParseError:
            continue
        except FileNotFoundError:
            continue

        parser = PlaintextParser.from_string(reference, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)
        summarizer = LsaSummarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)

        summary = ""
        for sentence in summarizer(parser.document, SENTENCES_COUNT):
            summary += str(sentence) + " "

        summary_references.append(summary_reference)
        summaries.append(summary)

    metrics = scorer.get_scores(summaries, summary_references, avg=True)
    print(metrics)