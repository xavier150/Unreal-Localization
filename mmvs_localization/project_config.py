from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class ProjectConfig:
    project_id: int
    project_path: Path
    project_export_path: Path
    languages_code_rename: dict[str, str] = field(default_factory=dict)
    languages_code_to_exclude: list[str] = field(default_factory=list)
