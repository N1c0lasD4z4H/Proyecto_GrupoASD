from fastapi import APIRouter, HTTPException, BackgroundTasks
from Services.pr_time_service import PRDashboardService
from Models.pr_time import PRTimeStats
from Elastic.index_dispatcher import send_document
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/prs/{owner}/{repo}")
async def get_dashboard_prs(owner: str, repo: str, background_tasks: BackgroundTasks):
    try:
        data = await PRDashboardService.get_enriched_pull_requests(owner, repo)

        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        pr_time_stats = PRTimeStats(**data)
        background_tasks.add_task(send_document, "github_pr_time", pr_time_stats.repository, pr_time_stats)
        
        return pr_time_stats

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
