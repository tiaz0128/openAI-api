import pandas as pd
import tiktoken


class EmbeddingCSV:
    def __init__(self, client, df: pd.DataFrame):
        self.client = client
        self.df: pd.DataFrame = df

        self.embedding_model = "text-embedding-3-small"
        self.embedding_encoding = "cl100k_base"
        self.max_tokens = 1500

        self.tokenizer: tiktoken.Encoding = tiktoken.get_encoding(
            self.embedding_encoding
        )
        self.set_n_tokens()

    def set_n_tokens(self):
        self.df.columns = ["fname", "content"]

        self.df["n_tokens"] = self.df.content.apply(
            lambda x: len(self.tokenizer.encode(x))
        )

    def get_shortened_text(self) -> list[str]:
        shortened = []

        for row in self.df.iterrows():
            if row[1]["content"] is None:
                continue

            if row[1]["n_tokens"] > self.max_tokens:
                shortened += self.split_into_many(row[1]["content"], self.max_tokens)
            else:
                shortened.append(row[1]["content"])
        return shortened

    def get_embedding(self, text):
        text = text.replace("\n", " ")

        return (
            self.client.embeddings.create(input=[text], model=self.embedding_model)
            .data[0]
            .embedding
        )

    def split_into_many(self, text, max_tokens=150):
        sentences = text.split(".")
        n_tokens = [
            len(self.tokenizer.encode(" " + sentence)) for sentence in sentences
        ]

        chunks = []
        tokens_so_far = 0
        chunk = []

        for sentence, token in zip(sentences, n_tokens):
            if tokens_so_far + token > max_tokens:
                chunks.append(". ".join(chunk) + ".")
                chunk = []
                tokens_so_far = 0

            if token > max_tokens:
                continue

            chunk.append(sentence)
            tokens_so_far += token + 1

        if chunk:
            chunks.append(". ".join(chunk) + ".")
        return chunks
