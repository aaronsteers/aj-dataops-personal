"""Deployment for AJs Personal DataOps Project.

This deployment requires that the service plane is already deployed.
"""


from pulumi_meltano.projects import new_hosted_project


def main():
    """Defines the infrastructure for this module."""
    new_hosted_project()


if __name__ == "__main__":
    main()
