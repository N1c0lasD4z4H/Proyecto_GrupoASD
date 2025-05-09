from Github_Request.template_request import GithubFileCheckAPI
from typing import Dict, Any
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class FileCheckService:
    @staticmethod
    async def analyze_pull_request_template(user_or_org: str) -> Dict[str, Any]:
        """Versión asíncrona con mejor manejo de errores"""
        try:
            repos = await GithubFileCheckAPI.list_user_repositories(user_or_org)
            if not repos:
                return {
                    "user_or_org": user_or_org,
                    "message": "No repositories found",
                    "repositories": []
                }

            paths_to_check = [
                "docs/PULL_REQUEST_TEMPLATE.md",
                ".github/PULL_REQUEST_TEMPLATE.md",
                ".github/pull_request_template.md",
                "docs/pull_request_template.md"
            ]

            repositories = []
            
            for repo in repos:
                try:
                    has_template = False
                    template_path = None
                    
                    for path in paths_to_check:
                        if await GithubFileCheckAPI.check_file_exists(repo, path):
                            has_template = True
                            template_path = path
                            break

                    repositories.append({
                        "repository": repo,
                        "has_template": has_template,
                        "template_path": template_path if has_template else None
                    })
                    
                except Exception as e:
                    logger.error(f"Error checking repo {repo}: {str(e)}")
                    repositories.append({
                        "repository": repo,
                        "has_template": False,
                        "error": str(e)
                    })

            return {
                "user_or_org": user_or_org,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "repositories": repositories,
                "stats": {
                    "total": len(repositories),
                    "with_template": sum(1 for r in repositories if r.get("has_template")),
                    "without_template": sum(1 for r in repositories if not r.get("has_template"))
                }
            }

        except Exception as e:
            logger.error(f"Error in analyze_pull_request_template: {str(e)}")
            return {
                "user_or_org": user_or_org,
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }