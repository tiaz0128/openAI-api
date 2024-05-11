import os
import re
import json
import csv

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter


from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI

from constant import PROMPT_TEXT


class PdfConvertor:
    def __init__(self, llm: ChatOpenAI, pdf_path: str) -> None:
        self.llm = llm
        self.pdf_path = pdf_path

    def extract_and_parse_json(self, pdf_text):
        try:
            match = re.search(r"\{.*\}", pdf_text, re.DOTALL)
            json_string = match.group() if match else ""

            return json.loads(json_string)
        except (AttributeError, json.JSONDecodeError) as e:
            return {}

    def load_all_pdf(self):
        pdf_files = [f for f in os.listdir(self.pdf_path) if f.endswith(".pdf")]

        contents = []

        for pdf_file in pdf_files:
            loader = PyPDFLoader(os.path.join(self.pdf_path, pdf_file))
            pages = loader.load_and_split()

            prompt = PROMPT_TEXT.format(pages[0].page_content)

            result = self.llm.invoke([HumanMessage(content=prompt)])

            contents.append(self.extract_and_parse_json(result.content))

        return contents

    def write_to_csv(self, billing_data, csv_file_path):
        header = billing_data[0].keys()

        with open(csv_file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(billing_data)

    def draw_graph(self, df: pd.DataFrame):

        df["발행일"] = pd.to_datetime(
            df["발행일"]
            .str.replace(" ", "")
            .str.replace("년", "-")
            .str.replace("월", "-")
            .str.replace("일", ""),
            format="%Y-%m-%d",
        )

        fig, ax = plt.subplots()
        ax.bar(df["발행일"], df["청구금액(총액)"])
        ax.set_xlabel("date")
        ax.set_ylabel("price")
        ax.set_xticks(df["발행일"])
        ax.set_xticklabels(df["발행일"].dt.strftime("%Y-%m-%d"), rotation=45)

        ax.set_ylim(0, max(df["청구금액(총액)"]) + 100000)

        ax.get_yaxis().set_major_formatter(
            FuncFormatter(lambda x, p: format(int(x), ","))
        )

        plt.tight_layout()
        plt.show()
