def value_or_default(kv, k, default):
    if k in kv:
        return kv[k]
    else:
        return default

class GithubContext:
    def __init__(self, **kwargs):
        # mandatory args        
        self.owner = kwargs["owner"]
        self.repo  = kwargs["repo"]
        self.token = kwargs["token"]

        # optional args
        self.github_api = value_or_default(kwargs, "api", 
            "https://api.github.com")
        self.target_url = value_or_default(kwargs, "target_url", 
            "https://soramitsu.atlassian.net/wiki/spaces/IS/pages/11173889/Rebase+and+merge+guide")
        
        self.botname = value_or_default(kwargs, "botname", 
            "Is branch rebased?")
        self.rebased = value_or_default(kwargs, "rebased", 
            "rebased")
        self.not_rebased = value_or_default(kwargs, "not_rebased", 
            "not rebased")
