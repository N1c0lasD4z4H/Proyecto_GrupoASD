import pytest
from unittest.mock import AsyncMock, Mock, patch
from Github_Request.repo_activity_request import GitHubRequest

@pytest.mark.asyncio
class TestGitHubRequest:

    @patch("Github_Request.repo_activity_request.httpx.AsyncClient")
    async def test_paginated_get_multiple_pages(self, mock_client_cls):
        """Debe manejar múltiples páginas correctamente."""
        mock_response_1 = AsyncMock(status_code=200)
        mock_response_1.json = Mock(return_value=[{"sha": "abc123"}])
        mock_response_1.headers = {'link': '<https://api.github.com/page2>; rel="next"'}

        mock_response_2 = AsyncMock(status_code=200)
        mock_response_2.json = Mock(return_value=[{"sha": "def456"}])
        mock_response_2.headers = {}

        mock_client = AsyncMock()
        mock_client.get.side_effect = [mock_response_1, mock_response_2]
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        request = GitHubRequest()
        results = await request._paginated_get("https://api.github.com/repos/test/commits", {})

        assert len(results) == 2
        assert results[0]["sha"] == "abc123"
        assert results[1]["sha"] == "def456"

    @patch("Github_Request.repo_activity_request.httpx.AsyncClient")
    async def test_get_commits_success(self, mock_client_cls):
        """Debe obtener commits correctamente."""
        mock_response = AsyncMock(status_code=200)
        mock_response.json = Mock(return_value=[{"sha": "abc123"}])
        mock_response.headers = {}
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        request = GitHubRequest()
        commits = await request.get_commits("owner", "repo")

        assert isinstance(commits, list)
        assert commits[0]["sha"] == "abc123"

    async def test_get_commits_missing_params(self):
        """Debe lanzar error si faltan parámetros obligatorios."""
        request = GitHubRequest()
        with pytest.raises(ValueError):
            await request.get_commits("", "repo")

    @patch("Github_Request.repo_activity_request.httpx.AsyncClient")
    async def test_paginated_get_unexpected_response_format(self, mock_client_cls):
        """Debe lanzar excepción si la respuesta no es una lista."""
        mock_response = AsyncMock(status_code=200)
        mock_response.json = Mock(return_value={"message": "not a list"})
        mock_response.headers = {}

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        request = GitHubRequest()
        with pytest.raises(Exception, match="Unexpected response format"):
            await request._paginated_get("https://api.github.com/repos/test/commits", {})
