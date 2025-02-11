# -*- coding: utf-8 -*-
from .api_requests import ApiReqeust


class Artifacts:

    def __init__(self, host_url: str):
        self.host_url = host_url
        self.request = ApiReqeust()

    def get(self, run_id: str) -> list:
        return self.request.get(f"{self.host_url}/actions/runs/{run_id}/artifacts").get("artifacts", [])

    def downloads(self, artifact_url: str, output_dir_path: str) -> None:
        self.request.download(artifact_url, output_dir_path)
