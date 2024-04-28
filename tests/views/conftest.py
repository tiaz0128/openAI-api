from fastapi.testclient import TestClient
from main import app  # main.py 파일에서 FastAPI 애플리케이션을 import
import pytest


@pytest.fixture(name="client")
def fixture_client():
    return TestClient(app)
