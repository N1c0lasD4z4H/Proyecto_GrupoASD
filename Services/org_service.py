from Github_Request.org_request import GithubOrgAPI

class GithubOrgService:
    """
    Servicio para interactuar con la API de GitHub y obtener información de los repositorios de una organización.
    """
    @staticmethod
    def get_org_repos_info(org_name: str):
        # Llamar al método de GithubOrgAPI para obtener los repositorios de la organización
        repos = GithubOrgAPI.get_org_repos(org_name)
        #list: Una lista de diccionarios con el nombre y la URL de cada repositorio.
        return [{"name": repo["name"], "url": repo["html_url"]} for repo in repos]