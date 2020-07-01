# Metrics
from rouge import Rouge

# Sumy imports
from sumy.summarizers.kl import KLSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

# xml_reader
from document_reader.summary_reference_reader import read_string_from_xml
from document_reader.summary_reference_reader import DATA_PATH
from document_reader.summary_reference_reader import read_original_text_and_reference_from_filepath
from document_reader.summary_reference_reader import get_folderpaths

LANGUAGE = "english"
SENTENCES_COUNT = 15

rouge = Rouge()

for path in get_folderpaths(DATA_PATH):
    try:
        summary_reference, reference = read_original_text_and_reference_from_filepath(path)
        parser = PlaintextParser.from_string(reference, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)

        summarizer = KLSummarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)

        summary = ""
        for sentence in summarizer(parser.document, SENTENCES_COUNT):
            summary += str(sentence) + " "

        print(rouge.get_scores(summary, reference))
    except:
        pass
