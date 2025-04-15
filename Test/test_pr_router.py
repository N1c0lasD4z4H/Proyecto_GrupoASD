import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from Routers.pr_router import router  

# Configuración del app FastAPI para pruebas
from fastapi import FastAPI
app = FastAPI()
app.include_router(router)

client = TestClient(app)

# Prueba unitaria para el caso exitoso
@patch("Services.pr_service.GithubPRService.classify_prs")
def test_get_pr_stats_success(mock_classify_prs):
    # Simula el resultado esperado de classify_prs
    mock_classify_prs.return_value = {"etiqueta1": {"aceptadas": 5, "cambios_solicitados": 2}}

    # Realiza una solicitud al endpoint
    response = client.get("/repos/test_owner/test_repo/pulls/stats")

    # Verifica que la respuesta sea correcta
    assert response.status_code == 200
    assert response.json() == {"etiqueta1": {"aceptadas": 5, "cambios_solicitados": 2}}

 #caso de error
@patch("Services.pr_service.GithubPRService.classify_prs")
def test_get_pr_stats_failure(mock_classify_prs):
    # Simula que classify_prs lanza una excepción
    mock_classify_prs.side_effect = Exception("Error al obtener los pull requests")

    # Realiza una solicitud al endpoint
    response = client.get("/repos/test_owner/test_repo/pulls/stats")

    # Verifica que la respuesta sea un error
    assert response.status_code == 400
    assert response.json() == {"detail": "Error al obtener los pull requests"}