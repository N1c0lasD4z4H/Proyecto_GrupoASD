import pytest
import httpx
from unittest.mock import AsyncMock
from Github_Request.repo_activity_request import GitHubRequest 

@pytest.mark.asyncio
async def test_get_commits():
    # Datos simulados de la API de GitHub
    simulated_commits = [{"sha": "123abc", "commit": {"message": "Initial commit"}}]

    # Función simulada para reemplazar las llamadas a httpx
    async def mock_response(request):
        if "page=1" in str(request.url):
            return httpx.Response(
                status_code=200,
                json=simulated_commits
            )
        else:
            return httpx.Response(
                status_code=200,
                json=[]
            )
    
    # Configuración del transporte simulado
    transport = httpx.MockTransport(mock_response)

    # Instancia de GitHubRequest
    github_request = GitHubRequest()

    # Sobrescribir el cliente http con transporte simulado
    github_request._paginated_get = AsyncMock(return_value=simulated_commits)

    # Ejecutar el método que estamos probando
    commits = await github_request.get_commits(
        owner="fake-owner",
        repo="fake-repo",
        token="fake-token"
    )

    assert len(commits) == len(simulated_commits)
    assert commits[0]["sha"] == "123abc"
    assert commits[0]["commit"]["message"] == "Initial commit"