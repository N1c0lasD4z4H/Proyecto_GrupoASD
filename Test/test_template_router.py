import pytest
from fastapi.testclient import TestClient
from fastapi.exceptions import HTTPException
from Routers.template_router import router

@pytest.fixture
def client():
    return TestClient(router)

def test_check_pull_request_templates_success(client, mocker):
    # Simula la respuesta exitosa de FileCheckService
    mock_service = mocker.patch('Services.template_service.FileCheckService.analyze_pull_request_template')
    mock_service.return_value = {"status": "success", "message": "Templates found"}

    response = client.get("/users/testuser/check-pull-request-templates")

    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Templates found"}

def test_check_pull_request_templates_error(client, mocker):
    # Simular un error en FileCheckService
    mock_service = mocker.patch('Services.template_service.FileCheckService.analyze_pull_request_template')
    mock_service.side_effect = Exception("Service error occurred")
    
    with pytest.raises(HTTPException) as exc_info:
        client.get("/users/testuser/check-pull-request-templates")

    # Validar que la excepción tiene el código y detalle correctos
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Service error occurred"