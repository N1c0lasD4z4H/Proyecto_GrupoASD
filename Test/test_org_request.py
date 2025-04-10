import unittest
from unittest.mock import patch, MagicMock
import requests
from Github_Request.org_request import GithubOrgAPI  # Importación correcta del módulo real
 
class TestGithubOrgAPI(unittest.TestCase):
 
    @patch("Github_Request.org_request.requests.get")  # Ruta completa al requests.get usado dentro de org_request
    def test_get_org_repos_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"name": "repo1", "id": 1},
            {"name": "repo2", "id": 2},
        ]
        mock_get.return_value = mock_response
 
        org_name = "testorg"
        repos = GithubOrgAPI.get_org_repos(org_name)
 
        self.assertEqual(len(repos), 2)
        self.assertEqual(repos[0]["name"], "repo1")
        self.assertEqual(repos[1]["name"], "repo2")
        mock_get.assert_called_once_with(
f"https://api.github.com/orgs/{org_name}/repos",
            headers={"Authorization": f"Bearer {GithubOrgAPI.TOKEN}"},
            params={"type": "all", "per_page": 100},
        )
 
    @patch("Github_Request.org_request.requests.get")
    def test_get_org_repos_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Not Found")
        mock_get.return_value = mock_response
 
        org_name = "invalidorg"
        with self.assertRaises(requests.exceptions.HTTPError):
            GithubOrgAPI.get_org_repos(org_name)
 
        mock_get.assert_called_once()
 
if __name__ == "__main__":
    unittest.main()