from fastapi import APIRouter, HTTPException, BackgroundTasks
from Services.pr_service import GithubPRService
from Models.pr_stats import PRStats
from Elastic.index_dispatcher import send_document

router = APIRouter()

@router.get("/repos/{owner}/{repo}/pulls/stats")
async def get_pr_stats(owner: str, repo: str, background_tasks: BackgroundTasks):
    try:
        stats = GithubPRService.classify_prs(owner, repo)
        stats["repo_id"] = f"{owner}_{repo}"
        pr_stats = PRStats(**stats)
        background_tasks.add_task(send_document, "github_pr_stats", pr_stats.repo_id, pr_stats)
        return pr_stats
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
