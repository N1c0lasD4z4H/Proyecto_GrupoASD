import httpx
import os
from typing import Dict, Any, List
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class GitHubClient:
    # Atributos de clase
    BASE_URL = "https://api.github.com"
    TOKEN = os.getenv("GITHUB_TOKEN")

    def __init__(self):
        # Validar que el token esté presente
        if not GitHubClient.TOKEN:
            raise ValueError("El token de GitHub (GITHUB_TOKEN) no está configurado en las variables de entorno.")

    async def get_user_repos(self, username: str = None) -> List[Dict[str, Any]]:
        """Obtiene los repositorios propios y aquellos en los que el usuario es colaborador."""
        params = {"visibility": "all", "affiliation": "owner,collaborator", "per_page": 100}
        url = f"{GitHubClient.BASE_URL}/user/repos" if username is None else f"{GitHubClient.BASE_URL}/users/{username}/repos"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url,
                    headers={"Authorization": f"Bearer {GitHubClient.TOKEN}"},
                    params=params
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise Exception(f"Error al obtener repositorios: {e.response.status_code} - {e.response.text}")

    async def get_repo_commits(self, username: str, repo_name: str) -> List[Dict[str, Any]]:
        """Obtiene los commits de un repositorio específico de un usuario."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{GitHubClient.BASE_URL}/repos/{username}/{repo_name}/commits",
                    headers={"Authorization": f"Bearer {GitHubClient.TOKEN}"},
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 409:  # Error 409: Repositorio vacío
                    return []  # Devuelve una lista vacía en lugar de un error
                raise Exception(f"Error al obtener commits: {e.response.status_code} - {e.response.text}")
