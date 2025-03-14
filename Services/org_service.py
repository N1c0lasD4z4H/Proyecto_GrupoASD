from Github_Request.org_request import GithubOrgAPI

class GithubOrgService:
    @staticmethod
    def get_org_repos_info(org_name: str):
        repos = GithubOrgAPI.get_org_repos(org_name)
        return [{"name": repo["name"], "url": repo["html_url"]} for repo in repos]
