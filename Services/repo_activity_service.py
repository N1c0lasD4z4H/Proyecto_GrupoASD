from datetime import datetime, timedelta
from typing import List, Dict, Any
from Github_Request.repo_activity_request import GitHubRequest
 
class GitHubService:
    def __init__(self):
        self.github_request = GitHubRequest()
        
    def _process_commits(self, commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        weekly_activity = {}
        last_commit_date = None
        
        for commit in commits:
            commit_data = commit['commit']
            author_date = datetime.strptime(commit_data['author']['date'], "%Y-%m-%dT%H:%M:%SZ")
            
            # Actualizar última fecha de commit
            if not last_commit_date or author_date > last_commit_date:
                last_commit_date = author_date
                
            # Contar actividad semanal
            if datetime.utcnow() - author_date <= timedelta(days=7):
                author = commit.get('author', {}).get('login', 'Unknown')
                weekly_activity[author] = weekly_activity.get(author, 0) + 1
                
        return {
            "total_commits": len(commits),
            "weekly_activity": weekly_activity,
            "last_commit": last_commit_date.isoformat() if last_commit_date else None
        }
 
    async def get_repo_activity(self, owner: str, repo: str, token: str = None) -> Dict[str, Any]:
        commits = await self.github_request.get_commits(owner, repo, token)
        return self._process_commits(commits)