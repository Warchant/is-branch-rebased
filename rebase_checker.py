from common import GithubCommon
from context import GithubContext 
import json

class RebaseChecker:
    def __init__(self, context):
        self.context = context
        self.common = GithubCommon(self.context)

    # data - parsed json, which we receive from github after
    # any PR update
    def after_pr_update(self, data):
        pr = data["pull_request"]
        prhead = pr["head"]
        prbase = pr["base"]
        prbase_sha = prbase["sha"]
        prhead_sha = prhead["sha"]

        base = self.common.get_latest_branch(self.context.base)
        base_sha = base["commit"]["sha"]

        self.__update_status(prhead_sha, base_sha == prbase_sha)

    # data - parsed json, which we receive from github after any push
    def after_push(self, data):
        ref = data["ref"]
        branch = ref.replace("refs/heads/", "")

        print("received push to {0}".format(branch))

        if branch == self.context.base:
            # we should update all pull requests' statuses
            base_sha_after = data["after"]

            prs = self.common.get_open_pull_requests()
            for pr in prs:
                base = pr["base"]
                html = pr["_links"]["html"]["href"]
                base_label = base["label"]

                # if pr base is not "base" stored in context, then ignore this pull request
                if base_label.lower() != self.context.label:
                    print("pr {0} has label {1}, not {2}".format(
                        html,
                        base_label.lower(),
                        self.context.label
                    ))
                    continue

                head = pr["head"]
                head_sha = head["sha"]
                base_sha = base["sha"]

                self.__update_status(head_sha, base_sha == base_sha_after)



    async def __update_status(self, sha, status):
        ok = self.common.set_commit_status(sha, status)
        print("status for {0} ".format(sha), end="")
        if ok:
            print("updated: {0}".format(status))
        else:
            print("not updated")
