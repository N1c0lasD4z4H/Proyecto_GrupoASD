import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from Routers.repo_activity_router import router

@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)
    with patch("Routers.repo_activity_router.github_service") as mock_service, \
         patch("Routers.repo_activity_router.send_document", new_callable=AsyncMock):
        yield TestClient(app), mock_service

def test_success(client):
    test_client, mock_service = client

    mock_service.get_repo_activity = AsyncMock(return_value={
    "status": "success",
    "total_commits": 42,
    "last_commit": "2024-01-01T10:00:00Z",
    "weekly_activity": {
        "period_start": "2024-01-01T00:00:00Z",
        "period_end": "2024-01-07T00:00:00Z",
        "count_by_author": {"dev1": 10},
        "total": 10
    },
    "commit_history": [{
        "author": "dev1",
        "date": "2024-01-01T10:00:00Z",
        "message": "Initial commit",
        "sha": "abc123"
    }],
    "authors": ["dev1"]
})


    response = test_client.get("/testowner/testrepo/activity")
    assert response.status_code == 200
    assert response.json()["total_commits"] == 42

def test_repo_not_found(client):
    test_client, mock_service = client

    mock_service.get_repo_activity = AsyncMock(return_value={
        "status": "error",
        "error": "Repository not found"
    })

    response = test_client.get("/invalidowner/invalidrepo/activity")
    assert response.status_code == 404
    assert response.json()["detail"] == "Repository not found"

def test_invalid_token(client):
    test_client, mock_service = client

    mock_service.get_repo_activity = AsyncMock(return_value={
        "status": "error",
        "error": "Invalid token"
    })

    response = test_client.get("/testowner/testrepo/activity")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid GitHub token"

def test_internal_error(client):
    test_client, mock_service = client

    mock_service.get_repo_activity = AsyncMock(side_effect=Exception("DB fail"))

    response = test_client.get("/testowner/testrepo/activity")
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error"
