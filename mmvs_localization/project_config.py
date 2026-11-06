from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectConfig:
    project_id: int
