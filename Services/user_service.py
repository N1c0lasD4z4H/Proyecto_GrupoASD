from Github_Request.user_request import GithubUserAPI

class GithubUserService:
    """
    Servicio para interactuar con la API de GitHub y obtener información de los repositorios de un usuario.
    """
    @staticmethod
    async def get_user_repos_info(username: str):
        """
        Obtiene y procesa la información de los repositorios de un usuario en GitHub.
        """
        repos = GithubUserAPI.get_user_repos(username)
        processed_repos = [
            {
                "name": repo["name"],
                "url": repo["html_url"],
                "created_at": repo["created_at"],
                "updated_at": repo["updated_at"],
                "language": repo["language"],
                "open_issues": repo["open_issues_count"],
                "size": repo["size"],
                "is_fork": repo["fork"],
            }
            for repo in repos
        ]
        return processed_repos
