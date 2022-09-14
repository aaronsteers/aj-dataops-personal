"""Service Fabric Module"""

from typing import Any, List

import pulumi_meltano
from pulumi_meltano.components import containers
from pulumi_meltano.output import export_keys


def new_service_fabric():
    """Defines the infrastructure for this module."""
    # Create an AWS resource (S3 Bucket)
    created: List[Any] = []

    ecr_container, ecr_image = containers.new_hosted_container_image()
    created.extend(
        (
            [ecr_container, ecr_image],
            list(containers.new_ecs(container_image=ecr_image)),
        )
    )

    vpc = pulumi_meltano.components.network.new_network(
        num_public_subnets=2,
        num_private_subnets=2,
        num_isolated_subnets=2,
    )

    # Deploy a small canary service (NGINX), to test that the cluster is working.
    eks_cluster = pulumi_meltano.components.eks.new_eks_cluster(
        vpc.public_subnet_ids[:2]
    )


    created += [vpc, eks_cluster]

    export_keys(**{type(obj).__name__: obj for obj in created})
