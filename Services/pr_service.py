from typing import Dict, List, Any
from datetime import datetime
from Github_Request.pr_request import GithubPRAPI

class GithubPRService:
    @staticmethod
    def classify_prs(owner: str, repo: str) -> Dict[str, Any]:
        try:
            prs = GithubPRAPI.get_repo_pull_requests(owner, repo, state="all")
            all_labels = set()
            prs_data = []  # Almacenará todos los PRs como documentos separados
            
            # Primera pasada: recolectar etiquetas y preparar datos granulares
            for pr in prs:
                labels = [label["name"].lower() for label in pr.get("labels", [])]
                all_labels.update(labels)
                
                pr_state = "aceptado" if pr.get("merged_at") else "cambios solicitados"
                
                # Documento granular para cada PR
                pr_data = {
                    "id": pr.get("id"),
                    "number": pr.get("number"),
                    "title": pr.get("title"),
                    "url": pr.get("html_url"),
                    "state": pr_state,
                    "labels": labels,
                    "created_at": pr.get("created_at"),
                    "updated_at": pr.get("updated_at"),
                    "merged_at": pr.get("merged_at"),
                    "user": pr.get("user", {}).get("login") if pr.get("user") else None
                }
                prs_data.append(pr_data)

            # Inicializar estructura de clasificación
            classified = {
                label: {
                    "total": 0,  # Nuevo: conteo total por etiqueta
                    "aceptado": {"count": 0, "prs": []},
                    "cambios solicitados": {"count": 0, "prs": []}
                } 
                for label in all_labels
            }

            # Segunda pasada: clasificar PRs
            for pr in prs_data:
                for label in pr["labels"]:
                    classified[label]["total"] += 1
                    state_key = pr["state"]
                    classified[label][state_key]["count"] += 1
                    classified[label][state_key]["prs"].append({
                        "id": pr["id"],
                        "number": pr["number"],
                        "title": pr["title"],
                        "url": pr["url"]
                    })

            # Calcular estadísticas adicionales
            prs_with_labels = sum(1 for pr in prs_data if pr["labels"])
            label_usage = {label: data["total"] for label, data in classified.items()}
            
            return {
                "labels_classification": classified,
                "individual_prs": prs_data,  # Nuevo: todos los PRs como documentos separados
                "stats": {
                    "total_prs": len(prs_data),
                    "prs_with_labels": prs_with_labels,
                    "prs_aceptados": sum(1 for pr in prs_data if pr["state"] == "aceptado"),
                    "prs_cambios_solicitados": sum(1 for pr in prs_data if pr["state"] == "cambios solicitados"),
                    "label_usage": label_usage  # Nuevo: uso de cada etiqueta
                },
                "repo_metadata": {
                    "owner": owner,
                    "repo": repo,
                    "processed_at": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "repo_info": f"{owner}/{repo}"
            }