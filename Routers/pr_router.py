from fastapi import APIRouter, HTTPException, BackgroundTasks
from Services.pr_service import GithubPRService
from Models.pr_stats import PRStats
from Elastic.bulk_dispatcher import send_bulk_documents

router = APIRouter()

@router.get("/repos/{owner}/{repo}/pulls/stats")
async def get_pr_stats(owner: str, repo: str, background_tasks: BackgroundTasks):
    try:
        # 1. Obtener y validar datos
        stats = GithubPRService.classify_prs(owner, repo)
        stats["repo_id"] = f"{owner}_{repo}"
        pr_stats = PRStats(**stats)

        # 2. Preparar documentos para Elasticsearch
        documents = []

        # PRs individuales
        for pr in pr_stats.individual_prs or []:
            pr_data = pr.model_dump()
            documents.append({
                **pr_data,
                "repo_owner": pr_stats.repo_metadata.owner,
                "repo_name": pr_stats.repo_metadata.repo,
                "processed_at": pr_stats.repo_metadata.processed_at
            })

        # Documento de estadísticas
        stats_data = pr_stats.stats.model_dump()
        documents.append({
            "repo_owner": pr_stats.repo_metadata.owner,
            "repo_name": pr_stats.repo_metadata.repo,
            "processed_at": pr_stats.repo_metadata.processed_at,
            "stats": stats_data
        })

        # 3. Enviar en segundo plano
        background_tasks.add_task(send_bulk_documents, "github_pr_stats", documents)

        return pr_stats

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
