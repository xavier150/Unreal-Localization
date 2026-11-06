from . import crowdin_export
from . import extract_translation
from . import copy_translation_in_project
from . import bpl
from .project_config import ProjectConfig


def main(project_config: ProjectConfig, api_token: str):
    bpl.console_utils.clear_console()
    bpl.advprint.print_simple_title("MMVS Localization Tool")

    run_download_translation(project_config, api_token, True, True, True)


def run_download_translation(
    project_config: ProjectConfig,
    api_token: str,
    download: bool = True, 
    extract: bool = True,
    copy_to_project: bool = True
):
    # Download translations from Crowdin

    if download:
        print(bpl.color_set.green("STEP 1: Downloading translations from Crowdin..."))
        result = crowdin_export.start_export(project_config, api_token)
        if not result:
            print("Error during download. Exiting.")
            return
    if extract:
        print(bpl.color_set.green("STEP 2: Extracting and processing translations..."))
        result = extract_translation.extract_translation()
        if not result:
            print("Error during extraction. Exiting.")
            return

    if copy_to_project:
        print(bpl.color_set.green("STEP 3: Copying translations to project..."))
        result = copy_translation_in_project.copy_translations_to_project()
        if not result:
            print("Error during copying translations to project. Exiting.")
            return