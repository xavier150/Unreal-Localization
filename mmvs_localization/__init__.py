import importlib
from . import main
from . import bpl
from . import config
from . import crowdin_export
from . import translation_paths
from . import extract_translation
from . import copy_translation_in_project

if "main" in locals():
    importlib.reload(main)
if "bpl" in locals():
    importlib.reload(bpl)
if "config" in locals():
    importlib.reload(config)
if "crowdin_export" in locals():
    importlib.reload(crowdin_export)
if "translation_paths" in locals():
    importlib.reload(translation_paths)
if "extract_translation" in locals():
    importlib.reload(extract_translation)
if "copy_translation_in_project" in locals():
    importlib.reload(copy_translation_in_project)


