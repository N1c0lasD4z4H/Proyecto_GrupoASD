import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from Routers.user_rputer import router

@pytest.fixture
def client(mocker):
    # Mock de GithubUserService
    mock_service = mocker.patch("Services.user_service.GithubUserService.get_user_repos_info")
    
    # Mock completo del Elasticsearch
    mock_es = mocker.patch("Elastic.index_dispatcher.es")
    mock_es.index = AsyncMock(return_value={"_id": "test_id"})  # Simula respuesta exitosa
    
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router)
    return TestClient(app), mock_service, mock_es

def test_get_user_repositories_success(client):
    test_client, mock_service, mock_es = client

    # Configurar el mock del servicio
    mock_service.return_value = [
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

    response = test_client.get("/users/testuser/repositories")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    
    # Verificar que se llamó a Elasticsearch
    mock_es.index.assert_awaited_once()

def test_get_user_repositories_not_found(client):
    test_client, mock_service, _ = client

    # Simular que el usuario no tiene repositorios
    mock_service.return_value = []

    response = test_client.get("/users/testuser/repositories")
    assert response.status_code == 404
    assert response.json()["detail"] == "No se encontraron repositorios para el usuario testuser"

def test_get_user_repositories_internal_error(client):
    test_client, mock_service, _ = client

    # Simular que el servicio lanza una excepción inesperada
    mock_service.side_effect = Exception("Unexpected error")

    response = test_client.get("/users/testuser/repositories")
    assert response.status_code == 500
    assert response.json()["detail"] == "Error procesando repositorios"