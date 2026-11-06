import json
import re
from pathlib import Path

from .project_config import ProjectConfig


def load_project_config(config_path: Path) -> ProjectConfig:
    try:
        with config_path.open(encoding="utf-8") as config_file:
            data = json.load(config_file)
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in configuration file '{config_path}': {error}") from error

    if not isinstance(data, dict):
        raise ValueError(f"Configuration file '{config_path}' must contain a JSON object.")

    required_keys = {"project_id", "project_path", "project_export_path"}
    missing_keys = required_keys - set(data)
    if missing_keys:
        raise ValueError(
            f"Configuration file '{config_path}' is missing required keys: "
            f"{', '.join(sorted(missing_keys))}."
        )

    unknown_keys = set(data) - required_keys - {"languages_code_rename", "languages_code_to_exclude"}
    if unknown_keys:
        raise ValueError(
            f"Configuration file '{config_path}' contains unsupported keys: "
            f"{', '.join(sorted(unknown_keys))}."
        )

    project_id = data.get("project_id")
    if type(project_id) is not int or project_id <= 0:
        raise ValueError(f"Configuration file '{config_path}' must contain a positive integer 'project_id'.")

    resolved_project_path = _load_path(data["project_path"], "project_path", config_path)
    resolved_export_path = _load_path(data["project_export_path"], "project_export_path", config_path)

    languages_code_rename = data.get("languages_code_rename", {})
    if not isinstance(languages_code_rename, dict) or not all(
        _is_language_code(source) and _is_language_code(target)
        for source, target in languages_code_rename.items()
    ):
        raise ValueError(
            f"Configuration file '{config_path}': 'languages_code_rename' must be an object "
            "mapping language codes to language codes."
        )

    languages_code_to_exclude = data.get("languages_code_to_exclude", [])
    if not isinstance(languages_code_to_exclude, list) or not all(
        _is_language_code(code) for code in languages_code_to_exclude
    ):
        raise ValueError(
            f"Configuration file '{config_path}': 'languages_code_to_exclude' must be a list of language codes."
        )

    return ProjectConfig(
        project_id=project_id,
        project_path=resolved_project_path,
        project_export_path=resolved_export_path,
        languages_code_rename=languages_code_rename,
        languages_code_to_exclude=languages_code_to_exclude,
    )


def _load_path(value: object, field_name: str, config_path: Path) -> Path:
    if not isinstance(value, str) or not value.strip() or "\0" in value:
        raise ValueError(f"Configuration file '{config_path}' must contain a non-empty string '{field_name}'.")
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = config_path.resolve().parent / path
    return path


def _is_language_code(value: object) -> bool:
    # Language rules are used as folder names, including when deleting excluded folders.
    return (
        isinstance(value, str)
        and re.fullmatch(r"[A-Za-z0-9]+(?:[-_][A-Za-z0-9]+)*", value) is not None
    )
