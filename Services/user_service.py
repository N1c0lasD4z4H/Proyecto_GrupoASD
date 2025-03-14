from Github_Request.user_request import GithubUserAPI

class GithubUserService:
    @staticmethod
    def get_user_repos_info(username: str):
        repos = GithubUserAPI.get_user_repos(username)
        return [{"name": repo["name"], "url": repo["html_url"]} for repo in repos]
