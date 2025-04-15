import pytest
from fastapi.testclient import TestClient
from fastapi.exceptions import HTTPException
from Routers.user_rputer import router  
@pytest.fixture
def client(): 
    return TestClient(router)


def test_get_user_repos_success(client, mocker):
    mock_service = mocker.patch('Services.user_service.GithubUserService.get_user_repos_info') 
    mock_service.return_value =[{"name": "name", "url": "html_url"}]   
    response = client.get("/user/test_user/repos")
    
    assert response.status_code == 200
    assert response.json() == {"username": "test_user", "repos": [{"name": "name", "url": "html_url"}]}
def test_get_user_repos_not_found(client, mocker):
    mock_service = mocker.patch('Services.user_service.GithubUserService.get_user_repos_info') 
    mock_service.side_effect = Exception("User not found")
    with pytest.raises(HTTPException) as exc_info: 
        client.get("/user/invalid_user/repos")

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "User not found"