# -*- coding: utf-8 -*-
from .api_requests import ApiReqeust


class PullRequest:

    def __init__(self, repo_name: str, pull_num: int):
        self.repo_name = repo_name
        self.pull_num = pull_num
        self.request = ApiReqeust()

    def get_all_comments(self, per_page: int = 100):
        comments = []
        page = 1
        while True:
            url = f"https://api.github.com/repos/{self.repo_name}/issues/{self.pull_num}/comments?page={page}&per_page={per_page}"
            response = self.request.get(url)
            if not response:
                break
            comments.extend(response)
            page += 1
        return comments
