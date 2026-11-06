import os
import shutil
import zipfile
from pathlib import Path
from typing import Dict
from . import translation_paths
from .project_config import ProjectConfig


def clear_extract_folder(extract_path: Path):
    if extract_path.exists():
        shutil.rmtree(extract_path)  # Remove all contents of the folder
    extract_path.mkdir(parents=True, exist_ok=True)  # Recreate the empty folder

def extract_translation_zip(zip_path: Path, extract_path: Path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

def clean_translation_folder_structure(extract_path: Path):
    for root, _, files in os.walk(extract_path):
        for file in files:
            if file.endswith(".po"):
                # Define original path and desired new path
                original_path = Path(root) / file

                # Get the language folder name - find the first folder after extract_path
                relative_path = original_path.relative_to(extract_path)
                language_folder = relative_path.parts[0]  # First part is the language folder

                # Define new path for .po file
                new_path = extract_path / language_folder / file

                # Ensure the language folder exists
                (extract_path / language_folder).mkdir(parents=True, exist_ok=True)

                # Move the .po file to the new path and remove the old folder if empty
                shutil.move(original_path, new_path)
                old_folder = original_path.parent
                if not list(old_folder.glob("*")):  # Remove old folder if empty
                    old_folder.rmdir()

def apply_renaming_rules(extract_path: Path, languages_code_rename: Dict[str, str]):
    for dir_name in extract_path.iterdir():
        if dir_name.is_dir() and dir_name.name in languages_code_rename:
            new_dir_name = languages_code_rename[dir_name.name]
            new_dir_path = extract_path / new_dir_name
            dir_name.rename(new_dir_path)

def apply_exclusion_rules(extract_path: Path, languages_code_to_exclude: list[str]):
    for lang_code in languages_code_to_exclude:
        lang_folder = extract_path / lang_code
        if lang_folder.exists() and lang_folder.is_dir():
            shutil.rmtree(lang_folder)

def extract_translation(project_config: ProjectConfig):
    file_path: Path = translation_paths.get_translations_download_path()
    extract_path: Path = translation_paths.get_translations_extract_path()

    # Ensure the extraction folder exists, and clear it if it does
    clear_extract_folder(extract_path)

    # Extract the ZIP file
    extract_translation_zip(file_path, extract_path)

    # Rearrange folder structure
    clean_translation_folder_structure(extract_path)

    # Apply renaming rules to folders after rearranging files
    apply_renaming_rules(extract_path, project_config.languages_code_rename)

    # Apply exclusion rules to remove unwanted language folders
    apply_exclusion_rules(extract_path, project_config.languages_code_to_exclude)

    print(f"Translations extracted to {extract_path}")
    return extract_path