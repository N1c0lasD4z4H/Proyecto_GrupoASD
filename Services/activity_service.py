from typing import Dict, List, Any
from datetime import datetime, timezone
from collections import defaultdict
from Github_Request.activity_request import GitHubClient  # Ajusta la ruta si es necesario

class GitHubService:
    def __init__(self):
        self.github_client = GitHubClient()

    async def get_repo_commit_documents(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        commits = await self.github_client.get_repo_commits(owner, repo)
        if not commits:
            return []

        activity_per_user_day = defaultdict(lambda: {"commit_count": 0, "author": {}})
        for commit in commits:
            author_info = commit['commit']['author']
            author_key = (author_info.get('email'), author_info.get('name'))

            commit_date = datetime.strptime(author_info['date'], "%Y-%m-%dT%H:%M:%SZ").date()
            key = (author_key, commit_date)

            activity_per_user_day[key]["commit_count"] += 1
            activity_per_user_day[key]["author"] = {
                "name": author_info.get('name'),
                "email": author_info.get('email')
            }

        today_utc = datetime.now(timezone.utc).isoformat()
        documents = []
        for (author_key, date), data in activity_per_user_day.items():
            documents.append({
                "owner": owner,
                "repo": repo,
                "author": data["author"],
                "date": str(date),
                "commit_count": data["commit_count"],
                "timestamp": today_utc
            })

        return documents

    async def get_commit_info(self, username: str) -> dict:
        try:
            repos = await self.github_client.get_user_repos(username)
            total_repos = len(repos)
            total_commits = 0
            repos_with_commits = 0
            commits_info = []

            for repo in repos:
                repo_name = repo.get("name")
                if not repo_name:
                    continue
                commits = await self.github_client.get_repo_commits(username, repo_name)
                if commits:
                    repos_with_commits += 1
                    total_commits += len(commits)
                    commits_info.append({
                        "repo_name": repo_name,
                        "count": len(commits),
                        "is_empty": False
                    })
                else:
                    commits_info.append({
                        "repo_name": repo_name,
                        "count": 0,
                        "is_empty": True
                    })

            return {
                "user": username,
                "total_repos": total_repos,
                "repos_with_commits": repos_with_commits,
                "total_commits": total_commits,
                "commits": commits_info
            }
        except Exception as e:
            return {"error": str(e)}
