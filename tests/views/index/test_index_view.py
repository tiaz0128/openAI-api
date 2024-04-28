import pytest


class TestIndexView:
    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client

    def test_index_view(self):
        response = self.client.get("/api/v1/index")
        assert response.status_code == 200
        assert response.json() == {"Hello": "World"}
