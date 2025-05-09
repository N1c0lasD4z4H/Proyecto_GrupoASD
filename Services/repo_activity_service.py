from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
from Github_Request.repo_activity_request import GitHubRequest
import logging

logger = logging.getLogger(__name__)

class GitHubService:
    def __init__(self):
        self.github_request = GitHubRequest()
        
    def _process_commits(self, commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        weekly_activity = {}
        commit_history = []
        last_commit_date = None
        authors = set()
        
        for commit in commits:
            try:
                if not isinstance(commit, dict):
                    logger.warning("Invalid commit format, skipping")
                    continue
                    
                commit_data = commit.get('commit', {})
                if not commit_data:
                    continue
                    
                author_info = commit_data.get('author', {})
                author_date_str = author_info.get('date')
                if not author_date_str:
                    continue
                    
                # Procesar autor
                author = commit.get('author', {}).get('login', 'Unknown')
                authors.add(author)
                
                # Procesar fecha
                try:
                    author_date = datetime.strptime(author_date_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

                except ValueError:
                    logger.warning(f"Invalid date format: {author_date_str}")
                    continue
                
                # Actualizar última fecha de commit
                if not last_commit_date or author_date > last_commit_date:
                    last_commit_date = author_date
                    
                # Registrar datos del commit
                commit_history.append({
                    "author": author,
                    "date": author_date.isoformat(),
                    "message": commit_data.get('message', '')[:200],  # Limitar tamaño
                    "sha": commit.get('sha', '')[:10]  # Acortar SHA
                })
                
                # Contar actividad semanal
                if datetime.now(timezone.utc) - author_date <= timedelta(days=7):
                    weekly_activity[author] = weekly_activity.get(author, 0) + 1
                    
            except Exception as e:
                logger.error(f"Error processing commit: {str(e)}")
                continue
                
        return {
            "total_commits": len(commits),
            "weekly_activity": {
                "period_start": (datetime.now(timezone.utc) - timedelta(days=7)).isoformat(),
                "period_end": datetime.now(timezone.utc).isoformat(),
                "count_by_author": weekly_activity,
                "total": sum(weekly_activity.values())
            },
            "last_commit": last_commit_date.isoformat() if last_commit_date else None,
            "commit_history": commit_history,
            "authors": list(authors)
        }

    async def get_repo_activity(self, owner: str, repo: str) -> Dict[str, Any]:
        try:
            if not owner or not repo:
                raise ValueError("Owner and repo parameters are required")
                
            # Llama al cliente asincrónico sin pasar token
            commits = await self.github_request.get_commits(owner, repo)
            
            result = {
                "status": "success",
                "repo": repo,
                "owner": owner,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            if not commits:
                result.update({
                    "message": "No commits found",
                    "total_commits": 0,
                    "weekly_activity": {
                        "period_start": (datetime.now(timezone.utc) - timedelta(days=7)).isoformat(),
                        "period_end": datetime.now(timezone.utc).isoformat(),
                        "count_by_author": {},
                        "total": 0
                    }
                })
            else:
                result.update(self._process_commits(commits))
                
            return result
            
        except Exception as e:
            logger.error(f"Error in get_repo_activity: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "repo": repo,
                "owner": owner,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }