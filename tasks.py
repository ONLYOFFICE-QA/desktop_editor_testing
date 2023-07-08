# -*- coding: utf-8 -*-
from invoke import task

from tests.desktop_test import DesktopTest


@task
def desktop_test(c, version=None, display=False, custom_config=None, telegram=False, license_file_path=None):
    DesktopTest(
        version=version,
        display_on=True if not display else False,
        custom_config=custom_config if custom_config else None,
        telegram=telegram,
        license_file_path=license_file_path
    ).run()
