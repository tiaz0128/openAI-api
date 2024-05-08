import pytest
from covert_csv import CovertCSV


class TestCovertCSV:
    @pytest.fixture(autouse=True)
    def setup(self, text):
        self.text = text

    def test_convert_text_to_csv(self):
        covert = CovertCSV(self.text)
        df = covert.convert_text_to_df()
        df.to_csv(".temp/scraped.csv", index=False, encoding="utf-8")
