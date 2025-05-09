import pytest
from unittest.mock import patch
from datetime import datetime
from Services.pr_service import GithubPRService

class TestGithubPRService:
    """Pruebas unitarias para GithubPRService.classify_prs"""

    @patch("Services.pr_service.GithubPRAPI.get_repo_pull_requests")
    def test_classify_prs_with_labels_and_merge(self, mock_get_prs):
        """Debe clasificar correctamente los PRs con etiquetas y merge."""
        mock_get_prs.return_value = [
            {
                "id": 1,
                "number": 101,
                "title": "Fix bug",
                "html_url": "http://github.com/test/repo/pull/101",
                "merged_at": "2023-01-01T12:00:00Z",
                "labels": [{"name": "bug"}, {"name": "urgent"}],
                "created_at": "2023-01-01T10:00:00Z",
                "updated_at": "2023-01-01T11:00:00Z",
                "user": {"login": "dev1"}
            },
            {
                "id": 2,
                "number": 102,
                "title": "Add feature",
                "html_url": "http://github.com/test/repo/pull/102",
                "merged_at": None,
                "labels": [{"name": "enhancement"}],
                "created_at": "2023-01-02T10:00:00Z",
                "updated_at": "2023-01-02T11:00:00Z",
                "user": {"login": "dev2"}
            }
        ]

        result = GithubPRService.classify_prs("test", "repo")

        assert result["stats"]["total_prs"] == 2
        assert result["stats"]["prs_with_labels"] == 2
        assert result["stats"]["prs_aceptados"] == 1
        assert result["stats"]["prs_cambios_solicitados"] == 1
        assert "bug" in result["labels_classification"]
        assert result["labels_classification"]["bug"]["aceptado"]["count"] == 1
        assert result["labels_classification"]["enhancement"]["cambios solicitados"]["count"] == 1

    @patch("Services.pr_service.GithubPRAPI.get_repo_pull_requests")
    def test_classify_prs_no_labels(self, mock_get_prs):
        """Debe manejar PRs sin etiquetas."""
        mock_get_prs.return_value = [
            {
                "id": 3,
                "number": 103,
                "title": "No label PR",
                "html_url": "http://github.com/test/repo/pull/103",
                "merged_at": None,
                "labels": [],
                "created_at": "2023-01-03T10:00:00Z",
                "updated_at": "2023-01-03T11:00:00Z",
                "user": {"login": "dev3"}
            }
        ]

        result = GithubPRService.classify_prs("test", "repo")

        assert result["stats"]["total_prs"] == 1
        assert result["stats"]["prs_with_labels"] == 0
        assert result["stats"]["prs_cambios_solicitados"] == 1
        assert result["labels_classification"] == {}

    @patch("Services.pr_service.GithubPRAPI.get_repo_pull_requests")
    def test_classify_prs_exception(self, mock_get_prs):
        """Debe manejar errores y devolver el campo 'error'."""
        mock_get_prs.side_effect = Exception("API error")

        result = GithubPRService.classify_prs("test", "repo")

        assert "error" in result
        assert result["repo_info"] == "test/repo"
