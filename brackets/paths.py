from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
DATA_DIR = PACKAGE_DIR / "data"
TEMPLATES_DIR = PACKAGE_DIR / "templates"
STATIC_DIR = PACKAGE_DIR / "static"
OUTPUTS_DIR = PACKAGE_DIR / "outputs"


def data_path(name):
    return DATA_DIR / name


def template_path(name):
    return TEMPLATES_DIR / name


def static_path(name):
    return STATIC_DIR / name


def output_path(name):
    return OUTPUTS_DIR / name