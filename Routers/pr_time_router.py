from fastapi import APIRouter, HTTPException, BackgroundTasks
from Services.pr_time_service import PRDashboardService
from Elastic.elastic_service import es
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

async def send_to_elastic(data: dict, index_name: str = "github_pr_time"):
    try:
        if "repository" not in data:
            raise ValueError("Missing repository identifier")
            
        await es.index(
            index=index_name,
            id=data["repository"],
            document=data
        )
    except Exception as e:
        logger.error(f"Elasticsearch error: {str(e)}")
        raise

@router.get("/prs/{owner}/{repo}")
async def get_dashboard_prs(owner: str, repo: str, background_tasks: BackgroundTasks):
    try:
        data = await PRDashboardService.get_enriched_pull_requests(owner, repo)
        
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
            
        background_tasks.add_task(send_to_elastic, data)
        return data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")