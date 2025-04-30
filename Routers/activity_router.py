from fastapi import APIRouter, HTTPException, BackgroundTasks
from Services.activity_service import GitHubService
from Elastic.elastic_service import es  

router = APIRouter()

async def send_to_elastic(data: dict, index_name: str = "github_user_commits"):
    """
    Envía datos de commits a Elasticsearch.
    """
    try:
        await es.index(
            index=index_name,
            id=data["username"],  
            document=data
        )
    except Exception as e:
        raise RuntimeError(f"Error al indexar en Elasticsearch: {str(e)}")

@router.get("/users/{username}/commits")
async def get_github_commits(username: str, background_tasks: BackgroundTasks):
    service = GitHubService()
    result = await service.get_commit_info(username)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    # Agrega el nombre de usuario para el identificador único
    result["username"] = username

    # Envía los datos a Elasticsearch como tarea en segundo plano
    background_tasks.add_task(send_to_elastic, result)

    return result
