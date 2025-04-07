from fastapi import APIRouter, HTTPException, Header, Depends
from typing import Optional
from Services.repo_activity_service import GitHubService
 
router = APIRouter()
github_service = GitHubService()
 
def get_github_token(authorization: Optional[str] = Header(None)) -> Optional[str]:
    if authorization and authorization.startswith("Bearer "):
        return authorization.split(" ")[1]
    return None
 
@router.get("/{owner}/{repo}/activity")
async def get_repo_activity(
    owner: str,
    repo: str,
    token: Optional[str] = Depends(get_github_token)
):
    try:
        return await github_service.get_repo_activity(owner, repo, token)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error retrieving activity: {str(e)}"
        )