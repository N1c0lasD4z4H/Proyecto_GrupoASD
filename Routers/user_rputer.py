from fastapi import APIRouter, HTTPException, BackgroundTasks
from Services.user_service import GithubUserService
from Elastic.bulk_dispatcher import send_bulk_documents
import logging
from datetime import datetime, timezone

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/users/{username}/repositories")
async def get_user_repositories(username: str, background_tasks: BackgroundTasks):
    try:
        repositories = await GithubUserService.get_user_repos_info(username)

        if not repositories:
            raise HTTPException(status_code=404, detail=f"No se encontraron repositorios para el usuario {username}")

        main_doc = {
            "username": username,
            "metadata": {
                "total_repos": len(repositories),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        }

        documents = [main_doc]
        for repo in repositories:
            repo_doc = {
                "username": username,
                "repository": repo,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            documents.append(repo_doc)

        background_tasks.add_task(send_bulk_documents, "github_user_repos", documents)

        return {
            "status": "success",
            "user": username,
            "repository_count": len(repositories),
            "message": "Repositories processed successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing {username}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error procesando repositorios")
