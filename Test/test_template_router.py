import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from Routers import template_router

@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(template_router.router)

    with patch("Routers.template_router.send_document", new_callable=AsyncMock):
        yield TestClient(app)

def test_check_pull_request_templates_success(client, mocker):
    # Simula respuesta con estructura correcta
    mock_service = mocker.patch("Services.template_service.FileCheckService.analyze_pull_request_template")
    mock_service.return_value = {
        "status": "success",
        "message": "Templates found",
        "user_or_org": "testuser",
        "repositories": [
            {"repository": "repo1", "has_template": True, "template_path": ".github/pull_request_template.md"},
            {"repository": "repo2", "has_template": False, "error": "Template not found"},
        ],
        "stats": {
            "total": 2,
            "with_template": 1,
            "without_template": 1
        },
        "timestamp": "2025-05-12T14:00:00Z"
    }

    response = client.get("/users/testuser/check-pull-request-templates")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["user"] == "testuser"
    assert data["stats"] == {
        "total": 2,
        "with_template": 1,
        "without_template": 1
    }
    assert data["sample_data"] == [
        {"repository": "repo1", "has_template": True, "template_path": ".github/pull_request_template.md"},
        {"repository": "repo2", "has_template": False, "error": "Template not found"}
    ]



def test_check_pull_request_templates_no_repos(client, mocker):
    #  Devuelve vacío en "repositories"
    mock_service = mocker.patch("Services.template_service.FileCheckService.analyze_pull_request_template")
    mock_service.return_value = {
        "status": "success",
        "message": "Templates found",
        "repositories": [],
        "stats": {"total": 0}
    }

    response = client.get("/users/testuser/check-pull-request-templates")
    assert response.status_code == 404
    assert response.json()["detail"] == "No repositories found to analyze"

def test_check_pull_request_templates_error_field(client, mocker):
    #  Devuelve un campo de error
    mock_service = mocker.patch("Services.template_service.FileCheckService.analyze_pull_request_template")
    mock_service.return_value = {"error": "Invalid user"}

    response = client.get("/users/testuser/check-pull-request-templates")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid user"

def test_check_pull_request_templates_exception(client, mocker):
    #  Lanza excepción inesperada
    mock_service = mocker.patch("Services.template_service.FileCheckService.analyze_pull_request_template")
    mock_service.side_effect = Exception("Service error occurred")

    response = client.get("/users/testuser/check-pull-request-templates")
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error"
