from datetime import datetime
from typing import Dict, List, Any
from Github_Request.pr_time_request import GithubPRAPI
import logging

logger = logging.getLogger(__name__)

class PRDashboardService:
    @staticmethod
    async def get_enriched_pull_requests(owner: str, repo: str) -> Dict[str, Any]:
        try:
            prs = await GithubPRAPI.get_repo_pull_requests(owner, repo)
            enriched = []
            stats = {
                "total": 0,
                "open": 0,
                "closed": 0,
                "merged": 0,
                "with_reviews": 0,
                "drafts": 0,
                "conflicts": 0
            }

            for pr in prs:
                try:
                    # Procesamiento básico
                    created_at = datetime.fromisoformat(pr["created_at"].replace("Z", "+00:00"))
                    closed_at = pr.get("closed_at")
                    closed_at_dt = datetime.fromisoformat(closed_at.replace("Z", "+00:00")) if closed_at else None
                    is_merged = pr.get("merged_at") is not None

                    # Actualizar estadísticas
                    stats["total"] += 1
                    if closed_at:
                        stats["closed"] += 1
                        if is_merged:
                            stats["merged"] += 1
                    else:
                        stats["open"] += 1
                    if pr.get("draft", False):
                        stats["drafts"] += 1

                    # Obtener revisiones
                    reviews = await GithubPRAPI.get_pull_request_reviews(owner, repo, pr["number"])
                    first_review = min(reviews, key=lambda r: r["submitted_at"]) if reviews else None
                    if first_review:
                        stats["with_reviews"] += 1

                    # Construir documento enriquecido
                    enriched_pr = {
                        "pr_id": pr["id"],
                        "number": pr["number"],
                        "url": pr["html_url"],
                        "author": pr["user"]["login"],
                        "created_at": pr["created_at"],
                        "closed_at": closed_at,
                        "merged_at": pr.get("merged_at"),
                        "state": "open" if not closed_at else "merged" if is_merged else "closed",
                        "draft": pr.get("draft", False),
                        "review_count": len(reviews),
                        "first_review_at": first_review["submitted_at"] if first_review else None
                    }
                    enriched.append(enriched_pr)

                except Exception as e:
                    logger.error(f"Error processing PR #{pr.get('number')}: {str(e)}")
                    continue

            return {
                "repository": f"{owner}/{repo}",
                "stats": stats,
                "pull_requests": enriched,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in get_enriched_pull_requests: {str(e)}")
            return {
                "error": str(e),
                "repository": f"{owner}/{repo}",
                "timestamp": datetime.utcnow().isoformat()
            }