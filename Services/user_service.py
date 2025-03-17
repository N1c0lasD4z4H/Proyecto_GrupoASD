from Github_Request.user_request import GithubUserAPI

class GithubUserService:
    """
    Servicio para interactuar con la API de GitHub y obtener información de los repositorios de un usuario.
    """
    @staticmethod
    def get_user_repos_info(username: str):
        # Llamar al método de GithubUserAPI para obtener los repositorios del usuario
        repos = GithubUserAPI.get_user_repos(username)
        #list: Una lista de diccionarios con el nombre y la URL de cada repositorio.
        return [{"name": repo["name"], "url": repo["html_url"]} for repo in repos]