# -*- coding: utf-8 -*-
import platform
import re
import subprocess as sb

try:
    import tomlkit
except ImportError:
    sb.call("pip install tomlkit==0.11.6", shell=True)
    import tomlkit

RELEASE = platform.release().lower()
OS = platform.system().lower()
REQUIREMENTS_FILE = "requirements.txt"
POETRY_FILE = "pyproject.toml"
EXCEPTIONS = {"python"}
PYTHON36_VERSIONS = {
    "opencv-python": "4.3.0.38",
    "rich": "12.6.0"
}

WINDOWS_VISTA = {
    "pywin32": "223"
}


def write_to_file(content, mode="w"):
    with open(REQUIREMENTS_FILE, mode) as f:
        f.write(content)

def get_version_for_old_python(package):
    return PYTHON36_VERSIONS.get(package.lower(), "")

def get_dependency_version(package, version_info, is_old_python):
    if isinstance(version_info, dict):
        if "git" in version_info:
            return f"git+{version_info['git']}@{version_info.get('branch', 'main')}"
        if package.lower() == "pywin32":
            if RELEASE in ['vista', 'xp']:
                return re.sub(r"[*^]", "", WINDOWS_VISTA.get("pywin32", ""))
            return re.sub(r"[*^]", "", version_info.get("version", ""))
    elif is_old_python:
        return get_version_for_old_python(package)
    else:
        return re.sub(r"[*^]", "", version_info)
    return ""

def generate_requirements():
    is_old_python = int(platform.python_version_tuple()[1]) < 9  #  Python < 3.9

    with open(POETRY_FILE, "r") as f:
        poetry_data = tomlkit.parse(f.read())

    dependencies = poetry_data.get("tool", {}).get("poetry", {}).get("dependencies", {})
    for package, version_info in dependencies.items():
        if package.lower() in EXCEPTIONS:
            continue

        version = get_dependency_version(package, version_info, is_old_python)
        if package.lower() == "pywin32" and OS != "windows":
            continue
        write_to_file(f"{package}=={version}\n" if version else f"{package}\n", "a")

def upgrade_pip():
    sb.call("python -m pip install --upgrade pip", shell=True)

def install_requirements():
    sb.call(f"pip install -r {REQUIREMENTS_FILE}", shell=True)

if __name__ == "__main__":
    upgrade_pip()
    write_to_file("# -*- coding: utf-8 -*-\n", "w")  # Очистка файла
    generate_requirements()
    install_requirements()
