import httpx
from datetime import datetime
from typing import List, Dict, Any
 
class GitHubRequest:
    def __init__(self):
        self.base_url = "https://api.github.com/repos"
        
    async def _paginated_get(self, url: str, headers: dict) -> List[Dict[str, Any]]:
        results = []
        page = 1
        
        async with httpx.AsyncClient() as client:
            while True:
                response = await client.get(
                    url,
                    headers=headers,
                    params={"page": page, "per_page": 100}
                )
                
                if response.status_code == 401:
                    raise Exception("Invalid or missing GitHub token")
                if response.status_code != 200:
                    raise Exception(f"GitHub API error: {response.text}")
                
                data = response.json()
                if not data:
                    break
                    
                results.extend(data)
                page += 1
                
        return results
 
    async def get_commits(self, owner: str, repo: str, token: str = None) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/{owner}/{repo}/commits"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {token}" if token else None
        }
        headers = {k: v for k, v in headers.items() if v is not None}
        
        return await self._paginated_get(url, headers)
 