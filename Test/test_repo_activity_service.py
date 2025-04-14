import unittest
from unittest.mock import AsyncMock, patch
from datetime import datetime, timedelta
 
from Services.repo_activity_service import GitHubService
 
class TestGitHubService(unittest.IsolatedAsyncioTestCase):
 
    @patch('Services.repo_activity_service.datetime')
    def test_process_commits(self, mock_datetime):
        # Fijamos "ahora" en 2025-04-14 12:00:00
        fixed_now = datetime(2025, 4, 14, 12, 0, 0)
        mock_datetime.utcnow.return_value = fixed_now
        # Redirigimos las llamadas a strptime al datetime original
        mock_datetime.strptime.side_effect = lambda s, fmt: datetime.strptime(s, fmt)
        
        commits = [
            {
                "commit": {"author": {"date": "2025-04-07T12:00:00Z"}},
                "author": {"login": "user1"}
            },
            {
                "commit": {"author": {"date": "2025-04-10T15:00:00Z"}},
                "author": {"login": "user2"}
            }
        ]
        service = GitHubService()
        result = service._process_commits(commits)
        self.assertEqual(result["total_commits"], 2)
        self.assertEqual(result["weekly_activity"], {"user1": 1, "user2": 1})
        # Se espera que el último commit sea el de user2
        self.assertEqual(result["last_commit"], "2025-04-10T15:00:00")
 
    # Cambiamos la ruta del patch para que intercepte la creación de GitHubRequest en el namespace del módulo
    @patch('Services.repo_activity_service.GitHubRequest')
    @patch('Services.repo_activity_service.datetime')
    async def test_get_repo_activity(self, mock_datetime, MockGitHubRequest):
        fixed_now = datetime(2025, 4, 14, 12, 0, 0)
        mock_datetime.utcnow.return_value = fixed_now
        mock_datetime.strptime.side_effect = lambda s, fmt: datetime.strptime(s, fmt)
        
        # Configuramos el mock para simular la respuesta de get_commits
        mock_request = MockGitHubRequest.return_value
        mock_request.get_commits = AsyncMock(return_value=[
            {
                "commit": {"author": {"date": "2025-04-07T12:00:00Z"}},
                "author": {"login": "user1"}
            },
            {
                "commit": {"author": {"date": "2025-04-10T15:00:00Z"}},
                "author": {"login": "user2"}
            }
        ])
 
        service = GitHubService()
        result = await service.get_repo_activity("test_owner", "test_repo")
        self.assertEqual(result["total_commits"], 2)
        self.assertEqual(result["weekly_activity"], {"user1": 1, "user2": 1})
        self.assertEqual(result["last_commit"], "2025-04-10T15:00:00")
 
if __name__ == "__main__":
    unittest.main()
 