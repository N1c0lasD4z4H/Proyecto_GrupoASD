from fastapi import APIRouter, HTTPException, BackgroundTasks
from Services.user_service import GithubUserService
from Models.user_repos import UserRepoDocument
from Elastic.index_dispatcher import send_document
import logging
from datetime import datetime, timezone

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/users/{username}/repositories")
async def get_user_repositories(username: str, background_tasks: BackgroundTasks):
    try:
        # Obtener lista de repositorios del usuario
        repositories = await GithubUserService.get_user_repos_info(username)

        if not repositories:
            raise HTTPException(status_code=404, detail=f"No se encontraron repositorios para el usuario {username}")

        doc = UserRepoDocument(
            username=username,
            repositories=repositories,
            metadata={
                "total_repos": len(repositories),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )

        background_tasks.add_task(send_document, "github_user_repos", username, doc)

        return {
            "status": "success",
            "user": username,
            "repository_count": len(repositories),
            "data": repositories[:100],
            "message": "Repositorios procesados exitosamente"
        }

    except HTTPException as he:
        logger.warning(f"Error controlado: {he.detail}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado procesando {username}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error procesando repositorios")
