import numpy as np
import pandas as pd
from scipy import spatial


class Chatbot:
    def qna(self):
        conversation_history = []

        while True:
            user_input = input("질문을 입력하세요:")

            if user_input == "exit":
                break

            conversation_history.append({"role": "user", "content": user_input})

            answer = self.answer_question(user_input, conversation_history)

            conversation_history.append({"role": "assistant", "content": answer})

            with open(".temp/chatbot.txt", "a") as f:
                f.write(f"질문: {user_input}\n답변: {answer}\n\n")

    def create_context(self, question, df, max_length=1800):
        q_embedding = (
            self.gpt_client.embeddings.create(
                input=[question], model="text-embedding-3-small"
            )
            .data[0]
            .embedding
        )

        df["distances"] = self.distances_from_embedding(
            q_embedding,
            df["embeddings"].apply(eval).apply(np.array).values,
            distance_metic="cosine",
        )

        returns = []
        cur_len = 0
        for _, row in df.sort_values("distances", ascending=True).iterrows():
            cur_len += row["n_tokens"] + 4
            if cur_len > max_length:
                break

            returns.append(row["content"])

        return "\n\n##\n\n".join(returns)

    def answer_question(self, question, conversation_history):
        df = pd.read_csv(".temp/embedded.csv")
        context = self.create_context(question, df, max_length=200)

        prompt = f"당신은 호텔 직원입니다. \n\n컨텍스트: {context}\n\n질문: {question}\n\n답변: {question}\n\n"
        conversation_history.append({"role": "user", "content": prompt})

        try:
            response = self.gpt_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation_history,
                temperature=1,
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            print(e)
            return ""

    def distances_from_embedding(
        self, q_embedding, embeddings, distance_metic="cosine"
    ):
        distance_metics = {
            "cosine": spatial.distance.cosine,
            "L1": spatial.distance.cityblock,
            "L2": spatial.distance.euclidean,
            "Linf": spatial.distance.chebyshev,
        }

        return [
            distance_metics[distance_metic](q_embedding, embedding)
            for embedding in embeddings
        ]
