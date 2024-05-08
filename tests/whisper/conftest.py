import pytest


@pytest.fixture(scope="session", name="wave_file")
def fixture_wave_file():
    with open(".temp/sample.m4a", "rb") as f:
        yield f


@pytest.fixture(scope="session", name="transcript")
def fixture_transcriptions():
    with open(".temp/transcriptions.txt", "r") as f:
        return f.read()
