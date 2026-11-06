from pathlib import Path

from . import config
from .project_config import ProjectConfig


def get_project_directory_path(project_config: ProjectConfig) -> Path:
    """Folder containing the .uproject file."""
    return project_config.project_path.parent


def get_copy_to_project_path(project_config: ProjectConfig) -> Path:
    """Full path for copying translations to the project, relative to the project directory."""
    return get_project_directory_path(project_config) / config.relative_copy_to_project_path
