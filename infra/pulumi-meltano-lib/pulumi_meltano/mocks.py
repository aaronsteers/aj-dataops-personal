"""Provides mock capabilities.

Usage:

`test_infra.py`
```
from pulumi_meltano.mocks import set_mocks

mock_settings = {"project:deployment_name": "mock"}
set_mocks(mock_settings)

# It's important to import other modules _after_ the mocks are defined.
import pulumi
...

def test_something():
    ...
```
"""

import json
from os import environ
from typing import Dict

import pulumi


class MyPulumiMocks(pulumi.runtime.Mocks):
    """From https://www.pulumi.com/docs/guides/testing/unit/"""

    def new_resource(self, args: pulumi.runtime.MockResourceArgs):
        return [args.name + "_id", args.inputs]

    def call(self, args: pulumi.runtime.MockCallArgs):
        return {}


def mock_pulumi_settings(settings: Dict) -> None:
    """Mock Pulumi settings.

    https://github.com/pulumi/pulumi/issues/4472#issuecomment-1015818376
    """
    pulumi_settings: Dict[str, str] = {}
    for k, v in settings.items():
        pulumi_settings[k] = v
    pulumi_settings_str = json.dumps(pulumi_settings)
    environ["PULUMI_CONFIG"] = pulumi_settings_str


def set_mocks(settings: Dict = None) -> None:
    """Set up Pulumi mocks.

    Args:
        settings: (Optional.) A dictionary of settings to their values.
    """
    if settings:
        mock_pulumi_settings(settings)

    pulumi.runtime.set_mocks(MyPulumiMocks())
