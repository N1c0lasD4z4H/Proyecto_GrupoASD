import unittest
import sys
import os
from unittest.mock import patch
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Github_Request.template_request import GithubFileCheckAPI
from Services.template_service import FileCheckService

class TestFileCheckService(unittest.TestCase):

    @patch.object(GithubFileCheckAPI, 'list_user_repositories')
    @patch.object(GithubFileCheckAPI, 'check_file_exists')
    def test_analyze_pull_request_template(self, mock_check_file_exists, mock_list_user_repositories):
        # Simular repositorios de usuario u organización
        mock_list_user_repositories.return_value = ["repo1", "repo2", "repo3"]

        # Simular archivos existentes en algunos repositorios
        def mock_check(repo, path):
            return repo == "repo1"  # Solo repo1 tiene el archivo

        mock_check_file_exists.side_effect = mock_check

        # Llamar al método de prueba
        result = FileCheckService.analyze_pull_request_template("example_user")

        # Verificaciones
        self.assertEqual(result["has_template"], ["repo1"])
        self.assertEqual(result["missing_template"], ["repo2", "repo3"])
        self.assertEqual(result["count_has_template"], 1)
        self.assertEqual(result["count_missing_template"], 2)
        

if __name__ == '__main__':
    unittest.main()