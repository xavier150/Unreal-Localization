import shutil
from pathlib import Path
from . import translation_paths
from . import config
from .project_config import ProjectConfig


def copy_translations_to_project(project_config: ProjectConfig) -> bool:
    copy_path: Path = translation_paths.get_copy_to_project_path(project_config)
    extract_path: Path = translation_paths.get_translations_extract_path()

    if not extract_path.exists():
        print(f"Extract path {extract_path} does not exist.")
        return False

    for lang_folder in extract_path.iterdir():
        if lang_folder.is_dir():
            # Define the target path in the project
            target_path = copy_path / lang_folder.name
            shutil.copytree(lang_folder, target_path, dirs_exist_ok=True)

    print(f"Translations copied to project at {copy_path}")
    print(config.post_copy_instructions.format(project_export_path=copy_path))
    return True