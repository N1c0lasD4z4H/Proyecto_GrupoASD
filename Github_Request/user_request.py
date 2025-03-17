import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno(token)
load_dotenv()

class GithubUserAPI:    #Clase para interactuar con la API de GitHub para obtener información de los repositorios de un usuario.
    BASE_URL = "https://api.github.com"
    TOKEN = os.getenv("GITHUB_TOKEN")

    @staticmethod
    def get_user_repos(username: str): #Obtiene los repositorios de un usuario de GitHub.
        url = f"{GithubUserAPI.BASE_URL}/users/{username}/repos"# Establece la url para consultar
        headers = {"Authorization": f"Bearer {GithubUserAPI.TOKEN}"}#Se establece la autorización a traves de token
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        response.raise_for_status()# Lanza una HTTPError si la solicitud a la API de GitHub falla.