"""EKS and Kubernetes Functions."""

from typing import Any, List
import pulumi
from pulumi_aws import eks
import pulumi_kubernetes as k8s
import pulumi_aws as aws
import json

from pulumi_meltano.util import name


def _new_eks_iam():
    eks_role = aws.iam.Role(
        name("eks-role"),
        assume_role_policy=(
            json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"Service": "eks.amazonaws.com"},
                            "Action": "sts:AssumeRole",
                        }
                    ],
                }
            )
        ),
    )
    eks_cluster_policy = aws.iam.RolePolicyAttachment(
        name("eks-iam-AmazonEKSClusterPolicy"),
        policy_arn="arn:aws:iam::aws:policy/AmazonEKSClusterPolicy",
        role=eks_role.name,
    )
    # Optionally, enable Security Groups for Pods
    # Reference: https://docs.aws.amazon.com/eks/latest/userguide/security-groups-for-pods.html
    eksvpc_resource_controller = aws.iam.RolePolicyAttachment(
        name("eks-iam-AmazonEKSVPCResourceController"),
        policy_arn="arn:aws:iam::aws:policy/AmazonEKSVPCResourceController",
        role=eks_role.name,
    )
    return eks_role, eks_cluster_policy, eksvpc_resource_controller


# Create an EKS cluster with the default configuration.


def new_eks_cluster(subnet_ids: List[str]) -> eks.Cluster:
    vpc_config_args = eks.ClusterVpcConfigArgs(subnet_ids=subnet_ids)
    eks_role, _, _ = _new_eks_iam()
    return eks.Cluster(
        name("eks"), role_arn=eks_role.arn, vpc_config=vpc_config_args
    )


def new_eks_deployment(eks_cluster: Any, app_name: str, image: str):
    app_name = "my-app"
    app_labels = {"app": app_name}
    image = image or "nginx"
    eks_deployment = k8s.apps.v1.Deployment(
        f"{app_name}-dep",
        spec=k8s.apps.v1.DeploymentSpecArgs(
            selector=k8s.meta.v1.LabelSelectorArgs(match_labels=app_labels),
            replicas=2,
            template=k8s.core.v1.PodTemplateSpecArgs(
                metadata=k8s.meta.v1.ObjectMetaArgs(labels=app_labels),
                spec=k8s.core.v1.PodSpecArgs(
                    containers=[k8s.core.v1.ContainerArgs(name=app_name, image=image)]
                ),
            ),
        ),
        opts=pulumi.ResourceOptions(provider=eks_cluster.provider),
    )
    eks_service = k8s.core.v1.Service(
        f"{app_name}-svc",
        spec=k8s.core.v1.ServiceSpecArgs(
            type="LoadBalancer",
            selector=app_labels,
            ports=[k8s.core.v1.ServicePortArgs(port=80)],
        ),
        opts=pulumi.ResourceOptions(provider=eks_cluster.provider),
    )
    return eks_deployment, eks_service
