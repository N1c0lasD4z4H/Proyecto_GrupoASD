from Github_Request.pr_time_request import GithubPRAPI
from datetime import datetime

class PRDashboardService:

    @staticmethod
    def get_enriched_pull_requests(owner: str, repo: str):
        prs = GithubPRAPI.get_repo_pull_requests(owner, repo)

        enriched = []
        open_count = 0
        closed_count = 0

        for pr in prs:
            created_at = datetime.fromisoformat(pr["created_at"].replace("Z", "+00:00"))
            closed_at = pr.get("closed_at")
            closed_at_dt = datetime.fromisoformat(closed_at.replace("Z", "+00:00")) if closed_at else None

            # Contadores
            if closed_at:
                closed_count += 1
            else:
                open_count += 1

            # Obtener revisión (si existe)
            reviews = GithubPRAPI.get_pull_request_reviews(owner, repo, pr["number"])
            if reviews:
                first_review = min(reviews, key=lambda r: r["submitted_at"])
                reviewed_at = first_review["submitted_at"]
                reviewer = first_review["user"]["login"]
                reviewed_at_dt = datetime.fromisoformat(reviewed_at.replace("Z", "+00:00"))
            else:
                reviewed_at = None
                reviewer = None
                reviewed_at_dt = None

            review_duration = (reviewed_at_dt - created_at).total_seconds() / 3600 if reviewed_at_dt else None
            total_duration = (closed_at_dt - created_at).total_seconds() / 3600 if closed_at_dt else None

            enriched.append({
                "PR_ID": f"PR-{pr['number']}",
                "Author": pr["user"]["login"],
                "Reviewer": reviewer,
                "Created_At": pr["created_at"],
                "Reviewed_At": reviewed_at,
                "Closed_At": closed_at,
                "Review_Duration_h": round(review_duration, 2) if review_duration else None,
                "Total_Duration_h": round(total_duration, 2) if total_duration else None
            })

        return {
            "owner_repo": f"{owner}/{repo}",
            "open_prs": open_count,
            "closed_prs": closed_count,
            "total_prs": len(prs),
            "pull_requests": enriched
        }

