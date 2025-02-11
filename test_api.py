# -*- coding: utf-8 -*-
from frameworks.github_api import GitHubApi

if __name__ == '__main__':
    api = GitHubApi(repo_owner="ONLYOFFICE", repo_name="appimage-desktopeditors")
    workflows = api.workflow.get()
    print(workflows)
    if workflows:
        for workflow in workflows:
            if workflow.get('name', '') == "Build APPIMAGE package":
                id = workflow["id"]
                break

        else:
            id = 0
    print(id)
    runs = api.workflow.get_runs(workflow_id=id)
    if runs:
        for run in runs:
            artifacts = api.artifacts.get(run_id=run["id"])
            for artifact in artifacts:
                print(f"- {artifact['name']} (Download URL: {artifact['archive_download_url']})")