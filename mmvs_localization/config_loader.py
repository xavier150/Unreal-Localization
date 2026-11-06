import json
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

    unknown_keys = set(data) - {"project_id"}
    if unknown_keys:
        raise ValueError(
            f"Configuration file '{config_path}' contains unsupported keys: "
            f"{', '.join(sorted(unknown_keys))}."
        )

    project_id = data.get("project_id")
    if type(project_id) is not int or project_id <= 0:
        raise ValueError(f"Configuration file '{config_path}' must contain a positive integer 'project_id'.")

    return ProjectConfig(project_id=project_id)
