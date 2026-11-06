import importlib

from . import bpl
from . import main
from . import config
from . import project_config
from . import config_loader
from . import crowdin_export
from . import translation_paths
from . import extract_translation
from . import copy_translation_in_project

if "bpl" in locals():
    importlib.reload(bpl)
if "main" in locals():
    importlib.reload(main)
if "config" in locals():
    importlib.reload(config)
if "project_config" in locals():
    importlib.reload(project_config)
if "config_loader" in locals():
    importlib.reload(config_loader)
if "crowdin_export" in locals():
    importlib.reload(crowdin_export)
if "translation_paths" in locals():
    importlib.reload(translation_paths)
if "extract_translation" in locals():
    importlib.reload(extract_translation)
if "copy_translation_in_project" in locals():
    importlib.reload(copy_translation_in_project)
