import pytest


from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_community.utilities.google_search import GoogleSearchAPIWrapper
from langchain_openai import ChatOpenAI

from app import define_tools, create_prompt, write_response_to_file


class TestGoogleSearch:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        langchain_openai_client: ChatOpenAI,
        google_search_client: GoogleSearchAPIWrapper,
        monkeypatch,
    ):
        self.llm = langchain_openai_client
        self.search = google_search_client
        self.mock_input = monkeypatch

        self.theme = "라스베가스 여행"

    def test_google_search(self):
        tools = define_tools(self.search)
        prompt = create_prompt()

        agent = create_openai_tools_agent(self.llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools)

        self.mock_input.setattr("builtins.input", lambda _: self.theme)

        response = agent_executor.invoke(
            {"theme": input("기사 주제를 입력해 주세요： ")}
        )
        write_response_to_file(response["output"], ".temp/search_google.txt")
