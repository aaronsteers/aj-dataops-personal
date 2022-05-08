"""Project information and resources."""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict
import yaml


@dataclass
class MeltanoProjectDefinition:
    """Meltano project class."""

    def __init__(self, from_dict: Dict) -> None:
        for k, val in from_dict.items():
            self.__dict__[k] = val
            self.__setattr__(k, val)


def get_project(path: Path) -> MeltanoProjectDefinition:
    """Get project from `meltano.yml` path."""
    contents = yaml.load(str(path), yaml.SafeLoader)
    return MeltanoProjectDefinition(contents)


def new_hosted_project():
    pass
