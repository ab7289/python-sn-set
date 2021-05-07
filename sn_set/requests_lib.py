from typing import Dict, List, Optional

import requests

from .settings import Settings

# import re


def get_update_sets(instance_name: str) -> List[Dict[str, str]]:
    """
    Handles retrieving the list of Complete update sets
    from the specified instance name. Uses basic auth credentials
    as specified in settings

    Parameters:
    instance_name: str - The SN Instance Host

    Returns:
    list: List of update set dicts
    """
    if is_invalid_instance(instance_name):
        raise ValueError("Please enter a valid instance name")

    uri = f"https://{instance_name}.service-now.com/api/now/table/sys_update_set"
    params = {"sysparm_query": "active=true^state=complete", "sysparm_fields": "name"}
    return make_request(uri, path_params=params)


def get_install_order(instance_name: str, set_ids: List[str]) -> List[Dict[str, str]]:
    """
    Handles retrieving the install order for the specified list
    of update set sys_ids

    Parameters:
    instance_name: str - the SN Instance Host
    set_ids: list - array of update set sys_ids

    Returns:
    list: List of update sets in the order they should be installed
    """
    if is_invalid_instance(instance_name):
        raise ValueError("Please enter a valid instance name.")

    if not isinstance(set_ids, List):
        raise ValueError("set_ids must be a list")

    # id_regex = re.compile("[a-zA-Z0-9]{32}")
    # for sys_id in set_ids:
    #     if not id_regex.match(sys_id):
    #         raise ValueError("Each ID must be a valid sys_id")
    for name in set_ids:
        if not name:
            raise ValueError("IDs cannot be null or empty")

    fields = [
        "name",
        "state",
        "update_source",
        "description",
        "sys_created_on",
        "commit_date",
        "sys_updated_by",
        "sys_updated_on",
        "collisions",
    ]

    id_list = ",".join(set_ids)
    uri = f"https://{instance_name}.service-now.com/api/now/table/sys_remote_update_set"
    params = {
        "sysparm_query": (
            f"state=committed^nameIN{id_list}"
            f"^commit_dateISNOTEMPTY^ORDERBYinstall_date"
        ),
        "sysparm_fields": ",".join(fields),
    }
    return make_request(uri, path_params=params)


def make_request(uri: str, path_params: Dict[str, str] = None) -> Optional[Dict]:
    """
    Makes a request to the given uri

    Parameters:
    uri: str - The HTTP URI to gake the request against
    path_params: Dict - Dictionary of path params and their
        values to be added to the request
    """
    settings = Settings()
    if not settings.get_user() or not settings.get_password():
        raise ValueError("Username or Password is empty")

    r = requests.get(
        uri,
        params=path_params,
        auth=requests.auth.HTTPBasicAuth(settings.get_user(), settings.get_password()),
    )
    r.raise_for_status()

    return r.json().get("result")


def is_invalid_instance(instance_name: str) -> bool:
    """
    TODO later add a method to call out to see if it's a valid instance
    Checks whether the supplied instance is valid

    parameters:
    instance: str - the instance's unique name, i.e. nyudev

    returns bool - True if it is valid, false otherwise
    """
    return (
        instance_name != "nyu"
        and instance_name != "nyuqa"
        and instance_name != "nyutest"
        and instance_name != "nyudev"
        and instance_name != "nyutrain"
        and instance_name != "nyusandbox"
    )
