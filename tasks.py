# -*- coding: utf-8 -*-
from invoke import task

from tests.desktop_tests import DesktopTests


@task
def open_test(c, version=None, display=False, config=None, telegram=False, license=None):
    DesktopTests(
        version=version,
        virtual_display=display,
        custom_config=config if config else None,
        telegram=telegram,
        license_file_path=license
    ).open_test()

@task
def update_test(c, version=None, update_from=None, display=False, config=None, telegram=False, license=None):
    DesktopTests(
        version=version,
        virtual_display=display,
        custom_config=config if config else None,
        telegram=telegram,
        old_version=update_from,
        license_file_path=license
    ).update_test()

@task
def install_desktop(c, version=None, config=None, license=None):
    test = DesktopTests(
        version=version,
        virtual_display=False,
        custom_config=config if config else None,
        license_file_path=license
    )
    test.install_package()
    test.check_installed()
    test.check_correct_version()
    test.desktop.set_license()
    test.desktop.open(debug_mode=True)
