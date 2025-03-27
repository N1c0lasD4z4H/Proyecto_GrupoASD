import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class GithubOrgAPI:
    BASE_URL = "https://api.github.com"
    TOKEN = os.getenv("GITHUB_TOKEN")

    @staticmethod
    def get_org_repos(org_name: str): #Obtiene los repositorios de una organización de GitHub.
        url = f"{GithubOrgAPI.BASE_URL}/orgs/{org_name}/repos"
        headers = {"Authorization": f"Bearer {GithubOrgAPI.TOKEN}"}#Se establece la autorización a traves de token
        params ={ "type": "all", "per_page": 100}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        response.raise_for_status()# Lanza una HTTPError si la solicitud a la API de GitHub falla.
