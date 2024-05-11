import pytest
import json
import pandas as pd

from langchain_openai import ChatOpenAI

from app import PdfConvertor


class TestExtractPdfAndParseJson:
    @pytest.fixture(autouse=True)
    def setup(self, langchain_openai_client: ChatOpenAI):
        pdf_path = "./tests/pdf/raw_data"

        self.convertor = PdfConvertor(langchain_openai_client, pdf_path)

    def test_convert_pdf(self):
        result = self.convertor.load_all_pdf()

        with open(".temp/pdf.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    def test_covert_csv(self):

        with open(".temp/pdf.json", "r") as f:
            data = json.load(f)

        self.convertor.write_to_csv(data, ".temp/billing.csv")

    def test_csv_graph(self):
        csv_file = ".temp/billing.csv"
        df = pd.read_csv(csv_file, thousands=",")

        self.convertor.draw_graph(df)
