import requests
import json

class State:
    error = "error"
    pending = "pending"
    failure = "failure"
    success = "success"

class GithubCommon:
    def __init__(self, context):
        self.context = context

    # branch: name of the branch
    def get_branch(self, branch):
        r = requests.get("{api}/repos/{owner}/{repo}/branches/{branch}"
            .format(
                api=self.context.github_api,
                owner=self.context.owner,
                repo=self.context.repo,
                branch=branch))

        if r.ok:
            return json.loads(r.text)
        else:
            return None

    # sha: sha hash of commit
    # status_ok: True/False
    # desc_extention: additional text to "rebased/not rebased"
    def set_commit_status(self, sha, status_ok, desc_extention=""):
        if status_ok:
            state = State.success
            desc = self.context.rebased + desc_extention
        else:
            state = State.error
            desc = self.context.not_rebased + desc_extention

        data = {
            "state": state,
            "target_url": self.context.target_url,
            "description": desc,
            "context": self.context.botname
        }

        r = requests.post("{api}/repos/{owner}/{repo}/statuses/{sha}"
            .format(
                api=self.context.github_api,
                owner=self.context.owner,
                repo=self.context.repo,
                sha=sha),
            json=data,
            headers={
                "Authorization": "token {token}".format(
                        token=self.context.token
                    )
            })

        return r.ok

    def get_open_pull_requests(self):
        data = {
            "state": "open"
        }

        r = requests.get("{api}/repos/{owner}/{repo}/pulls"
            .format(
                api=self.context.github_api,
                owner=self.context.owner,
                repo=self.context.repo,
                ),
            json=data)

        if r.ok:
            return json.loads(r.text)
        else:
            return None
