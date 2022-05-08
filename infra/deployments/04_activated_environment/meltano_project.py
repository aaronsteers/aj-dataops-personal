"""Project information and resources."""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict
import yaml


@dataclass
class MeltanoProject:
    def __init__(self, from_dict: Dict) -> None:
        for k, val in from_dict.items():
            self.__dict__[k] = val


def get_project(path: Path) -> MeltanoProject:
    contents = yaml.load(str(path), yaml.SafeLoader)
    return MeltanoProject(contents)
