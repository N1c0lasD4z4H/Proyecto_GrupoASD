import os
import requests
from dotenv import load_dotenv

load_dotenv()

class GithubIssueAPI:
    BASE_URL = "https://api.github.com"
    TOKEN = os.getenv("GITHUB_TOKEN")

    @staticmethod
    def _make_paginated_request(url: str, params: dict = None):
        """Maneja peticiones paginadas a la API de GitHub"""
        headers = {"Authorization": f"Bearer {GithubIssueAPI.TOKEN}"}
        all_items = []
        page = 1
        params = params or {}
        
        while True:
            params["page"] = page
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                break
                
            all_items.extend(data)
            
            if "next" not in response.links:
                break
                
            page += 1

        return all_items

    @staticmethod
    def get_repo_issues(owner: str, repo: str, state: str = "all"):
        """Obtiene TODOS los issues (con paginación)"""
        url = f"{GithubIssueAPI.BASE_URL}/repos/{owner}/{repo}/issues"
        params = {"state": state, "per_page": 100}
        return GithubIssueAPI._make_paginated_request(url, params)