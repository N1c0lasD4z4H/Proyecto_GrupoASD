import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime, timedelta, timezone
from Services.repo_activity_service import GitHubService

@pytest.mark.asyncio
class TestGitHubService:
    """Pruebas unitarias para GitHubService.get_repo_activity"""

    @patch("Services.repo_activity_service.GitHubRequest.get_commits")
    async def test_get_repo_activity_success(self, mock_get_commits):
        """Debe devolver actividad del repositorio con commits válidos."""
        mock_get_commits.return_value = [
            {
                "sha": "abc123456789",
                "commit": {
                    "author": {"date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")},

                    "message": "Initial commit"
                },
                "author": {"login": "dev1"}
            }
        ]

        service = GitHubService()
        result = await service.get_repo_activity("testowner", "testrepo")

        assert result["status"] == "success"
        assert result["repo"] == "testrepo"
        assert result["total_commits"] == 1
        assert result["weekly_activity"]["total"] >= 1
        assert len(result["commit_history"]) == 1
        assert "dev1" in result["authors"]

    @patch("Services.repo_activity_service.GitHubRequest.get_commits")
    async def test_get_repo_activity_no_commits(self, mock_get_commits):
        """Debe manejar repositorios sin commits."""
        mock_get_commits.return_value = []

        service = GitHubService()
        result = await service.get_repo_activity("testowner", "testrepo")

        assert result["status"] == "success"
        assert result["total_commits"] == 0
        assert result["weekly_activity"]["total"] == 0

    @patch("Services.repo_activity_service.GitHubRequest.get_commits")
    async def test_get_repo_activity_missing_params(self, mock_get_commits):
        """Debe manejar falta de parámetros obligatorios."""
        service = GitHubService()
        result = await service.get_repo_activity("", "testrepo")

        assert result["status"] == "error"
        assert "Owner and repo parameters are required" in result["error"]

    @patch("Services.repo_activity_service.GitHubRequest.get_commits")
    async def test_get_repo_activity_handles_exception(self, mock_get_commits):
        """Debe manejar errores internos del API."""
        mock_get_commits.side_effect = Exception("GitHub API Error")

        service = GitHubService()
        result = await service.get_repo_activity("testowner", "testrepo")

        assert result["status"] == "error"
        assert "GitHub API Error" in result["error"]
