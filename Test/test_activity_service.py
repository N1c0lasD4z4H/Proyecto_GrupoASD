import unittest
from datetime import datetime
from unittest.mock import patch, AsyncMock

from Services.activity_service import GitHubService

class TestGitHubService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.service = GitHubService()

    @patch('Services.activity_service.GitHubClient')
    async def test_get_commit_info_repo_without_name(self, mock_client_class):
        mock_client = AsyncMock()
        mock_client.get_user_repos.return_value = [{"not_name": "repo1"}]
        mock_client.get_repo_commits.return_value = []
        mock_client_class.return_value = mock_client

        resultado = await self.service.get_commit_info("user3")
        self.assertEqual(resultado["commits"], [])
    

if __name__ == '__main__':
    unittest.main()