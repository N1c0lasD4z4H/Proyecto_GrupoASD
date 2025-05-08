from fastapi import APIRouter, HTTPException, BackgroundTasks
from Services.activity_service import GitHubService
from Models.user_commits import UserCommitDocument
from Elastic.index_dispatcher import send_document
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/users/{username}/commits", summary="Get user commit activity")
async def get_github_commits(username: str, background_tasks: BackgroundTasks):
    try:
        if not username:
            raise HTTPException(status_code=400, detail="Username is required")

        service = GitHubService()
        result = await service.get_commit_info(username)

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        # Calcula total_commits solo si no está presente
        if "total_commits" not in result:
            total_commits = sum(repo["total_commits"] for repo in result["commits"])
            result["total_commits"] = total_commits

        # Validar datos con Pydantic
        document = UserCommitDocument(**result)

        # Enviar datos a Elasticsearch en segundo plano
        background_tasks.add_task(send_document, "github_user_commits", username, document)

        return {
            "status": "success",
            "username": username,
            "total_commits": document.total_commits,
            "repositories": document.commits
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing {username}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


