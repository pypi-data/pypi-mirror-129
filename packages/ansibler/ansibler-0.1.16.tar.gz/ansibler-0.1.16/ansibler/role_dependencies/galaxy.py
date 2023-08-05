from typing import Any, Dict
from ansibler.utils.subprocesses import get_subprocess_output
from ansibler.exceptions.ansibler import RoleMetadataError


def get_from_ansible_galaxy(role: str) -> Dict[str, Any]:
    """
    Gets role metadata from ansible-galaxy.

    Args:
        role (str): role in the form {{role_namespace}}.{{role_name}}

    Raises:
        RoleMetadataError: raised when role not found

    Returns:
        Dict[str, Any]: role metadata
    """
    # Run ansible-galaxy info {{ role }}
    out = get_subprocess_output(["ansible-galaxy", "info", role], "description")

    # Search for description, raise error if role not found
    description = None
    if "description" in out:
        description = out.replace("description:", "").strip()

    if not description:
        print(f"Role {role} not found. Description will be 'Unavailable'.")
        description = "Unavailable"

    # Extract data
    role_data = role.split(".")
    return {
        "namespace": role_data[0],
        "role_name": role_data[1],
        "description": description,
        "repository": None,
        "repository_status": None
    }
