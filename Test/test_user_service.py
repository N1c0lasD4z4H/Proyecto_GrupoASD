import pytest
from unittest.mock import patch
from Services.user_service import GithubUserService

@pytest.mark.asyncio
class TestGithubUserService:
    """Pruebas unitarias para GithubUserService.get_user_repos_info"""

    @patch("Services.user_service.GithubUserAPI.get_user_repos")
    async def test_get_user_repos_info_success(self, mock_get_user_repos):
        """Debe devolver la información procesada de los repositorios del usuario."""
        mock_get_user_repos.return_value = [
            {
                "name": "repo1",
                "html_url": "https://github.com/testuser/repo1",
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-02T12:00:00Z",
                "language": "Python",
                "open_issues_count": 5,
                "size": 12345,
                "fork": False
            },
            {
                "name": "repo2",
                "html_url": "https://github.com/testuser/repo2",
                "created_at": "2023-02-01T12:00:00Z",
                "updated_at": "2023-02-02T12:00:00Z",
                "language": "JavaScript",
                "open_issues_count": 0,
                "size": 54321,
                "fork": True
            }
        ]

        result = await GithubUserService.get_user_repos_info("testuser")

        assert len(result) == 2
        assert result[0]["name"] == "repo1"
        assert result[0]["url"] == "https://github.com/testuser/repo1"
        assert result[0]["language"] == "Python"
        assert result[0]["open_issues"] == 5
        assert result[0]["is_fork"] is False

        assert result[1]["name"] == "repo2"
        assert result[1]["url"] == "https://github.com/testuser/repo2"
        assert result[1]["language"] == "JavaScript"
        assert result[1]["open_issues"] == 0
        assert result[1]["is_fork"] is True

    @patch("Services.user_service.GithubUserAPI.get_user_repos")
    async def test_get_user_repos_info_no_repos(self, mock_get_user_repos):
        """Debe manejar correctamente cuando el usuario no tiene repositorios."""
        mock_get_user_repos.return_value = []

        result = await GithubUserService.get_user_repos_info("testuser")

        assert result == []

    @patch("Services.user_service.GithubUserAPI.get_user_repos")
    async def test_get_user_repos_info_api_error(self, mock_get_user_repos):
        """Debe manejar errores cuando la API de GitHub lanza una excepción."""
        mock_get_user_repos.side_effect = Exception("API Error")

        with pytest.raises(Exception) as excinfo:
            await GithubUserService.get_user_repos_info("testuser")

        assert str(excinfo.value) == "API Error"
