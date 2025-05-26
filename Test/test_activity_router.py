from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from Routers.activity_router import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

@patch("Elastic.index_dispatcher.es.index", new_callable=AsyncMock)
def test_get_github_commits(mock_index):
    mock_index.return_value = {"result": "created"}

    response = client.get("/users/octocat/commits")

    assert response.status_code == 200
    assert response.json()["total_commits"] == 42
    mock_index.assert_awaited_once()
