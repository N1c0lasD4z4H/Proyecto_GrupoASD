import httpx
import os
from dotenv import load_dotenv
from typing import List, Optional

load_dotenv()

class GithubFileCheckAPI:
    BASE_URL = "https://api.github.com"
    TOKEN = os.getenv("GITHUB_TOKEN")
    HEADERS = {"Authorization": f"Bearer {TOKEN}"}
    TIMEOUT = 30.0

    @staticmethod
    async def list_user_repositories(user_or_org: str) -> List[str]:
        """Lista todos los repositorios con paginación"""
        repos = []
        page = 1
        
        async with httpx.AsyncClient(timeout=GithubFileCheckAPI.TIMEOUT) as client:
            while True:
                url = f"{GithubFileCheckAPI.BASE_URL}/users/{user_or_org}/repos"
                params = {
                    "type": "all",
                    "per_page": 100,
                    "page": page
                }
                
                try:
                    response = await client.get(
                        url,
                        headers=GithubFileCheckAPI.HEADERS,
                        params=params
                    )
                    
                    if response.status_code == 404:
                        raise ValueError(f"User/org '{user_or_org}' not found")
                    response.raise_for_status()
                    
                    data = response.json()
                    if not data:
                        break
                        
                    repos.extend([f"{repo['owner']['login']}/{repo['name']}" for repo in data])
                    page += 1
                    
                except httpx.RequestError as e:
                    raise Exception(f"Failed to connect to GitHub: {str(e)}")
        
        return repos

    @staticmethod
    async def check_file_exists(repo: str, file_path: str) -> bool:
        """Verifica asincrónicamente si un archivo existe"""
        url = f"{GithubFileCheckAPI.BASE_URL}/repos/{repo}/contents/{file_path}"
        
        async with httpx.AsyncClient(timeout=GithubFileCheckAPI.TIMEOUT) as client:
            try:
                response = await client.get(url, headers=GithubFileCheckAPI.HEADERS)
                if response.status_code == 200:
                    return True
                elif response.status_code == 404:
                    return False
                response.raise_for_status()
            except httpx.RequestError as e:
                raise Exception(f"Failed to check file: {str(e)}")