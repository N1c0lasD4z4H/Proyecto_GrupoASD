import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class GithubUserAPI:
    BASE_URL = "https://api.github.com"
    TOKEN = os.getenv("GITHUB_TOKEN")

    @staticmethod
    def get_user_repos(username: str):
        url = f"{GithubUserAPI.BASE_URL}/users/{username}/repos"
        headers = {"Authorization": f"Bearer {GithubUserAPI.TOKEN}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        response.raise_for_status()
