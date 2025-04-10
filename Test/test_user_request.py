import unittest
from unittest.mock import patch, MagicMock
from Github_Request.user_request import GithubUserAPI


class TestGithubUserAPI(unittest.TestCase):

    @patch("Github_Request.user_request.requests.get")  # Mock del método requests.get
    def test_get_user_repos_success(self, mock_get):
        # Simula una respuesta de éxito desde la API de GitHub
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"id": 1, "name": "repo1"},
            {"id": 2, "name": "repo2"},
        ]
        mock_get.return_value = mock_response

        username = "octocat"
        repos = GithubUserAPI.get_user_repos(username)

        # Validaciones
        self.assertIsInstance(repos, list, "El resultado debe ser una lista.")
        self.assertGreater(
            len(repos), 0, "La lista de repositorios no debe estar vacía."
        )
        self.assertTrue(
            all(isinstance(repo, dict) for repo in repos),
            "Cada repositorio debe ser un diccionario.",
        )

        # Validar que se llamó correctamente la API
        mock_get.assert_called_once_with(
            f"https://api.github.com/users/{username}/repos",
            headers={"Authorization": f"Bearer {GithubUserAPI.TOKEN}"},
            params={"type": "all", "per_page": 100},
        )


if __name__ == "__main__":
    unittest.main()
