"""Containers module."""

from typing import Optional, Tuple
import pulumi
import pulumi_aws as aws
import pulumi_awsx as awsx

from pulumi_aws.imagebuilder.image import Image
from pulumi_aws.ecr.repository import Repository

from pulumi_meltano.util import name


def new_hosted_container_image(
    dockerfile_dir: str = "/Users/aj/Source/aj-dataops-personal",
) -> Tuple[Repository, Image]:
    """Builds the docker image and publishes to a new ECR` repo.

    Args:
        deployment: The deployment name.
        dockerfile_dir: Path to a directory containing a Dockerfile.

    Returns:
        Tuple with Repository and Image.
    """
    ecr_repo = awsx.ecr.Repository(name("ecr-repo"))
    pulumi.export("ecr_repo_name", ecr_repo.name)
    pulumi.export("ecr_repo_url", ecr_repo.url)

    remote_image = awsx.ecr.Image(
        "image", repository_url=ecr_repo.url, path=dockerfile_dir
    )
    pulumi.export("ecr_image_url", remote_image.image_uri)
    return ecr_repo, remote_image


def new_ecs(
    container_image, as_service: bool = False
) -> Tuple[awsx.ecs.FargateService, awsx.ecs.FargateServiceTaskDefinitionArgs]:
    """Creates an ECS cluster and optionally an always-on ECS service.

    Args:
        deployment: The deployment name.
        container_image: The Pulumi image object.
        as_service: True to setup an always-on service.

    Returns:
        Tuple with: Service, TaskDefinitionArgs, LoadBalancer.
    """
    ecs_cluster = aws.ecs.Cluster(name("default-cluster"))
    alb = awsx.lb.ApplicationLoadBalancer(name("nginx-lb", max_len=32 - 8))
    ecs_task = awsx.ecs.FargateServiceTaskDefinitionArgs(
        containers={
            "nginx": awsx.ecs.TaskDefinitionContainerDefinitionArgs(
                image=container_image.image_uri,
                memory=128,
                port_mappings=[
                    awsx.ecs.TaskDefinitionPortMappingArgs(
                        container_port=80,
                        target_group=alb.default_target_group,
                    )
                ],
            )
        }
    )
    ecs_service: Optional[awsx.ecs.FargateService] = None
    if as_service:
        ecs_service = awsx.ecs.FargateService(
            name("service"),
            cluster=ecs_cluster.arn,
            task_definition_args=ecs_task,
        )
    return ecs_service, ecs_task, alb
