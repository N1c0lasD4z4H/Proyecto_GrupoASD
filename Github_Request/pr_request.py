import os
import requests
from dotenv import load_dotenv

load_dotenv()

class GithubPRAPI:
    BASE_URL = "https://api.github.com"
    TOKEN = os.getenv("GITHUB_TOKEN")

    @staticmethod
    def get_repo_pull_requests(owner: str, repo: str, state: str = "all"):
        """
          - owner: propietario del repositorio.
          - repo: nombre del repositorio.
          - state: estado de los PRs ("open", "closed" o "all").
        """
        url = f"{GithubPRAPI.BASE_URL}/repos/{owner}/{repo}/pulls?state={state}"
        headers = {"Authorization": f"Bearer {GithubPRAPI.TOKEN}"}
        params ={ "type": "all", "per_page": 100}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        response.raise_for_status()