import unittest
from unittest.mock import patch, MagicMock
from Github_Request.template_request import GithubFileCheckAPI
import os  # Importa os para obtener variables de entorno

class TestGithubFileCheckAPI(unittest.TestCase):

    @patch("requests.get")
    def test_list_user_repositories_success(self, mock_get):
        # Configuración del mock para una respuesta exitosa
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"owner": {"login": "user1"}, "name": "repo1"},
            {"owner": {"login": "user1"}, "name": "repo2"},
        ]
        mock_get.return_value = mock_response

        # Prueba del método
        repos = GithubFileCheckAPI.list_user_repositories("user1")
        self.assertEqual(repos, ["user1/repo1", "user1/repo2"])

        # Verifica que el mock fue llamado correctamente
        mock_get.assert_called_with(
            "https://api.github.com/users/user1/repos",
            headers={'Authorization': f'Bearer {os.getenv("GITHUB_TOKEN")}'},
            params={'type': 'all', 'per_page': 100}
        )

    @patch("requests.get")
    def test_check_file_exists_success(self, mock_get):
        # Configuración del mock para una respuesta exitosa
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Prueba del método
        file_exists = GithubFileCheckAPI.check_file_exists("user1/repo1", "README.md")
        self.assertTrue(file_exists)

        # Verifica que el mock fue llamado correctamente
        mock_get.assert_called_with(
            "https://api.github.com/repos/user1/repo1/contents/README.md",
            headers={'Authorization': f'Bearer {os.getenv("GITHUB_TOKEN")}'}
        )

    @patch("requests.get")
    def test_check_file_exists_not_found(self, mock_get):
        # Configuración del mock para un archivo no encontrado
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Prueba del método
        file_exists = GithubFileCheckAPI.check_file_exists("user1/repo1", "nonexistent_file.md")
        self.assertFalse(file_exists)

        # Verifica que el mock fue llamado correctamente
        mock_get.assert_called_with(
            "https://api.github.com/repos/user1/repo1/contents/nonexistent_file.md",
            headers={'Authorization': f'Bearer {os.getenv("GITHUB_TOKEN")}'}
        )

if __name__ == "__main__":
    unittest.main()