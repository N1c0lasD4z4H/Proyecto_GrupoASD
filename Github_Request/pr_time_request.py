import os
import requests
from dotenv import load_dotenv

load_dotenv()

class GithubPRAPI:
    BASE_URL = "https://api.github.com"
    TOKEN = os.getenv("GITHUB_TOKEN")
    HEADERS = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    @staticmethod
    def get_repo_pull_requests(owner: str, repo: str, state: str = "all", per_page: int = 30):
        url = f"{GithubPRAPI.BASE_URL}/repos/{owner}/{repo}/pulls"
        params = {"state": state, "per_page": per_page}
        response = requests.get(url, headers=GithubPRAPI.HEADERS, params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_pull_request_reviews(owner: str, repo: str, pr_number: int):
        url = f"{GithubPRAPI.BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
        response = requests.get(url, headers=GithubPRAPI.HEADERS)
        response.raise_for_status()
        return response.json()
