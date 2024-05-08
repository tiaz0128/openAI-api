import pandas as pd
import re


class CovertCSV:
    def __init__(self, text):
        self.text = text

    def remove_newlines(self, text):
        text = re.sub(r"\n", " ", text)
        text = re.sub(r" +", " ", text)

        return text

    def convert_text_to_df(self) -> pd.DataFrame:
        texts = []

        sections = self.text.split("\n\n")

        for section in sections:
            lines = section.split("\n")

            fname = lines[0]

            content = " ".join(lines[1:])
            texts.append([fname, content])

        df = pd.DataFrame(texts, columns=["filename", "content"])

        df["content"] = df["content"].apply(self.remove_newlines)

        return df
