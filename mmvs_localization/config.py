download_translations_filename: str = "translations.zip"

crowdin_download_max_attempts: int = 3
crowdin_delay_between_attempts_seconds: int = 5

post_copy_instructions: str = """
You can now import them into Unreal Engine.
Open Tools -> Localization Dashboard.
1. In Localization Dashboard -> Game Targets, click "Gather Text for all targets in the project".
2. In Localization Dashboard -> Game Targets, select your localization target.
3. Click "Import Text" and import from "{project_export_path}".
4. Return to Localization Dashboard -> Game Targets and click "Gather Text for all targets in the project" again.
5. Click "Compile Translations for all targets in the project".

To update source translations in Crowdin:
1. Open Tools -> Localization Dashboard -> Game Targets -> your localization target -> its source culture,
   then click "Export Translations for this culture".
2. Save the source .po file in a temporary location.
3. Open your Crowdin project's Sources page.
4. In the source language folder, select the corresponding .po file, click "Upload",
   and select the exported .po file.
"""