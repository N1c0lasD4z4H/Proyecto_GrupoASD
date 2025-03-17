from Github_Request.pr_request import GithubPRAPI

class GithubPRService:
    # Etiquetas predefinidas a buscar en los PRs
    PREDEFINED_LABELS = {"diseño", "estilos", "pruebas"}

    @staticmethod
    def classify_prs(owner: str, repo: str):
        """
        Recupera y clasifica los PRs de un repositorio según:
          - Etiquetas: diseño, estilos, pruebas unitarias.
          - Estado: 'aceptado' (mergeado) o 'cambios solicitados' (no mergeado).
        """
        prs = GithubPRAPI.get_repo_pull_requests(owner, repo, state="all")
        
        # Estructura de salida: un diccionario por cada etiqueta predefinida con dos subcategorías de estado
        classified = {label: {"aceptado": [], "cambios solicitados": []} for label in GithubPRService.PREDEFINED_LABELS}
        
        for pr in prs:
            # Determinar el estado: si tiene "merged_at" es aceptado, de lo contrario, se considera que tiene cambios solicitados.
            pr_state = "aceptado" if pr.get("merged_at") else "cambios solicitados"
            # Obtener las etiquetas del PR()
            pr_labels = {label["name"].lower() for label in pr.get("labels", [])}
            # Clasificar el PR en cada categoría que corresponda según la intersección de etiquetas
            for label in GithubPRService.PREDEFINED_LABELS.intersection(pr_labels):
                classified[label][pr_state].append({
                    "id": pr.get("id"),
                    "title": pr.get("title"),
                    "url": pr.get("html_url"),
                    "state": pr_state
                })
        return classified
