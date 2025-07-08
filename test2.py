# -*- coding: utf-8 -*-
import os
import re

from frameworks.github_api import GitHubApi, PullRequest
from frameworks.host_control import FileUtils

if __name__ == '__main__':
    # api = GitHubApi(repo_owner="ONLYOFFICE", repo_name="appimage-desktopeditors")
    # workflows = api.workflow.get()
    # print(workflows)
    # if workflows:
    #     for workflow in workflows:
    #         if workflow.get('name', '') == "Build APPIMAGE package":
    #             id = workflow["id"]
    #             break
    #
    #     else:
    #         id = 0
    # print(id)
    # runs = api.workflow.get_runs(workflow_id=id)
    # if runs:
    #     for run in runs:
    #         artifacts = api.artifacts.get(run_id=run["id"])
    #         for artifact in artifacts:
    #             print(artifact)
    #             print(f"- {artifact['name']} (Download URL: {artifact['archive_download_url']})")
                # api.artifacts.downloads(artifact['archive_download_url'], output_dir=os.getcwd(), file_name=f"{artifact['name']}.zip")
    # FileUtils.unpacking_zip(archive_path=r'C:\scripts\desktop_editor_testing\ONLYOFFICE_DesktopEditors-99.99.99-4135.zip', execute_path=os.getcwd())
    print(any([False, True, False]))

    # pr = PullRequest(repo_name="flathub/org.onlyoffice.desktopeditors", pull_num=142)
    # filtered_comments = [
    #     comment for comment in pr.get_all_comments() if re.search(r"flatpak install --user", comment["body"])
    # ]
    #
    # newest_comment = max(filtered_comments, key=lambda c: c["created_at"])
    # print(newest_comment['body'])
    #
    # command_match = re.search(r"flatpak install --user[^\n]*", newest_comment["body"])
    # command = command_match.group(0) if command_match else "Command not found"
    # print(command)



