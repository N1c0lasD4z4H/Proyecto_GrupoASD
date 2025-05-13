from datetime import datetime, timezone
from typing import Dict, Any
from Github_Request.issue_request import GithubIssueAPI


class GithubIssueService:
    @staticmethod
    def analyze_issues(owner: str, repo: str) -> Dict[str, Any]:
        try:
            issues = GithubIssueAPI.get_repo_issues(owner, repo)

            # Estructuras dinámicas para clasificación y tendencias
            classified = {}
            all_issues = []

            for issue in issues:
                labels = [lbl["name"].lower() for lbl in issue.get("labels", [])]
                labels = labels or ["unlabeled"]  # Si no hay etiquetas, asignar "unlabeled"

                # Métricas de tiempo
                created_at = issue["created_at"]
                closed_at = issue["closed_at"]
                resolution_time = (
                    (datetime.fromisoformat(closed_at.replace("Z", "+00:00")) -
                     datetime.fromisoformat(created_at.replace("Z", "+00:00"))).total_seconds()
                    if closed_at else None
                )
                last_response_time = (
                    datetime.fromisoformat(issue["updated_at"].replace("Z", "+00:00")) -
                    datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                ).total_seconds()

                issue_data = {
                    "issue_id": issue["id"],
                    "number": issue["number"],
                    "url": issue["html_url"],
                    "author": issue.get("user", {}).get("login"),
                    "title": issue["title"],
                    "labels": labels,
                    "created_at": created_at,
                    "closed_at": closed_at,
                    "state": issue["state"],
                    "resolution_time": resolution_time,
                    "last_response_time": last_response_time
                }

                all_issues.append(issue_data)

            # Estadísticas generales
            total_issues = len(issues)
            open_issues = sum(1 for iss in issues if iss["state"] == "open")
            closed_issues = total_issues - open_issues
            avg_resolution_time = (
                sum(iss["resolution_time"] for iss in all_issues if iss["resolution_time"]) / closed_issues / 86400
                if closed_issues else None
            )

            return {
                "repository": f"{owner}/{repo}",
                "stats": {
                    "total": total_issues,
                    "open": open_issues,
                    "closed": closed_issues,
                    "avg_resolution_time": round(avg_resolution_time, 2) if avg_resolution_time else None
                },
                "issues": all_issues,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        except Exception as e:
            return {"error": str(e)}
