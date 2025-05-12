import pytest
from unittest.mock import patch, Mock
from Github_Request.pr_request import GithubPRAPI  

class TestGithubPRAPI:
    

    @patch("Github_Request.pr_request.requests.get")
    def test_make_paginated_request_single_page(self, mock_get):

        """Debe obtener los resultados de una sola página correctamente."""
        mock_response = Mock()
        mock_response.json.return_value = [{"id": 1}, {"id": 2}]
        mock_response.links = {}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = GithubPRAPI._make_paginated_request("https://api.github.com/fake")
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == 1

    @patch("Github_Request.pr_request.requests.get")
    def test_make_paginated_request_multiple_pages(self, mock_get):
        """Debe manejar múltiples páginas."""
        # Primera página
        response_page_1 = Mock()
        response_page_1.json.return_value = [{"id": 1}]
        response_page_1.links = {"next": {"url": "fake-url"}}
        response_page_1.raise_for_status = Mock()

        # Segunda página (última)
        response_page_2 = Mock()
        response_page_2.json.return_value = [{"id": 2}]
        response_page_2.links = {}
        response_page_2.raise_for_status = Mock()

        mock_get.side_effect = [response_page_1, response_page_2]

        result = GithubPRAPI._make_paginated_request("https://api.github.com/fake")
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2

    @patch("Github_Request.pr_request.GithubPRAPI._make_paginated_request")
    def test_get_repo_pull_requests(self, mock_paginated):
        """Debe llamar correctamente a la función privada con el endpoint de PRs."""
        mock_paginated.return_value = [{"id": 123}]
        result = GithubPRAPI.get_repo_pull_requests("owner", "repo")

        mock_paginated.assert_called_with(
            "https://api.github.com/repos/owner/repo/pulls",
            {"state": "all", "per_page": 100}
        )
        assert result == [{"id": 123}]

    @patch("Github_Request.pr_request.GithubPRAPI._make_paginated_request")
    def test_get_repo_labels(self, mock_paginated):
        """Debe llamar correctamente a la función privada con el endpoint de etiquetas."""
        mock_paginated.return_value = [{"name": "bug"}]
        result = GithubPRAPI.get_repo_labels("owner", "repo")

        mock_paginated.assert_called_with(
            "https://api.github.com/repos/owner/repo/labels",
            {"per_page": 100}
        )
        assert result == [{"name": "bug"}]
