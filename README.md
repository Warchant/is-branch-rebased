# is-branch-rebased
Github Bot, which checks if pull requests and branches are rebased or not


# Usage

### Open *-webhook.py file and make these changes:

```python3
ctx = GithubContext(
        token="", # github account personal token
        owner="", # repository owner
        repo=""   # repository name
    )
```

Also, change host and port for webhook:
```python3
app.run(host="0.0.0.0", port=12345)
```

### Run webhook with python3

```bash
$ python3 isbranchrebased-webhook.py
```

### Create webhook on github repo with rights "push" and "pull request"

And specify webhook's host+port.
