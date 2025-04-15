import pytest
from fastapi.testclient import TestClient
from fastapi.exceptions import HTTPException
from unittest.mock import AsyncMock, patch
from Routers.repo_activity_router import router

@pytest.fixture
def client():
    return TestClient(router)

@pytest.mark.asyncio
async def test_get_repo_activity_success(client): 
    with patch("Services.repo_activity_service.GitHubService.get_repo_activity", new_callable=AsyncMock) as mock_get_repo_activity:
        mock_get_repo_activity.return_value = [{"event": "commit", "user": "test_user"}]

        response = client.get("/test_owner/test_repo/activity", headers={"Authorization": "Bearer test_token"})

        assert response.status_code == 200
        assert response.json() == [{"event": "commit", "user": "test_user"}]

        mock_get_repo_activity.assert_called_once_with("test_owner", "test_repo", "test_token")


@pytest.mark.asyncio
async def test_get_repo_activity_no_token(client): 
    with patch("Services.repo_activity_service.GitHubService.get_repo_activity", new_callable=AsyncMock) as mock_get_repo_activity:
        mock_get_repo_activity.return_value = [{"event": "commit", "user": "test_user"}]

        response = client.get("/test_owner/test_repo/activity")

        assert response.status_code == 200  
        assert response.json() == [{"event": "commit", "user": "test_user"}]


def test_get_repo_activity_error(client, mocker):
    mock_service = mocker.patch("Services.repo_activity_service.GitHubService.get_repo_activity")
    mock_service.side_effect = Exception("Error not found repos")

    with pytest.raises(HTTPException) as exc_info:
        client.get("/test_owner/test_repo/activity", headers={"Authorization": "Bearer test_token"})

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Error not found repos"  

# Prueba cuando el servicio retorna una lista vacía
@pytest.mark.asyncio
async def test_get_repo_activity_empty_response(client):  # Aquí no necesitas declarar mock como argumento
    with patch("Services.repo_activity_service.GitHubService.get_repo_activity", new_callable=AsyncMock) as mock_get_repo_activity:
        mock_get_repo_activity.return_value = []

        response = client.get("/test_owner/test_repo/activity", headers={"Authorization": "Bearer test_token"})

        assert response.status_code == 200
        assert response.json() == []