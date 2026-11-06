from pathlib import Path

from .project_config import ProjectConfig


def get_project_directory_path(project_config: ProjectConfig) -> Path:
    """Folder containing the .uproject file."""
    return project_config.project_path.parent


def get_copy_to_project_path(project_config: ProjectConfig) -> Path:
    """Configured destination for copying translations."""
    return project_config.project_export_path
