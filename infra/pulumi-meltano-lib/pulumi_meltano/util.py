"""Utility module."""


from typing import Dict

from pulumi_meltano.config import config


def name(
    base_name: str,
    *,
    deployment: str = None,
    max_len: int = 1000,
    lower: bool = False,
    delimiter: str = "-",
) -> str:
    result: str
    deployment = deployment or config.deployment_name
    if len(deployment) + len(base_name) + len(delimiter) <= max_len:
        result = f"{deployment}{delimiter}{base_name}"
    else:
        result = (
            f"{deployment[:4]}{deployment[-4:]}{delimiter}"
            f"{base_name[:4]}{base_name[-4:]}"
        )
        for candidate in [
            f"{deployment[:4]}{deployment[-4:]}{delimiter}{base_name}",
        ]:
            if len(candidate) <= max_len:
                result = candidate
        return result

    if lower:
        return result.lower()

    return result


def tags(deployment: str = None) -> Dict[str, str]:
    deployment = deployment or config.deployment_name
    return {"deployment": deployment}
