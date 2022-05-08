"""An AWS Python Pulumi program"""

from pulumi_meltano.service_fabric import new_service_fabric


def main():
    """Defines the infrastructure for this module."""
    new_service_fabric()


if __name__ == "__main__":
    main()
