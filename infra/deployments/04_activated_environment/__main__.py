"""Deployment for AJs Personal DataOps Project.

This deployment requires that the service plane is already deployed.
"""

# Project modules
from pulumi_meltano.meltano_environments import new_activated_environment


def main():
    """Defines the infrastructure for this module."""
    new_activatad_environments()


if __name__ == "__main__":
    main()
