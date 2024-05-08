import pytest
import pandas as pd


@pytest.fixture(scope="session", name="text")
def fixture_api_key():
    with open(".temp/data.txt", "r") as f:
        return f.read()


@pytest.fixture(scope="session", name="df_scraped")
def fixture_df_scraped():
    return pd.read_csv(".temp/scraped.csv")
