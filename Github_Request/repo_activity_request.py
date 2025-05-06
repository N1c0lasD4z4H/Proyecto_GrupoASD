import os
import httpx
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class GitHubRequest:
    BASE_URL = "https://api.github.com"
    TOKEN = os.getenv("GITHUB_TOKEN")

    def __init__(self):
        self.timeout = httpx.Timeout(30.0)
    
    async def _paginated_get(self, url: str, headers: dict) -> List[Dict[str, Any]]:
        results = []
        next_url = f"{url}?per_page=100"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            while next_url:
                try:
                    response = await client.get(next_url, headers=headers)

                    if response.status_code == 401:
                        raise Exception("Invalid or missing GitHub token")
                    if response.status_code == 404:
                        raise Exception("Repository not found")
                    if response.status_code != 200:
                        raise Exception(f"GitHub API error: {response.text}")

                    data = response.json()
                    if not isinstance(data, list):
                        raise Exception(f"Unexpected response format: {data}")

                    results.extend(data)

                    # Manejo de paginación
                    link_header = response.headers.get('link', '')
                    next_url = None
                    if 'rel="next"' in link_header:
                        next_url = link_header.split(';')[0].strip('<> ')
                        
                except httpx.RequestError as e:
                    logger.error(f"Request failed: {str(e)}")
                    raise Exception(f"Failed to connect to GitHub API: {str(e)}")

        return results

    async def get_commits(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        if not owner or not repo:
            raise ValueError("Owner and repo parameters are required")

        url = f"{self.BASE_URL}/repos/{owner}/{repo}/commits"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {self.TOKEN}"
        }

        try:
            return await self._paginated_get(url, headers)
        except Exception as e:
            logger.error(f"Error getting commits for {owner}/{repo}: {str(e)}")
            raise
