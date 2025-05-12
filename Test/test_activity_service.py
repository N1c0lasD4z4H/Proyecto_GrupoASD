import pytest
import sys
import os
from unittest.mock import AsyncMock, patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Services.activity_service import GitHubService

@pytest.mark.asyncio
class TestGitHubService:

    async def test_get_commit_info_success(self):
        #devolver los datos de commits correctamente cuando hay repos y commits
        with patch("Services.activity_service.GitHubClient") as MockClient:
            mock_client = MockClient.return_value
            mock_client.get_user_repos = AsyncMock(return_value=[
                {"name": "repo1"},
                {"name": "repo2"}
            ])
            mock_client.get_repo_commits = AsyncMock(side_effect=[
                [
                    {"commit": {"author": {"username": "dev1", "date": "2023-01-01T12:00:00Z"}}},
                    {"commit": {"author": {"username": "dev2", "date": "2023-01-02T12:00:00Z"}}}
                ],
                []
            ])

            service = GitHubService()
            result = await service.get_commit_info("testuser")

            assert result["user"] == "testuser"
            assert result["total_repos"] == 2
            assert result["repos_with_commits"] == 1
            assert result["total_commits"] == 2
            assert not result["commits"][0]["is_empty"]

    async def test_get_commit_info_empty_repos(self):
        #Debe devolver valores por defecto cuando no hay repositorios
        with patch("Services.activity_service.GitHubClient") as MockClient:
            mock_client = MockClient.return_value
            mock_client.get_user_repos = AsyncMock(return_value=[])

            service = GitHubService()
            result = await service.get_commit_info("testuser")

            assert result["total_repos"] == 0
            assert result["commits"] == []

    async def test_get_commit_info_with_missing_repo_name(self):
        #omitir repositorios sin nombre
        with patch("Services.activity_service.GitHubClient") as MockClient:
            mock_client = MockClient.return_value
            mock_client.get_user_repos = AsyncMock(return_value=[{"id": 1}])

            service = GitHubService()
            result = await service.get_commit_info("testuser")
            assert result["commits"] == []

    async def test_get_commit_info_handles_exception(self):
        #manejar excepciones y devolver un error
        with patch("Services.activity_service.GitHubClient") as MockClient:
            mock_client = MockClient.return_value
            mock_client.get_user_repos = AsyncMock(side_effect=Exception("Test error"))

            service = GitHubService()
            result = await service.get_commit_info("testuser")

            assert "error" in result
            assert "Test error" in result["error"]
