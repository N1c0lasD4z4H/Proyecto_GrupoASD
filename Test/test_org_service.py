import unittest
from unittest.mock import patch
from Github_Request.org_request import GithubOrgAPI
from Services.org_service import GithubOrgService  

class TestGithubOrgService(unittest.TestCase):
    @patch('Github_Request.org_request.GithubOrgAPI.get_org_repos')
    def test_get_org_repos_info(self, mock_get_org_repos):
        # Datos de prueba simulados
        mock_repos = [
            {"name": "repo1", "html_url": "https://github.com/org/repo1"},
            {"name": "repo2", "html_url": "https://github.com/org/repo2"}
        ]
        mock_get_org_repos.return_value = mock_repos

        # Llamar al método bajo prueba
        org_name = "org"
        repos_info = GithubOrgService.get_org_repos_info(org_name)

        # Verificar los resultados
        expected_result = [
            {"name": "repo1", "url": "https://github.com/org/repo1"},
            {"name": "repo2", "url": "https://github.com/org/repo2"}
        ]
        self.assertEqual(repos_info, expected_result)

if __name__ == '__main__':
    unittest.main()