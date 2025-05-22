import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from Routers.pr_router import router
from unittest.mock import patch

app = FastAPI()
app.include_router(router)

@pytest.mark.asyncio
async def test_get_pr_stats_unexpected_error():
    with patch("Services.pr_service.GithubPRService.classify_prs") as mock_service:
        mock_service.side_effect = Exception("Unexpected failure")

        client = TestClient(app)
        response = client.get("/repos/test_owner/test_repo/pulls/stats")

        assert response.status_code == 400  # Según tu pr_router, error lanza 400
        assert response.json() == {"detail": "Unexpected failure"}
