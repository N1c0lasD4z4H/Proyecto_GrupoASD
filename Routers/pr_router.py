from fastapi import APIRouter, HTTPException, BackgroundTasks
from Services.pr_service import GithubPRService
from Elastic.elastic_service import es  

router = APIRouter()

async def send_to_elastic(data: dict, index_name: str = "github_pr_stats"):
    """
    Envía datos a Elasticsearch.
    """
    try:
        await es.index(
            index=index_name,
            id=data["repo_id"],  
            document=data
        )
    except Exception as e:
        raise RuntimeError(f"Error al indexar en Elasticsearch: {str(e)}")

@router.get("/repos/{owner}/{repo}/pulls/stats")
async def get_pr_stats(owner: str, repo: str, background_tasks: BackgroundTasks):
    """
    Endpoint que devuelve estadísticas de pull requests del repositorio,
    clasificadas por etiquetas predefinidas y estado.
    """
    try:
        # Obtén estadísticas de los pull requests
        stats = GithubPRService.classify_prs(owner, repo)

        # Asegura que las estadísticas tienen un identificador único
        stats["repo_id"] = f"{owner}_{repo}"

        # Indexa las estadísticas en Elasticsearch en segundo plano
        background_tasks.add_task(send_to_elastic, stats)

        return stats  # Devuelve las estadísticas al cliente
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
