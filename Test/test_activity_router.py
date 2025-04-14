import sys
from fastapi.exceptions import HTTPException
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from Routers.activity_router import router
 
base_path = Path(__file__).resolve().parent

sys.path.append(str(base_path  / "Routers"))
 
@pytest.fixture

def client():

    return TestClient(router)
 
def test_get_github_commits_success(client, mocker):
    # Simular la respuesta del servicio GitHubService
    mock_service = mocker.patch('Routers.activity_router.GitHubService.get_commit_info')
    mock_service.return_value = {"commits": [{"sha": "123", "message": "Initial commit"}]}
 
    response = client.get("/users/testuser/commits")
 
    assert response.status_code == 200
    assert response.json() == {"commits": [{"sha": "123", "message": "Initial commit"}]}
 
def test_get_github_commits_error(client, mocker):
    # Simular un error en el servicio GitHubService
    mock_service = mocker.patch('Routers.activity_router.GitHubService.get_commit_info')
    mock_service.return_value = {"error": "User not found"}
    
    with pytest.raises(HTTPException) as exc_info:
        client.get("/users/invaliduser/commits")
        
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "User not found"

 
 
 
 