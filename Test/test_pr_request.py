import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Github_Request.pr_request import GithubPRAPI
 
class TestGithubPRAPI(unittest.TestCase):

    @patch("requests.get")

    def test_get_repo_pull_requests(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [

            {"id": 1, "state": "open", "title": "PR #1"},
            {"id": 2, "state": "closed", "title": "PR #2"}

        ]

        mock_get.return_value = mock_response
        owner = "test_owner"
        repo = "test_repo"
        state = "all"
        pull_requests = GithubPRAPI.get_repo_pull_requests(owner, repo, state)
        mock_get.assert_called_once_with(

            f"https://api.github.com/repos/{owner}/{repo}/pulls?state={state}",
            headers={"Authorization": f"Bearer {GithubPRAPI.TOKEN}"},
            params={"type": "all", "per_page": 100}

        )
 
        self.assertEqual(len(pull_requests), 2)
        self.assertEqual(pull_requests[0]["state"], "open")
        self.assertEqual(pull_requests[1]["state"], "closed")
 
if __name__ == "__main__":
    unittest.main()
    
     