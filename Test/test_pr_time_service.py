import pytest
from unittest.mock import AsyncMock, patch
from Services.pr_time_service import PRDashboardService

@pytest.mark.asyncio
class TestPRDashboardService:
    """Pruebas unitarias para PRDashboardService.get_enriched_pull_requests"""

    @patch("Services.pr_time_service.GithubPRAPI.get_pull_request_reviews")
    @patch("Services.pr_time_service.GithubPRAPI.get_repo_pull_requests")
    async def test_get_enriched_pull_requests_basic(self, mock_get_prs, mock_get_reviews):
        """Debe retornar PRs enriquecidos con estadísticas básicas."""
        mock_get_prs.return_value = [
            {
                "id": 1,
                "number": 10,
                "html_url": "http://example.com/pr/10",
                "user": {"login": "dev1"},
                "created_at": "2023-01-01T10:00:00Z",
                "closed_at": "2023-01-02T10:00:00Z",
                "merged_at": "2023-01-02T12:00:00Z",
                "draft": False
            }
        ]
        mock_get_reviews.return_value = [
            {"submitted_at": "2023-01-01T15:00:00Z"},
            {"submitted_at": "2023-01-01T20:00:00Z"}
        ]

        result = await PRDashboardService.get_enriched_pull_requests("test", "repo")

        assert result["repository"] == "test/repo"
        assert result["stats"]["total"] == 1
        assert result["stats"]["closed"] == 1
        assert result["stats"]["merged"] == 1
        assert result["stats"]["open"] == 0
        assert result["stats"]["with_reviews"] == 1
        assert result["pull_requests"][0]["review_count"] == 2
        assert result["pull_requests"][0]["first_review_at"] == "2023-01-01T15:00:00Z"

    @patch("Services.pr_time_service.GithubPRAPI.get_pull_request_reviews")
    @patch("Services.pr_time_service.GithubPRAPI.get_repo_pull_requests")
    async def test_get_enriched_pull_requests_draft_open_no_reviews(self, mock_get_prs, mock_get_reviews):
        """Debe manejar PR abiertos en estado draft sin revisiones."""
        mock_get_prs.return_value = [
            {
                "id": 2,
                "number": 11,
                "html_url": "http://example.com/pr/11",
                "user": {"login": "dev2"},
                "created_at": "2023-02-01T10:00:00Z",
                "closed_at": None,
                "merged_at": None,
                "draft": True
            }
        ]
        mock_get_reviews.return_value = []

        result = await PRDashboardService.get_enriched_pull_requests("test", "repo")

        assert result["stats"]["total"] == 1
        assert result["stats"]["open"] == 1
        assert result["stats"]["drafts"] == 1
        assert result["stats"]["with_reviews"] == 0
        assert result["pull_requests"][0]["state"] == "open"
        assert result["pull_requests"][0]["review_count"] == 0

    @patch("Services.pr_time_service.GithubPRAPI.get_repo_pull_requests")
    async def test_get_enriched_pull_requests_exception(self, mock_get_prs):
        """Debe manejar excepciones del API de PRs."""
        mock_get_prs.side_effect = Exception("API Error")

        result = await PRDashboardService.get_enriched_pull_requests("test", "repo")

        assert "error" in result
        assert result["repository"] == "test/repo"
