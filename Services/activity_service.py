from typing import Dict, List, Any, Set
from datetime import datetime
from Github_Request.activity_request import GitHubClient

class GitHubService:
    def __init__(self):
        self.github_client = GitHubClient()

    async def get_commit_info(self, username: str) -> Dict[str, Any]:
        """Recopila información detallada sobre los commits de los repositorios de un usuario."""
        try:
            repos = await self.github_client.get_user_repos(username)
            commit_data = []

            for repo in repos:
                repo_name = repo.get('name')
                if not repo_name:
                    continue

                commits = await self.github_client.get_repo_commits(username, repo_name)
                
                # Procesamiento de commits
                unique_authors = set()
                first_commit = None
                last_commit = None
                
                if commits:
                    # Obtener autores únicos
                    unique_authors.update(
                        commit['commit']['author']['username'] 
                        for commit in commits 
                        if commit.get('commit', {}).get('author', {}).get('username')
                    )
                    
                    # Primer commit
                    first_commit_date_str = commits[-1]['commit']['author'].get('date')
                    first_commit = datetime.strptime(
                        first_commit_date_str, "%Y-%m-%dT%H:%M:%SZ"
                    ) if first_commit_date_str else None
                    
                    # Último commit
                    last_commit_date_str = commits[0]['commit']['author'].get('date')
                    last_commit = datetime.strptime(
                        last_commit_date_str, "%Y-%m-%dT%H:%M:%SZ"
                    ) if last_commit_date_str else None

                commit_data.append({
                    "repo_name": repo_name,
                    "total_commits": len(commits),
                    "first_commit": first_commit.isoformat() if first_commit else None,
                    "last_commit": last_commit.isoformat() if last_commit else None,
                    "is_empty": not bool(commits),
                    "unique_authors_count": len(unique_authors),
                    "unique_authors": list(unique_authors) if unique_authors else []
                })

            return {
                "user": username,
                "total_repos": len(repos),
                "repos_with_commits": len([r for r in commit_data if not r['is_empty']]),
                "commits": commit_data
            }

        except Exception as e:
            return {"error": f"Se produjo un error inesperado: {str(e)}"}