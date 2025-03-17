from fastapi import APIRouter, HTTPException
from Services.org_service import GithubOrgService

router = APIRouter()

@router.get("/org/{org_name}/repos")
async def get_org_repos(org_name: str):
    """
    Endpoint para obtener los repositorios de una organización de GitHub.
    """
    try:
        repos = GithubOrgService.get_org_repos_info(org_name)
        return {"organization": org_name, "repos": repos}#dict: Un diccionario con el nombre de la organización y lista de repositorios.
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))#HTTPException: Si ocurre un error al obtener los repositorios.
