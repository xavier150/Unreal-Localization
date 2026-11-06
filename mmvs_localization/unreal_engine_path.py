from pathlib import Path

from . import config


def get_project_directory_path() -> Path:
    """Folder containing the .uproject file."""
    return config.project_path.parent


def get_copy_to_project_path() -> Path:
    """Full path for copying translations to the project, relative to the project directory."""
    return get_project_directory_path() / config.relative_copy_to_project_path
