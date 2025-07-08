# -*- coding: utf-8 -*-
# import win32gui
# import win32con
import os

import requests

from frameworks.desktop.package import SnapPackage


def get_hwnd(class_name: str, text: str):
    data = []

    def enum_windows_callback(hwnd: int, data: list):
        if win32gui.IsWindowVisible(hwnd):
            _cls_name, _text = win32gui.GetClassName(hwnd), win32gui.GetWindowText(hwnd)
            print(_cls_name.strip(), _text.strip())
            if class_name.strip() == _cls_name.strip() and text.strip() == _text.strip():
                print(class_name, text)
                data.append(hwnd)

    win32gui.EnumWindows(enum_windows_callback, data)
    print(data)
    return data[0] if data else None

# def get_child_window_hwnd(window_hwnd: int, child_window_title: str, child_window_text: str):
#     data = []
#
#     def find_button(hwnd, data: list):
#         cls_name, text = win32gui.GetClassName(hwnd), win32gui.GetWindowText(hwnd)
#         print(cls_name, text)
#         if cls_name in child_window_title and child_window_text in text:
#             data.append(hwnd)
#
#     win32gui.EnumChildWindows(window_hwnd, find_button, data)
#     return data[0] if data else None

def close(hwnd: int) -> None:
    try:
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    except Exception as e:
        print(f"[red]|WARNING| Can't close the window. Exception: {e}")

def click_on_button(button_hwnd: int):
    try:
        win32gui.SendMessage(button_hwnd, win32con.BM_CLICK, 0, 0)
    except Exception as ex:
        print(ex)


# window_hwnd = get_hwnd('Qt5QWindowIcon', 'ONLYOFFICE Desktop Editors')
#
# print(window_hwnd)
# close(window_hwnd)

# from subprocess import call, getoutput
# out = getoutput('snap version')
# print(out)

if __name__ == '__main__':
    # print(any([True, False, False]))
    resp = requests.get('https://dl.flathub.org/build-repo/164604/org.onlyoffice.desktopeditors.flatpakref')
    print(resp.status_code)
    # process_name = 'editors.exe'
    # os.system(f"taskkill /f /im {process_name}")

# button_hwnd = get_child_window_hwnd(
#     window_hwnd,
#     'Button',
#     'No'
# )
#
# print(button_hwnd)
#
# if button_hwnd:
#     click_on_button(button_hwnd)


test = """
(function()
{
    let doc = Api.GetDocument();
    let paragraph = Api.CreateParagraph();
    paragraph.AddText("Hello world!");
    doc.InsertContent([paragraph]);
})();
"""

