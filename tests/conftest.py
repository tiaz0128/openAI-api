import pytest
import os
from dotenv import load_dotenv

from openai import OpenAI
import tweepy
from langchain_openai import ChatOpenAI
from langchain_community.utilities.google_search import GoogleSearchAPIWrapper

load_dotenv()


@pytest.fixture(scope="session", name="gpt_client")
def fixture_api_key():
    api_key = os.getenv("OPEN_API_KEY")
    return OpenAI(api_key=api_key)


@pytest.fixture(scope="session", name="twitter_client")
def fixture_twitter():
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    return tweepy.Client(
        bearer_token,
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret,
    )


@pytest.fixture(scope="session", name="messages")
def fixture_messages():
    return [
        {
            "role": "system",
            "content": "질문에 대한 답변은 항상 한 문장으로 작성해주세요.",
        },
        {
            "role": "system",
            "content": "답변은 마케터가 새로운 신간에 대한 홍보성 이벤트를 한다고 가정하고 작성해주세요.",
        },
        {
            "role": "user",
            "content": "위키북스에 새로운 신간을 소개하는 글을 작성해주세요.",
        },
    ]


@pytest.fixture(scope="session", name="google_search_client")
def fixture_google_search_client():
    google_cse_id = os.getenv("GOOGLE_CSE_ID")
    google_api_key = os.getenv("GOOGLE_API_KEY")
    return GoogleSearchAPIWrapper(
        google_cse_id=google_cse_id, google_api_key=google_api_key
    )


@pytest.fixture(scope="session", name="langchain_openai_client")
def fixture_langchain_openai_client():
    api_key = os.getenv("OPEN_API_KEY")
    return ChatOpenAI(api_key=api_key, model="gpt-3.5-turbo", max_tokens=2000)
