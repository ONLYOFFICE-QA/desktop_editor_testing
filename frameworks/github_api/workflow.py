# -*- coding: utf-8 -*-
from .api_requests import ApiReqeust


class Workflow:

    def __init__(self, host_url: str):
        self.host_url = host_url
        self.request = ApiReqeust()

    def get(self) -> list:
        return self.request.get(f"{self.host_url}/actions/workflows").get("workflows", [])

    def get_runs(self, workflow_id: str) -> list:
        return self.request.get(f"{self.host_url}/actions/workflows/{workflow_id}/runs").get("workflow_runs", [])
