from Github_Request.user_request import GithubUserAPI
from datetime import datetime

class GithubUserService:
    @staticmethod
    async def get_user_repos_info(username: str):
        repos = GithubUserAPI.get_user_repos(username)
        return [
            {
                "name": repo["name"],
                "url": repo["html_url"],
                "created_at": datetime.strptime(repo["created_at"], "%Y-%m-%dT%H:%M:%SZ").isoformat(),
                "updated_at": datetime.strptime(repo["updated_at"], "%Y-%m-%dT%H:%M:%SZ").isoformat(),
                "language": repo["language"],
                "open_issues": repo["open_issues_count"],
                "size": repo["size"],
                "is_fork": repo["fork"]
            }
            for repo in repos
        ]