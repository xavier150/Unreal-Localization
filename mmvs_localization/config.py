import json
from typing import Dict, List
from pathlib import Path

# POEditor API Key
api_token: str = "xxxxxxxxxxxxx" #dtv5

# Crowdin Project ID
project_id: int = 735873 #Macro Micro VR Service


def load_project_id(config_path: Path) -> None:
    global project_id

    try:
        with config_path.open(encoding="utf-8") as config_file:
            project_config = json.load(config_file)
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in configuration file '{config_path}': {error}") from error

    if not isinstance(project_config, dict):
        raise ValueError(f"Configuration file '{config_path}' must contain a JSON object.")

    loaded_project_id = project_config.get("project_id")
    if isinstance(loaded_project_id, bool) or not isinstance(loaded_project_id, int) or loaded_project_id <= 0:
        raise ValueError(f"Configuration file '{config_path}' must contain a positive integer 'project_id'.")

    project_id = loaded_project_id


relative_download_translations_path: Path = Path("ExportedTranslations/Downloaded")
download_translations_filename: str = "translations.zip"

relative_translations_export_path: Path = Path("ExportedTranslations/Extracted")

languages_code_rename: Dict[str, str] = {
    "es-ES": "es", # Crowdin uses 'es-ES' for Spanish, but we want 'es'
    "pt-PT": "pt", # Crowdin uses 'pt-PT' for Portuguese, but we want 'pt'
    "zh-CN": "zh-Hans", # Crowdin uses 'zh-CN' for Simplified Chinese, but we want 'zh-Hans'
    "zh-TW": "zh-Hant", # Crowdin uses 'zh-TW' for Traditional Chinese, but we want 'zh-Hant'
}

languages_code_to_exclude: List[str] = [
    "en",  # English is the source language, not a translation
]

# PROJECT CONFIGURATION
project_path: Path = Path('M:/MMVS_ProjectFiles_v2/UnrealProject/MacroMicroVRService.uproject')
relative_copy_to_project_path: Path = Path("Content/Localization/MacroMicroVRService")

crowdin_download_max_attempts: int = 3
crowdin_delay_between_attempts_seconds: int = 5

post_copy_instructions: str = f"""
You can now import them into Unreal Engine.
1. Tools -> Localization Dashboard
4. In Localization Dashboard -> Game Targets, Click "Gather Text for all targets in the project".
2. Go in Localization Dashboard -> Game Targets -> MacroMicroVRService 
3. Click "Import Text", import from the extracted translations in "{relative_copy_to_project_path}"
4. Return in Localization Dashboard -> Game Targets. Click again "Gather Text for all targets in the project".
6. And Click "Compile Translations for all targets in the project".

Update translation sounrce in Crowdin:
1. Tools -> Localization Dashboard -> Game Targets -> MacroMicroVRService -> English -> Export Translations for this culture.
2. Save as "MacroMicroVRService.po" in a temporary location.
3. Go in Crowdin -> MMVS -> Sources: https://crowdin.com/project/MMVS/sources/files
4. In en -> MacroMicroVRService.po, Click "Upload" and select the exported "MacroMicroVRService.po" file.
"""