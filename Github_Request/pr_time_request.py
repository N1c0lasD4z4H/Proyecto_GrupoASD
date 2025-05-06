import httpx
import os
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()

class GithubPRAPI:
    BASE_URL = "https://api.github.com"
    TOKEN = os.getenv("GITHUB_TOKEN")
    HEADERS = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    TIMEOUT = 30.0

    @staticmethod
    async def _paginated_get(url: str, params: dict = None) -> List[Dict[str, Any]]:
        results = []
        page = 1
        params = params or {}
        
        async with httpx.AsyncClient(timeout=GithubPRAPI.TIMEOUT) as client:
            while True:
                params["page"] = page
                response = await client.get(
                    url,
                    headers=GithubPRAPI.HEADERS,
                    params=params
                )
                
                if response.status_code == 401:
                    raise Exception("Invalid GitHub token")
                response.raise_for_status()
                
                data = response.json()
                if not data:
                    break
                    
                results.extend(data)
                page += 1
                
        return results

    @staticmethod
    async def get_repo_pull_requests(owner: str, repo: str, state: str = "all") -> List[Dict[str, Any]]:
        url = f"{GithubPRAPI.BASE_URL}/repos/{owner}/{repo}/pulls"
        params = {"state": state, "per_page": 100}
        return await GithubPRAPI._paginated_get(url, params)

    @staticmethod
    async def get_pull_request_reviews(owner: str, repo: str, pr_number: int) -> List[Dict[str, Any]]:
        url = f"{GithubPRAPI.BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
        return await GithubPRAPI._paginated_get(url)