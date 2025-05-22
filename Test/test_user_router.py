import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from Routers.user_rputer import router

@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)

@patch("Routers.user_rputer.send_bulk_documents", new_callable=AsyncMock)
@patch("Services.user_service.GithubUserService.get_user_repos_info", new_callable=AsyncMock)
def test_get_user_repositories_success(mock_get_repos, mock_send_bulk, client):
    mock_get_repos.return_value = [
        {
            "name": "repo1",
            "url": "https://github.com/testuser/repo1",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-02T00:00:00Z",
            "language": "Python",
            "open_issues": 3,
            "size": 120,
            "is_fork": False,
        }
    ]

    response = client.get("/users/testuser/repositories")

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    mock_send_bulk.assert_awaited_once()
