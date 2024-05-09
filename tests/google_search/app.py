from langchain.agents import Tool
from langchain_community.utilities.google_search import GoogleSearchAPIWrapper
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def define_tools(search: GoogleSearchAPIWrapper):
    return [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to answer questions about current events. You should ask targeted questions",
        ),
    ]


def create_prompt():
    template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "당신은 뉴스 기사를 쓰는 블로거입니다. 다음 주제에 대해 구글 검색을 통해 최신 정보를 얻고, 그 정보를 바탕으로 뉴스 기사를 작성해 주세요. 1000자 이상, 한국어로 출력해 주세요. 기사 말미에 참고한 URL을 참조 출처로 제목과 URL을 출력해 주세요.",
            ),
            ("human", "{theme}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )
    return template


def write_response_to_file(response, filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(response)
    print("출력이 완료되었습니다")
