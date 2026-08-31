# -*- coding: utf-8 -*-
import platform
import re
import subprocess as sb
import sys

RELEASE = platform.release().lower()
OS = platform.system().lower()
REQUIREMENTS_FILE = "requirements.txt"
POETRY_FILE = "pyproject.toml"
EXCEPTIONS = {"python"}
PYTHON36_VERSIONS = {
    "opencv-python": "4.3.0.38",
    "rich": "12.6.0",
    "pillow": "8.4.0"
}

WINDOWS_VISTA = {
    "pywin32": "223"
}


def ensure_ssl():
    """Fail early if Python has no SSL — pip cannot talk to PyPI over HTTPS."""
    try:
        import ssl  # noqa: F401
    except ImportError:
        print(
            "ERROR: Python SSL module is missing, pip cannot download packages.\n"
            "On Debian/Ubuntu: sudo apt-get install -y libssl3 libssl-dev ca-certificates\n"
            "If Python was built from source, reinstall it after libssl-dev and recreate the venv.\n"
            "Check: python3 -c 'import ssl; print(ssl.OPENSSL_VERSION)'",
            file=sys.stderr,
        )
        sys.exit(1)


def pip_install(*args):
    """Run pip via the current interpreter.
    :param args: Arguments passed to `pip install`
    """
    cmd = [sys.executable, "-m", "pip", "install", *args]
    result = sb.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)


def load_poetry_data():
    """Parse pyproject.toml. Use stdlib tomllib on Python 3.11+ so pip/SSL is not required."""
    if sys.version_info >= (3, 11):
        import tomllib
        with open(POETRY_FILE, "rb") as f:
            return tomllib.load(f)

    try:
        import tomlkit
    except ImportError:
        pip_install("tomlkit==0.11.6")
        import tomlkit

    with open(POETRY_FILE, "r") as f:
        return tomlkit.parse(f.read())


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

    poetry_data = load_poetry_data()

    dependencies = poetry_data.get("tool", {}).get("poetry", {}).get("dependencies", {})
    for package, version_info in dependencies.items():
        if package.lower() in EXCEPTIONS:
            continue

        version = get_dependency_version(package, version_info, is_old_python)
        if package.lower() == "pywin32" and OS != "windows":
            continue
        write_to_file(f"{package}=={version}\n" if version else f"{package}\n", "a")

def upgrade_pip():
    pip_install("--upgrade", "pip")

def install_requirements():
    pip_install("-r", REQUIREMENTS_FILE)

if __name__ == "__main__":
    ensure_ssl()
    upgrade_pip()
    write_to_file("# -*- coding: utf-8 -*-\n", "w")
    generate_requirements()
    install_requirements()
