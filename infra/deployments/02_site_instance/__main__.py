"""Deployment for AJs Personal DataOps Project.

This deployment requires that the service plane is already deployed.
"""

from pulumi_meltano.site_instances import new_site_instance


def main():
    """Defines the infrastructure for this module."""
    new_site_instance()


if __name__ == "__main__":
    main()
