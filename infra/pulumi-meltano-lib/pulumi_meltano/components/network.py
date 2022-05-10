"""Network capabilities."""

from ipaddress import IPv4Network

from typing import List, Tuple
import pulumi_aws as aws
import pulumi_awsx as awsx
from pulumi_awsx import ec2 as ec2x

from pulumi_meltano.util import name, tags

# Helpful docs here:
# https://www.pulumi.com/docs/reference/pkg/nodejs/pulumi/awsx/ec2/


# def print_network_information(ipv4network: IPv4Network) -> None:
#     """Prints the network address, broadcast address and number
#     of addresses on the given IPv4 network.
#     """
#     print("Network IP:", ipv4network.network_address)
#     print("Broadcast address:", ipv4network.broadcast_address)
#     print("Number of hosts:", ipv4network.num_addresses)
# def new_cidr_strategy():
#     IPv4Network("192.168.0.0/255.255.255.0")


def new_network(
    num_public_subnets: int,
    num_private_subnets: int,
    num_isolated_subnets: int,
) -> awsx.ec2.Vpc:
    """Create new network.

    Args:
        deployment: The deployment name.
        public_subnets: The number of public subnets.
        private_subnets: The number of private subnets.
        addresses_per_subnet: The number of addresses needed per subnet. Defaults to 16.

    Returns:
        The VPC object.
    """
    subnets = (
        num_public_subnets
        * [
            ec2x.SubnetSpecArgs(
                type=ec2x.SubnetType.PUBLIC,
                name=name("public"),
                cidr_mask=6,
            )
        ]
        + num_private_subnets
        * [
            ec2x.SubnetSpecArgs(
                type=ec2x.SubnetType.PRIVATE,
                name=name("private"),
                cidr_mask=6,
            )
        ]
        + num_isolated_subnets
        * [
            ec2x.SubnetSpecArgs(
                type=ec2x.SubnetType.ISOLATED,
                name=name("isolated"),
                cidr_mask=6,
            )
        ]
    )
    nat_eip = aws.ec2.Eip(name("eip"), vpc=True)
    vpc = ec2x.Vpc(
        name("vpc"),
        ec2x.VpcArgs(
            number_of_availability_zones=3,
            nat_gateways=ec2x.NatGatewayConfigurationArgs(
                strategy=ec2x.NatGatewayStrategy.SINGLE,
                elastic_ip_allocation_ids=[nat_eip.allocation_id],
            ),
            # subnet_specs=subnets,
        ),
    )
    return vpc


def new_subnets(
    vpc: aws.ec2.Vpc, count: int = 1, private: bool = False
) -> List[aws.ec2.Subnet]:
    """Create new public subnet.

    Args:
        deployment: The deployment name.
        vpc: The VPC.

    Returns:
        A list of subnet objects.
    """
    subnets: List[aws.ec2.Subnet] = []
    obj_tags = tags(deployment)
    for n in range(1, count):
        if count == 1:
            subnet_name = name("subnet")
        else:
            subnet_name = name(f"subnet{n}")

        cidr_block = "10.0.1.0/24"
        subnets.append(
            aws.ec2.Subnet(
                subnet_name,
                vpc_id=vpc["main"]["id"],
                cidr_block=cidr_block,
                tags=obj_tags,
                map_public_ip_on_launch=not private,
            )
        )
    return subnets
