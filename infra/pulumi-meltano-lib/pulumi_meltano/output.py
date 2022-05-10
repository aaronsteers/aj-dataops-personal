"""Module to export output to Pulumi."""

from typing import Any, Dict

import pulumi
import pulumi_kubernetes as k8s

EXPORT_KEYS = ["name", "url", "id", "arn", "kubeconfig"]


def _send_output(obj: Any, prefix: str = ""):
    if prefix:
        prefix = f"{prefix}-"

    for key in EXPORT_KEYS:
        export_as = f"{prefix}{key}".replace("--", "-")
        if hasattr(object, key):
            pulumi.export(name=export_as, value=obj[key])


def export_keys(*args, **kwargs: Dict[str, Any]) -> None:
    """Pass output to Pulumi.

    Each positional argument will have its keys sent to output with no prefix.
    Each keyword argument will have its keys prefixed with the provided
    dictionary key.

    The list of keys to pass for each object depends upon the object's class.

    As a general rule, the keys `name`, `url`, `id`, and `arn` are passed if they exist.

    Args:
        kwargs: A dictionary of name prefix to objects.
    """

    for arg in args:
        _send_output(arg)

    for prefix, obj in kwargs.items():
        _send_output(obj=obj, prefix=prefix)

        # Export the URL for the load balanced service.
        if isinstance(obj, k8s.core.v1.Service):
            pulumi.export(
                "url",
                obj.status.load_balancer.ingress[0].hostname,
            )
