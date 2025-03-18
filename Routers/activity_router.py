from fastapi import APIRouter, Depends, HTTPException
from Services.activity_service import GitHubService

router = APIRouter()

@router.get("/users/{username}/commits")
async def get_github_commits(username: str):
    service = GitHubService()
    result = await service.get_commit_info(username)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result