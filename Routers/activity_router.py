from fastapi import APIRouter, HTTPException, BackgroundTasks
from Services.activity_service import GitHubService
from Elastic.bulk_dispatcher import send_bulk_documents
import logging
from datetime import datetime, timezone

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/repos/{owner}/{repo}/commits")
async def get_repo_commits(owner: str, repo: str, background_tasks: BackgroundTasks):
    try:
        service = GitHubService()
        documents = await service.get_repo_commit_documents(owner=owner, repo=repo)

        if not documents:
            return {"status": "success", "message": "No commits found"}

        background_tasks.add_task(send_bulk_documents, "github_repo_commits_activity", documents)

        return {
            "status": "success",
            "owner": owner,
            "repo": repo,
            "records_indexed": len(documents)
        }
    except Exception as e:
        logger.error(f"Error processing {owner}/{repo}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

