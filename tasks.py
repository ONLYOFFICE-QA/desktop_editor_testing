# -*- coding: utf-8 -*-
from invoke import task

from tests.desktop_test import DesktopTest


@task
def desktop_test(c, version=None, display=False, config=None, telegram=False, license=None):
    DesktopTest(
        version=version,
        virtual_display=display,
        custom_config=config if config else None,
        telegram=telegram,
        license_file_path=license
    ).run()

@task
def install_desktop(c, version=None, config=None, license=None):
    test = DesktopTest(
        version=version,
        virtual_display=False,
        custom_config=config if config else None,
        license_file_path=license
    )
    test.install_package()
    test.check_installed()
    test.check_correct_version()
    test.desktop.set_license()
    test.desktop.open()
