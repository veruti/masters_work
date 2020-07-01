from summarizer import Summarizer
from document_reader.summary_reference_reader import read_string_from_xml
from document_reader.summary_reference_reader import DATA_PATH
from document_reader.summary_reference_reader import read_original_text_and_reference_from_filepath
from document_reader.summary_reference_reader import get_folderpaths

from rouge import Rouge

model = Summarizer()
rouge = Rouge()

for path in get_folderpaths(DATA_PATH):
    try:
        summary_etalon, reference = read_original_text_and_reference_from_filepath(path)
        result = model(reference, min_length=250)
        summary = ' '.join(result)

        print(rouge.get_scores(summary, summary_etalon))
    except:
        continue
