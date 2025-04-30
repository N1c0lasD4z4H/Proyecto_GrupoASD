from fastapi import APIRouter, HTTPException, Header, BackgroundTasks
from typing import Optional, Dict, Any
from Services.repo_activity_service import GitHubService
from Elastic.elastic_service import es  

router = APIRouter()
github_service = GitHubService()

async def send_to_elastic(data: Dict[str, Any], index_name: str = "github_repo_activity"):
    """
    Envía datos a Elasticsearch en segundo plano.
    """
    try:
        await es.index(
            index=index_name,
            id=data["repo_id"],  # Usa un campo único del documento
            document=data
        )
    except Exception as e:
        raise RuntimeError(f"Error al indexar en Elasticsearch: {str(e)}")

@router.get("/{owner}/{repo}/activity")
async def get_repo_activity(
    owner: str,
    repo: str,
    token: Optional[str] = Header(None),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    try:
        # Obtener actividad del repositorio de manera asincrónica
        activity_data = await github_service.get_repo_activity(owner, repo, token)

        # Asegura que tiene un identificador único
        activity_data["repo_id"] = f"{owner}_{repo}"

        # Indexar en Elasticsearch como tarea en segundo plano
        background_tasks.add_task(send_to_elastic, activity_data)

        return activity_data  # Responder con los datos obtenidos
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving activity: {str(e)}"
        )
