from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from  Routers.activity_router import router
client = TestClient(router)

@patch("Elastic.index_dispatcher.es.index", new_callable=AsyncMock)
def test_get_github_commits(mock_index):
    """Simula la indexación en Elasticsearch durante el test."""
    mock_index.return_value = {"result": "created"}

    response = client.get("/users/octocat/commits")

    assert response.status_code == 200
    assert "total_commits" in response.json()
    mock_index.assert_awaited_once()
