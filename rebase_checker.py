from common import GithubCommon

class RebaseChecker:
    def __init__(self, context):
        self.context = context
        self.github = GithubCommon(self.context)

    # data - parsed json, which we receive from github after
    # any PR update
    def after_pr_update(self, data):
        pr = data["pull_request"]
        prhead = pr["head"]
        prbase = pr["base"]
        prbase_ref = prbase["ref"]
        prbase_sha = prbase["sha"]
        prhead_sha = prhead["sha"]

        base = self.github.get_branch(prbase_ref)
        base_sha = base["commit"]["sha"]

        self.__update_status(prhead_sha, base_sha == prbase_sha)

    # data - parsed json, which we receive from github after any push
    def after_push(self, data):
        ref = data["ref"]
        branch = ref.replace("refs/heads/", "")
        label = "{0}:{1}".format(
            self.context.owner.lower(),
            branch
        )

        print("received push to {0}".format(branch))

        # we should update all pull requests' statuses
        base_sha_after = data["after"]

        prs = self.github.get_open_pull_requests()
        for pr in prs:
            base = pr["base"]
            link = pr["_links"]["html"]["href"]
            pr_base_label = base["label"].lower()

            # if pr base is not "base" stored in context, then ignore this pull request
            if pr_base_label != label:
                print("pr {0} has label {1}, not {2}".format(
                    link,
                    pr_base_label,
                    label
                ))
                continue

            head = pr["head"]
            head_sha = head["sha"]
            base_sha = base["sha"]

            self.__update_status(head_sha, base_sha == base_sha_after)

    def __update_status(self, sha, status):
        ok = self.github.set_commit_status(sha, status)
        print("status for {0} ".format(sha), end="")
        if ok:
            print("updated: {0}".format(status))
        else:
            print("not updated")
