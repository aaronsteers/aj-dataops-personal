"""Pulumi config."""

from typing import Optional

import pulumi

DEPLOYMENT_NAME_CONFIG = "deployment_name"


class Config(pulumi.Config):
    """Config."""

    def __init__(self) -> None:
        """Add validation to default constructor"""
        super().__init__()
        self._validate_config()

    def _validate_config(self) -> None:
        _ = self.require(DEPLOYMENT_NAME_CONFIG)
        # target_eks_cluster = config.require("target_eks_cluster")
        # branch_environment_map = config.require("project_config.branch_environment_map")
        # devtest_environment_name = config.require("project_config.devtest_environment_name")
        # ci_environment_name = config.require("project_config.ci_environment_name")
        # environment_config = config.require_object("project_config.environment_config")

    @property
    def deployment_name(self) -> str:
        """Gets the deployment name, used when naming resources.

        Returns:
            The deployment name.
        """
        return self.require(DEPLOYMENT_NAME_CONFIG)


config = Config()
