# -*- coding: utf-8 -*-
from .artifacts import Artifacts
from .workflow import Workflow


class GitHubApi:
    __host = "https://api.github.com/repos"

    def __init__(self, repo_owner: str, repo_name: str):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.host = f"{self.__host}/{repo_owner}/{repo_name}"
        self.workflow = Workflow(host_url=self.host)
        self.artifacts = Artifacts(host_url=self.host)
