import os
import requests
from dotenv import load_dotenv

load_dotenv()

class GithubPRAPI:
    BASE_URL = "https://api.github.com"
    TOKEN = os.getenv("GITHUB_TOKEN")

    @staticmethod
    def _make_paginated_request(url: str, params: dict = None):
        """Maneja peticiones paginadas a la API de GitHub"""
        headers = {"Authorization": f"Bearer {GithubPRAPI.TOKEN}"}
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
            
            # Verificar si hay más páginas (headers pueden variar)
            if "next" not in response.links:
                break
                
            page += 1

        return all_items

    @staticmethod
    def get_repo_pull_requests(owner: str, repo: str, state: str = "all"):
        """Obtiene TODOS los PRs (con paginación)"""
        url = f"{GithubPRAPI.BASE_URL}/repos/{owner}/{repo}/pulls"
        params = {"state": state, "per_page": 100}
        return GithubPRAPI._make_paginated_request(url, params)

    @staticmethod
    def get_repo_labels(owner: str, repo: str):
        """Obtiene TODAS las etiquetas (con paginación)"""
        url = f"{GithubPRAPI.BASE_URL}/repos/{owner}/{repo}/labels"
        params = {"per_page": 100}
        return GithubPRAPI._make_paginated_request(url, params)