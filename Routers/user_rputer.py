from fastapi import APIRouter, HTTPException
from Services.user_service import GithubUserService

router = APIRouter()

@router.get("/user/{username}/repos")
async def get_user_repos(username: str):
    """
    Endpoint para obtener los repositorios de un usuario de GitHub.
    """
    try:
        repos = GithubUserService.get_user_repos_info(username)
        return {"username": username, "repos": repos}#dict: Un diccionario con el nombre de usuario y una lista de sus repositorios.

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))#HTTPException: Si ocurre un error al obtener los repositorios.
