import pytest
from unittest.mock import AsyncMock,Mock, patch
from Github_Request.template_request import GithubFileCheckAPI
@pytest.mark.asyncio
class TestGithubFileCheckAPI:

    @patch("Github_Request.template_request.httpx.AsyncClient")
    async def test_list_user_repositories_success(self, mock_client_cls):
        """Debe devolver la lista de repositorios paginados."""
        mock_response_1 = AsyncMock(status_code=200)
        mock_response_1.json = Mock(return_value=[
            {"owner": {"login": "user1"}, "name": "repo1"},
            {"owner": {"login": "user1"}, "name": "repo2"}
        ])
        mock_response_1.raise_for_status = AsyncMock()

        mock_response_2 = AsyncMock(status_code=200)
        mock_response_2.json = Mock(return_value=[])
        mock_response_2.raise_for_status = AsyncMock()

        mock_client = AsyncMock()
        mock_client.get.side_effect = [mock_response_1, mock_response_2]
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        repos = await GithubFileCheckAPI.list_user_repositories("user1")
        assert repos == ["user1/repo1", "user1/repo2"]

    @patch("Github_Request.template_request.httpx.AsyncClient")
    async def test_list_user_repositories_404(self, mock_client_cls):
        """Debe lanzar un ValueError si el usuario/org no existe."""
        mock_response = AsyncMock(status_code=404, json=AsyncMock(return_value={}))
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        with pytest.raises(ValueError) as exc:
            await GithubFileCheckAPI.list_user_repositories("invaliduser")
        assert "not found" in str(exc.value)

    @patch("Github_Request.template_request.httpx.AsyncClient")
    async def test_check_file_exists_true(self, mock_client_cls):
        """Debe devolver True si el archivo existe."""
        mock_response = AsyncMock(status_code=200)
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        result = await GithubFileCheckAPI.check_file_exists("user1/repo1", "README.md")
        assert result is True

    @patch("Github_Request.template_request.httpx.AsyncClient")
    async def test_check_file_exists_false(self, mock_client_cls):
        """Debe devolver False si el archivo no existe."""
        mock_response = AsyncMock(status_code=404)
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        result = await GithubFileCheckAPI.check_file_exists("user1/repo1", "MISSING.md")
        assert result is False
