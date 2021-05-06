from typing import Dict, List, Optional

import requests

from .settings import Settings


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
    raise NotImplementedError()


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
    raise NotImplementedError()


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
