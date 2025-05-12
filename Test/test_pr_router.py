import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from Routers.pr_router import router
from unittest.mock import patch

# Crear la app de FastAPI
app = FastAPI()
app.include_router(router)

# Usar TestClient para hacer la prueba
@pytest.mark.asyncio
async def test_get_dashboard_prs_unexpected_error():
    with patch("Routers.pr_router.PRDashboardService.get_enriched_pull_requests") as mock_service:
        mock_service.side_effect = Exception("Unexpected failure")

        # Usar TestClient en lugar de AsyncClient
        client = TestClient(app)
        response = client.get("/prs/test_owner/test_repo")

        assert response.status_code == 500
        assert response.json() == {"detail": "Internal server error"}
