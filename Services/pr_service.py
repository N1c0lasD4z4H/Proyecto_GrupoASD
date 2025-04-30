from Github_Request.pr_request import GithubPRAPI

class GithubPRService:
    @staticmethod
    def classify_prs(owner: str, repo: str):
        try:
            # 1. Obtener todas las etiquetas usadas en PRs (no todas las del repo)
            prs = GithubPRAPI.get_repo_pull_requests(owner, repo, state="all")
            all_labels = set()
            
            # Primera pasada: recolectar solo etiquetas usadas
            for pr in prs:
                all_labels.update(label["name"].lower() for label in pr.get("labels", []))
            
            # 2. Inicializar estructura solo con etiquetas usadas
            classified = {
                label: {
                    "aceptado": {"count": 0, "prs": []},
                    "cambios solicitados": {"count": 0, "prs": []}
                } 
                for label in all_labels
            }

            # 3. Segunda pasada: clasificar PRs
            for pr in prs:
                pr_state = "aceptado" if pr.get("merged_at") else "cambios solicitados"
                
                for label in pr.get("labels", []):
                    label_name = label["name"].lower()
                    if label_name in classified:
                        classified[label_name][pr_state]["prs"].append({
                            "id": pr.get("id"),
                            "title": pr.get("title"),
                            "url": pr.get("html_url"),
                            "state": pr_state
                        })
                        classified[label_name][pr_state]["count"] += 1

            # 4. Añadir metadatos útiles
            return {
                "labels_data": classified,
                "repo_info": f"{owner}_{repo}",
                "total_prs": len(prs),
                "prs_with_labels": sum(1 for pr in prs if pr.get("labels"))
            }
            
        except Exception as e:
            return {"error": str(e)}