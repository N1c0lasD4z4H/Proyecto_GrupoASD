import pytest
from unittest.mock import AsyncMock, patch
from Services.template_service import FileCheckService
from datetime import datetime, timezone

@pytest.mark.asyncio
class TestFileCheckService:
    """Pruebas unitarias para FileCheckService.analyze_pull_request_template"""

    @patch("Services.template_service.GithubFileCheckAPI.list_user_repositories")
    @patch("Services.template_service.GithubFileCheckAPI.check_file_exists")
    async def test_analyze_pull_request_template_success(self, mock_check_file_exists, mock_list_repos):
        """Debe analizar los repositorios y verificar plantillas con éxito."""
        mock_list_repos.return_value = ["repo1", "repo2", "repo3"]
        mock_check_file_exists.side_effect = lambda repo, path: repo == "repo1" and path == ".github/PULL_REQUEST_TEMPLATE.md"

        result = await FileCheckService.analyze_pull_request_template("testuser")

        assert result["user_or_org"] == "testuser"
        assert result["stats"]["total"] == 3
        assert result["stats"]["with_template"] == 1
        assert result["stats"]["without_template"] == 2
        assert len(result["repositories"]) == 3
        assert result["repositories"][0]["repository"] == "repo1"
        assert result["repositories"][0]["has_template"] is True
        assert result["repositories"][0]["template_path"] == ".github/PULL_REQUEST_TEMPLATE.md"
        assert result["repositories"][1]["has_template"] is False
        assert result["repositories"][2]["has_template"] is False

    @patch("Services.template_service.GithubFileCheckAPI.list_user_repositories")
    async def test_analyze_pull_request_template_no_repositories(self, mock_list_repos):
        """Debe manejar usuarios sin repositorios."""
        mock_list_repos.return_value = []

        result = await FileCheckService.analyze_pull_request_template("testuser")

        assert result["user_or_org"] == "testuser"
        assert result["message"] == "No repositories found"
        assert result["repositories"] == []

    @patch("Services.template_service.GithubFileCheckAPI.list_user_repositories")
    async def test_analyze_pull_request_template_error_list_repos(self, mock_list_repos):
        """Debe manejar errores al listar repositorios."""
        mock_list_repos.side_effect = Exception("API Error")

        result = await FileCheckService.analyze_pull_request_template("testuser")

        assert result["user_or_org"] == "testuser"
        assert "error" in result
        assert result["error"] == "API Error"

    @patch("Services.template_service.GithubFileCheckAPI.list_user_repositories")
    @patch("Services.template_service.GithubFileCheckAPI.check_file_exists")
    async def test_analyze_pull_request_template_error_check_file(self, mock_check_file_exists, mock_list_repos):
        """Debe manejar errores al verificar archivos en repositorios individuales."""
        mock_list_repos.return_value = ["repo1", "repo2"]

        def mock_side_effect(repo, path):
            if repo == "repo2":
                raise Exception("File check error")
            return False

        mock_check_file_exists.side_effect = mock_side_effect

        result = await FileCheckService.analyze_pull_request_template("testuser")

        assert result["stats"]["total"] == 2
        assert result["stats"]["with_template"] == 0
        assert result["stats"]["without_template"] == 2
        assert result["repositories"][1]["error"] == "File check error"
