from pathlib import Path
from . import config 
from .project_config import ProjectConfig

def get_localization_path() -> Path:
    # Get the absolute path of the current script
    full_path = Path(__file__).resolve()
    
    # Get the parent directory containing this script
    containing_folder = full_path.parent
    
    # Get the folder one level above the containing folder
    localization_path = containing_folder.parent

    return localization_path

def get_translations_download_path() -> Path:
    localization_path = get_localization_path()

    # Construct the full path for the translations file
    filename = config.download_translations_filename
    relative_path = config.relative_download_translations_path
    file_path = localization_path / relative_path / filename
    return file_path


def get_translations_extract_path() -> Path:
    localization_path = get_localization_path()

    path: Path = localization_path / config.relative_translations_export_path
    return path

def get_project_path(project_config: ProjectConfig) -> Path:
    return project_config.project_path


def get_copy_to_project_path(project_config: ProjectConfig) -> Path:
    from . import unreal_engine_path
    return unreal_engine_path.get_copy_to_project_path(project_config)