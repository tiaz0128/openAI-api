import pytest

import os
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session", name="api_key")
def fixture_api_key():
    return os.getenv("GPT_API_KEY")
