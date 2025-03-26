import os
import requests
from dotenv import load_dotenv

load_dotenv()

class GithubFileCheckAPI:
    BASE_URL = "https://api.github.com"
    TOKEN = os.getenv("GITHUB_TOKEN")

    @staticmethod
    def list_user_repositories(user_or_org: str):
        """
        Lista todos los repositorios públicos de un usuario u organización.
        También incluye repositorios donde el usuario autenticado colabora.
        """
        url = f"{GithubFileCheckAPI.BASE_URL}/users/{user_or_org}/repos"
        headers = {"Authorization": f"Bearer {GithubFileCheckAPI.TOKEN}"}
        params = {"type": "all", "per_page": 100}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            repos = response.json()
            return [f"{repo['owner']['login']}/{repo['name']}" for repo in repos]
        response.raise_for_status()

    @staticmethod
    def check_file_exists(repo: str, file_path: str):
        """
        Verifica si un archivo existe en el repositorio.
        :param file_path: Ruta del archivo dentro del repositorio.
        """
        url = f"{GithubFileCheckAPI.BASE_URL}/repos/{repo}/contents/{file_path}"
        headers = {"Authorization": f"Bearer {GithubFileCheckAPI.TOKEN}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return True  # El archivo existe
        elif response.status_code == 404:
            return False  # El archivo no existe
        else:
            response.raise_for_status()
