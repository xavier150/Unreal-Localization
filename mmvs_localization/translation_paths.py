from pathlib import Path
from . import config 
from .project_config import ProjectConfig

def get_translations_download_path(work_directory: Path) -> Path:
    return work_directory / config.download_translations_filename


def get_translations_extract_path(work_directory: Path) -> Path:
    return work_directory / "Extracted"

def get_project_path(project_config: ProjectConfig) -> Path:
    return project_config.project_path


def get_copy_to_project_path(project_config: ProjectConfig) -> Path:
    from . import unreal_engine_path
    return unreal_engine_path.get_copy_to_project_path(project_config)