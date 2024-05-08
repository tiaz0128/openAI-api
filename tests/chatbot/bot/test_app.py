import pytest

from openai import OpenAI

from chatbot import Chatbot


class TestChatbot:
    @pytest.fixture(autouse=True)
    def setup(self, gpt_client: OpenAI, monkeypatch):
        self.gpt_client = gpt_client
        self.mock_input = monkeypatch

        self.questions = [
            "호텔에 주차장이 있나요?",
            "호텔에 피트니스 센터가 있나요?",
            "exit",
        ]
        self.chatbot = Chatbot()

    def test_chatbot(self):
        inputs = iter(self.questions)

        self.mock_input.setattr("builtins.input", lambda _: next(inputs))
        self.chatbot.qna()
