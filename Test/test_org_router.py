import pytest
from fastapi.testclient import TestClient
from fastapi.exceptions import HTTPException
from Routers.org_router import router

@pytest.fixture
def client():
    return TestClient(router)

def test_get_org_repos_success(client, mocker):
    # Simular respuesta exitosa de GithubOrgService
    mock_service = mocker.patch('Services.org_service.GithubOrgService.get_org_repos_info')
    mock_service.return_value = [{"name": "repo1", "description": "Test repo"}]

    response = client.get("/org/testorg/repos")

    assert response.status_code == 200
    assert response.json() == {"organization": "testorg", "repos": [{"name": "repo1", "description": "Test repo"}]}

def test_get_org_repos_error(client, mocker):
    
    mock_service = mocker.patch('Services.org_service.GithubOrgService.get_org_repos_info')
    mock_service.side_effect = Exception("Organization not found")

    with pytest.raises(HTTPException) as exc_info: 
        client.get("/org/invalidorg/repos")

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Organization not found"