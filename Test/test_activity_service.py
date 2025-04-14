import unittest
from unittest.mock import AsyncMock, patch
from Services.activity_service import GitHubService  

class TestGitHubService(unittest.IsolatedAsyncioTestCase):  
    @patch('Github_Request.activity_request.GitHubClient')  
    async def test_get_commit_info(self, MockGitHubClient):
        # Configuración de mocks
        mock_client = MockGitHubClient.return_value
        mock_client.get_user_repos = AsyncMock(return_value=[
            {"name": "repo1"}, {"name": "repo2"}
        ])
        mock_client.get_repo_commits = AsyncMock(side_effect=[
            [{"commit": {"author": {"date": "2023-04-01T10:00:00Z"}}}],
            []  
        ])

        # Instanciar el servicio
        service = GitHubService()
        service.github_client = mock_client  # Reemplazar el cliente por el mock

        # Ejecutar el método
        result = await service.get_commit_info("test_user")

        # Verificar resultados
        self.assertEqual(result["user"], "test_user")
        self.assertEqual(len(result["commits"]), 2)
        self.assertEqual(result["commits"][0], {
            "repo_name": "repo1",
            "total_commits": 1,
            "last_commit": "2023-04-01T10:00:00",
            "is_empty": False
        })
        self.assertEqual(result["commits"][1], {
            "repo_name": "repo2",
            "total_commits": 0,
            "last_commit": None,
            "is_empty": True
        })

        # Verificar que los métodos del cliente fueron llamados correctamente
        mock_client.get_user_repos.assert_called_once_with("test_user")
        mock_client.get_repo_commits.assert_any_call("test_user", "repo1")
        mock_client.get_repo_commits.assert_any_call("test_user", "repo2")

if __name__ == '__main__':
    unittest.main()