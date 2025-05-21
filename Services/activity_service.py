from typing import Dict, List, Any
from datetime import datetime, timezone
from collections import defaultdict
from Github_Request.activity_request import GitHubClient

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
            author_key = (author_info['email'], author_info['name'])

            commit_date = datetime.strptime(author_info['date'], "%Y-%m-%dT%H:%M:%SZ").date()
            key = (author_key, commit_date)

            activity_per_user_day[key]["commit_count"] += 1
            activity_per_user_day[key]["author"] = {
                "name": author_info['name'],
                "email": author_info['email']
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