# Routers/pr_router.py

from fastapi import APIRouter, BackgroundTasks, HTTPException
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class PRDashboardService:
    @staticmethod
    async def get_enriched_pull_requests(owner: str, repo: str):
        # Aquí va la lógica real (simulada en este ejemplo)
        if owner == "error":
            raise HTTPException(status_code=400, detail="Simulated error")

        return {
            "owner": owner,
            "repo": repo,
            "pull_requests": 5,
            "average_merge_time": "2 days"
        }

@router.get("/prs/{owner}/{repo}")
async def get_dashboard_prs(owner: str, repo: str, background_tasks: BackgroundTasks):
    try:
        pr_time_stats = await PRDashboardService.get_enriched_pull_requests(owner, repo)

        background_tasks.add_task(lambda: logger.info("Documento enviado"))

        return pr_time_stats

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
