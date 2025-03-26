from Github_Request.template_request import GithubFileCheckAPI

class FileCheckService:
    @staticmethod
    def analyze_pull_request_template(user_or_org: str):
        """
        Verifica si los repositorios del usuario u organización contienen `PULL_REQUEST_TEMPLATE`.
        """
        repos = GithubFileCheckAPI.list_user_repositories(user_or_org)
        paths_to_check = [
            "docs/PULL_REQUEST_TEMPLATE.md",
            ".github/PULL_REQUEST_TEMPLATE.md",
            ".github/pull_request_template.md",
            "docs/pull_request_template.md"
        ]

        result = {
            "has_template": [],
            "missing_template": []
        }

        for repo in repos:# Recorre cada repositorio
            has_template = False
            for path in paths_to_check:# Lista de ritas para verificar que el archivo existe
                if GithubFileCheckAPI.check_file_exists(repo, path):
                    has_template = True
                    break

            if has_template:
                result["has_template"].append(repo)
            else:
                result["missing_template"].append(repo)

        # Contar elementos en has_template y missing_template
        result["count_has_template"] = len(result["has_template"])
        result["count_missing_template"] = len(result["missing_template"])

        return result
