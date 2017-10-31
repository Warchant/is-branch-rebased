#!/usr/bin/env python3

from context import GithubContext
from rebase_checker import RebaseChecker 
from flask import Flask, request

app = Flask(__name__)

ctx  = GithubContext(
    token="",
    owner="",
    repo="",
    base=""
    )

checker = RebaseChecker(ctx)


@app.route("/", methods=["POST"])
def handle():
    data = request.get_json(silent=True)

    gh_event = request.headers.get('X-GitHub-Event')

    if gh_event == "pull_request":
        checker.after_pr_update(data)
    elif gh_event == "push":
        checker.after_push(data)
    else:
        print("unrecognized gh_event: {0}".format(gh_event))

    return "ok"


if __name__ == "__main__":
    app.run()
