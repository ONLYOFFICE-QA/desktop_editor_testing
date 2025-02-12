# -*- coding: utf-8 -*-
from invoke import task
from tests import OpenTest, SnapOpenTest, FlatPakOpenTest, AppImageOpenTest, TestTools, TestData


@task
def open_test(
        c,
        version: str = None,
        update_from: str = None,
        display: bool = False,
        config: str = None,
        telegram: bool = False,
        license: str = None,
        snap: bool = False,
        appimage: bool = False,
        flatpak: bool = False
):
    config = TestData(
        version=version,
        update_from=update_from,
        virtual_display=display,
        custom_config=config if config else None,
        telegram=telegram,
        license_file_path=license,
        snap=snap,
        appimage=appimage
    )

    if snap:
        SnapOpenTest(test_data=config).run()
    elif appimage:
        AppImageOpenTest(test_data=config).run()
    elif flatpak:
        FlatPakOpenTest(test_data=config)
    else:
        OpenTest(test_data=config).run()


@task
def install_desktop(c, version: str = None, config: str = None, license: str = None, debug: bool = False):
    tools = TestTools(
        TestData(
            version=version,
            virtual_display=False,
            custom_config=config if config else None,
            license_file_path=license
        )
    )

    tools.install_package(desktop=tools.desktop)
    tools.check_installed()
    tools.check_correct_version()
    tools.desktop.set_license()
    tools.desktop.open(debug_mode=debug)
