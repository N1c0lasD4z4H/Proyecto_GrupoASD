import pytest
import sys
import os
from unittest.mock import patch
 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
 
from Github_Request.user_request import GithubUserAPI
from Services.user_service import GithubUserService  
 
class TestGithubUserService:
 
    @patch.object(GithubUserAPI, 'get_user_repos')
    def test_get_user_repos_info_returns_correct_data(self, mock_get_user_repos):
        mock_repos = [
{"name": "repo1", "html_url": "https://github.com/user/repo1"},
{"name": "repo2", "html_url": "https://github.com/user/repo2"}
        ]
        mock_get_user_repos.return_value = mock_repos
 
        result = GithubUserService.get_user_repos_info("testuser")
        
        assert result == [
{"name": "repo1", "url": "https://github.com/user/repo1"},
{"name": "repo2", "url": "https://github.com/user/repo2"}
        ]
        mock_get_user_repos.assert_called_once_with("testuser")
 
        # Verificar el resultado procesado
        expected = [
{"name": "repo1", "url": "https://github.com/user/repo1"},
{"name": "repo2", "url": "https://github.com/user/repo2"}
        ]
        assert result == expected
 
    @patch.object(GithubUserAPI, 'get_user_repos')
    def test_get_user_repos_info_handles_empty_response(self, mock_get_user_repos):
        # Configurar el mock para retornar una lista vacía
        mock_get_user_repos.return_value = []
 
        result = GithubUserService.get_user_repos_info("emptyuser")
 
        mock_get_user_repos.assert_called_once_with("emptyuser")
        assert result == []
 
    @patch.object(GithubUserAPI, 'get_user_repos')
    def test_get_user_repos_info_propagates_exceptions(self, mock_get_user_repos):
        
        mock_get_user_repos.side_effect = Exception("API Error")
 
        with pytest.raises(Exception, match="API Error"):
            GithubUserService.get_user_repos_info("erroruser")
 
        mock_get_user_repos.assert_called_once_with("erroruser")