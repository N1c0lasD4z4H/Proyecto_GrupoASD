from fastapi import APIRouter, HTTPException
from Services.user_service import GithubUserService

router = APIRouter()

@router.get("/user/{username}/repos")
async def get_user_repos(username: str):
    try:
        repos = GithubUserService.get_user_repos_info(username)
        return {"username": username, "repos": repos}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
