from typing import Dict, List, Any
from datetime import datetime
from Github_Request.activity_request import GitHubClient
class GitHubService:
    def __init__(self):
        self.github_client = GitHubClient()

    async def get_commit_info(self, username: str) -> Dict[str, Any]:
        """Recopila información sobre los commits de los repositorios de un usuario."""
        try:
            # Obtener los repositorios del usuario
            repos = await self.github_client.get_user_repos(username)
            commit_data = []

            for repo in repos:
                # Verificar que el repositorio tiene el campo 'name'
                repo_name = repo.get('name')
                if not repo_name:
                    continue

                # Obtener los commits del repositorio
                commits = await self.github_client.get_repo_commits(username, repo_name)
                
                # Procesar el último commit
                if commits:
                    last_commit_date_str = commits[0]['commit']['author'].get('date')
                    last_commit = datetime.strptime(
                        last_commit_date_str, "%Y-%m-%dT%H:%M:%SZ"
                    ) if last_commit_date_str else None
                else:
                    last_commit = None

                # Agregar la información procesada
                commit_data.append({
                    "repo_name": repo_name,
                    "total_commits": len(commits),
                    "last_commit": last_commit.isoformat() if last_commit else None,
                    "is_empty": not bool(commits)
                })

            # Retornar la información recopilada
            return {"user": username, "commits": commit_data}

        except Exception as e:
            # Manejar cualquier error
            return {"error": f"Se produjo un error inesperado: {str(e)}"}