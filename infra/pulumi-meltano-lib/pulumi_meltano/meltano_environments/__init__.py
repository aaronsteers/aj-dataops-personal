"""Deployment for AJs Personal DataOps Project.

This deployment requires that the service plane is already deployed.
"""

import pulumi_kubernetes as k8
from pulumi_awsx import ecr
from pulumi_meltano.util import name

# Project modules
from pulumi_meltano.projects import MeltanoProjectDefinition


def is_selected(
    environment_name: str, project_definition: MeltanoProjectDefinition
) -> bool:
    """Return true if this environment should be deployed.

    Args:
        environment_name: The environment name.

    Returns:
        True if selected, otherwise False.
    """
    # TODO: Add logic later to compare current branch from git and only deploy the
    # matching environment. For now, this will return `True` only for the 'beta'
    # environment.
    _ = project_definition
    return environment_name == "beta"


def new_activated_environments(project_definition: MeltanoProjectDefinition):
    """Defines _all_ activated environments."""
    for env_name, env_def in project_definition.environments:
        if not is_selected(env_name, project_definition):
            continue

        new_activated_environment(project_definition, env_def)


def new_activated_environment(
    project_definition: MeltanoProjectDefinition, environment_name: str
) -> k8.core.v1.Pod:
    """Defines a single activated environment.

    Args:
        project_definition: The project definition option.
        environment_name: The environment name.

    Returns:
        The environment K8 pod.
    """
    project_image = "meltano/meltano"  # TODO

    return k8.core.v1.Pod(
        "nginxPod",
        spec=k8.core.v1.PodSpecArgs(
            containers=[
                k8.core.v1.ContainerArgs(
                    name="nginx",
                    image=project_image,
                    ports=[
                        k8.core.v1.ContainerPortArgs(
                            container_port=80,
                        )
                    ],
                )
            ],
        ),
    )
