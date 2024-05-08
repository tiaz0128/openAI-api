import pytest

import pandas as pd

from embedding import EmbeddingCSV


class TestCovertCSV:
    @pytest.fixture(autouse=True)
    def setup(self, gpt_client, df_scraped):
        self.client = gpt_client
        self.df: pd.DataFrame = df_scraped

    def test_embedding(self):
        embedding = EmbeddingCSV(self.client, self.df)

        shortened = embedding.get_shortened_text()
        df = pd.DataFrame(shortened, columns=["content"])

        df["n_tokens"] = df.content.apply(lambda x: len(embedding.tokenizer.encode(x)))
        df["embeddings"] = df.content.apply(lambda x: embedding.get_embedding(x))

        df.to_csv(".temp/embedded.csv")
