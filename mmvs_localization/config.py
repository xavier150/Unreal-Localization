from pathlib import Path

relative_download_translations_path: Path = Path("ExportedTranslations/Downloaded")
download_translations_filename: str = "translations.zip"

relative_translations_export_path: Path = Path("ExportedTranslations/Extracted")

crowdin_download_max_attempts: int = 3
crowdin_delay_between_attempts_seconds: int = 5

post_copy_instructions: str = """
You can now import them into Unreal Engine.
1. Tools -> Localization Dashboard
4. In Localization Dashboard -> Game Targets, Click "Gather Text for all targets in the project".
2. Go in Localization Dashboard -> Game Targets -> MacroMicroVRService 
3. Click "Import Text", import from the extracted translations in "{project_export_path}"
4. Return in Localization Dashboard -> Game Targets. Click again "Gather Text for all targets in the project".
6. And Click "Compile Translations for all targets in the project".

Update translation sounrce in Crowdin:
1. Tools -> Localization Dashboard -> Game Targets -> MacroMicroVRService -> English -> Export Translations for this culture.
2. Save as "MacroMicroVRService.po" in a temporary location.
3. Go in Crowdin -> MMVS -> Sources: https://crowdin.com/project/MMVS/sources/files
4. In en -> MacroMicroVRService.po, Click "Upload" and select the exported "MacroMicroVRService.po" file.
"""