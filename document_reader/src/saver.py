from typing import List


def save_txt_file(output_path: str, tokenized_text: List[str]) -> None:

    with open(output_path, "w") as file:
        for sentence in tokenized_text:
            file.write(sentence)
            file.write("\n")
