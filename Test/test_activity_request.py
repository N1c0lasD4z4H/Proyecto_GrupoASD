import pytest
import httpx
from unittest.mock import patch, MagicMock  # Eliminar AsyncMock si no lo usas
from Github_Request.activity_request import GitHubClient
 
 
@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_get_user_repos(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status = MagicMock()
    mock_response.json = MagicMock(return_value=[{"name": "repo1"}, {"name": "repo2"}])
    mock_get.return_value = mock_response
 
    client = GitHubClient()
    repos = await client.get_user_repos("usuario_test")
 
    assert isinstance(repos, list)
    assert repos[0]["name"] == "repo1"
    mock_get.assert_called_once()
 
 
@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_get_repo_commits_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status = MagicMock()
    mock_response.json = MagicMock(return_value=[{"sha": "abc123"}, {"sha": "def456"}])
    mock_get.return_value = mock_response
 
    client = GitHubClient()
    commits = await client.get_repo_commits("usuario_test", "repo_test")
 
    assert isinstance(commits, list)
    assert commits[0]["sha"] == "abc123"
    mock_get.assert_called_once()
 
 
@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_get_repo_commits_empty_repo(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 409
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Repo vacío", request=MagicMock(), response=mock_response
    )
    mock_get.return_value = mock_response
 
    client = GitHubClient()
    commits = await client.get_repo_commits("usuario_test", "empty_repo")
 
    assert commits == []