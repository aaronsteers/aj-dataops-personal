"""Pulumi definition tests."""

from pulumi_meltano.mocks import set_mocks

# It's important to import other modules _after_ the mocks are defined.
# pylint: disable=C0413
mock_settings = {"project:deployment_name": "mock"}
set_mocks(mock_settings)

from pulumi_meltano.meltano_environments import new_activated_environment  # noqa: E402
from pulumi_meltano.projects import MeltanoProjectDefinition  # noqa: E402
from pulumi_meltano.projects import new_hosted_project  # noqa: E402
from pulumi_meltano.service_fabric import new_service_fabric  # noqa: E402
from pulumi_meltano.site_instances import new_site_instance  # noqa: E402


def test_service_fabric():
    """Test service fabric definition."""
    new_service_fabric()


def test_site_instances():
    """Test service fabric definition."""
    new_site_instance()


def test_hosted_projects():
    """Test service fabric definition."""
    new_hosted_project()


def test_activated_environments():
    """Test service fabric definition."""
    project_def = MeltanoProjectDefinition({})
    environment_name = "mock"

    new_activated_environment(
        project_definition=project_def, environment_name=environment_name
    )
