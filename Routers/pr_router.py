from fastapi import APIRouter, HTTPException
from Services.pr_service import GithubPRService

router = APIRouter()

@router.get("/repos/{owner}/{repo}/pulls/stats")
async def get_pr_stats(owner: str, repo: str):
    """
    Endpoint que devuelve estadísticas de pull requests del repositorio,
    clasificadas por etiquetas predefinidas y estado.
    """
    try:
        stats = GithubPRService.classify_prs(owner, repo)
        return stats#Un diccionario en una lista de pull request con su etiqueta con el 
                    #numero de aceptadas y con cambios solicitados
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))#HTTPException: Si ocurre un error al obtener los pull request.
