from Services.pr_service import GithubPRService
from Elastic.bulk_dispatcher import send_bulk_documents
from datetime import datetime

def job_index_prs():
    print(f"[⏰] Ejecutando tarea programada para PRs - {datetime.now()}")

    # Aquí defines los repos que quieres rastrear
    tracked_repos = [
        {"owner": "public-apis", "repo": "public-apis"},
        {"owner": "unionlabs", "repo": "union"}
    ]

    for repo_info in tracked_repos:
        owner = repo_info["owner"]
        repo = repo_info["repo"]

        try:
            stats = GithubPRService.classify_prs(owner, repo)
            stats["repo_id"] = f"{owner}_{repo}"

            documents = []

            # PRs individuales
            for pr in stats["individual_prs"] or []:
                documents.append({
                    **pr.model_dump(),
                    "repo_owner": owner,
                    "repo_name": repo,
                    "processed_at": stats["repo_metadata"].processed_at
                })

            # Documento resumen
            documents.append({
                "repo_owner": owner,
                "repo_name": repo,
                "processed_at": stats["repo_metadata"].processed_at,
                "stats": stats["stats"].model_dump()
            })

            send_bulk_documents("github_pr_stats", documents)

        except Exception as e:
            print(f"[❌] Error procesando {owner}/{repo}: {str(e)}")
