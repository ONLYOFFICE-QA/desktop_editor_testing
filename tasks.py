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

@task
def install(c, version=None, custom_config=None, license_file_path=None):
    test = DesktopTest(
        version=version,
        display_on=False,
        custom_config=custom_config if custom_config else None,
        license_file_path=license_file_path
    )
    test.install_package()
    test.check_installed()
    test.check_correct_version()
    test.desktop.set_license()
    test.desktop.open()
