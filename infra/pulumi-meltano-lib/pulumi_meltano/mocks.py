import json
from typing import Dict
import pulumi
from os import environ


class MyPulumiMocks(pulumi.runtime.Mocks):
    def new_resource(self, args: pulumi.runtime.MockResourceArgs):
        return [args.name + "_id", args.inputs]

    def call(self, args: pulumi.runtime.MockCallArgs):
        return {}


def mock_pulumi_settings(settings: Dict) -> None:
    pulumi_settings: Dict[str, str] = {}
    for k, v in settings.items():
        pulumi_settings[k] = v
    pulumi_settings_str = json.dumps(pulumi_settings)
    environ["PULUMI_CONFIG"] = pulumi_settings_str


def set_mocks(settings: Dict = None) -> None:
    if settings:
        mock_pulumi_settings(settings)

    pulumi.runtime.set_mocks(MyPulumiMocks())
