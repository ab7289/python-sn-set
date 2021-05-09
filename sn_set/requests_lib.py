from datetime import datetime
from typing import Dict, List, Optional

import requests
from requests.exceptions import HTTPError

from .settings import Settings

# import datetime


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
    params = {"sysparm_query": "state=complete", "sysparm_fields": "name"}
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
        if not name or not isinstance(name, str):
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
    # uri = f"https://{instance_name}.service-now.com/api/now/table/sys_remote_update_set" # noqa E501
    # result_sets = []
    # for name in set_ids:
    #     params = {
    #         "sysparm_query": f"state=committed^name={name}^commit_dateISNOTEMPTY^ORDERBYcommit_date", # noqa E501
    #         "sysparm_fields": ",".join(fields),
    #         "sysparm_display_value": "true"
    #     }
    #     result_sets.append(make_request(uri, path_params=params))

    # result_sets = [ elem[0] for elem in result_sets if len(elem) > 0]

    # return result_sets

    # TODO figure out a way to catch error 400 error and then split it into multiple requests # noqa E501
    # perhaps just send each request with like 25 update set names or something, will still have # noqa E501
    # to sort at the end

    id_list = ",".join(set_ids)
    uri = f"https://{instance_name}.service-now.com/api/now/table/sys_remote_update_set"
    params = {
        "sysparm_query": (
            f"state=committed^nameIN{id_list}"
            f"^commit_dateISNOTEMPTY^ORDERBYcommit_date"
        ),
        "sysparm_fields": ",".join(fields),
        "sysparm_display_value": "true",
    }
    try:
        return make_request(uri, path_params=params)
    except HTTPError as e:
        if e.response.status_code != 400:
            raise e
        else:
            # if we get a 400, it could be that the URL is too long, so we split it up into # noqa E501
            # multiple requests
            print(
                "get_install_order: Received 400, "
                "attempting to split into multiple calls"
            )
            results = []
            for name in set_ids:
                params = {
                    "sysparm_query": (
                        f"state=committed^name={name}"
                        f"^commit_dateISNOTEMPTY^ORDERBYcommit_date"
                    ),
                    "sysparm_fields": ",".join(fields),
                    "sysparm_display_value": "true",
                }
                results.append(make_request(uri, path_params=params))

            results = [elem[0] for elem in results if len(elem) > 0]
            return order_sets(results)


def order_sets(set_list: List[Dict[str, str]]) -> List[Dict[str, str]]:
    set_list.sort(
        key=lambda elem: datetime.strptime(elem.get("commit_date"), "%Y-%m-%d %H:%M:%S")
    )
    return set_list


def get_install_order_new(
    instance_name: str, set_ids: List[str]
) -> List[Dict[str, str]]:
    """
    Get the sets that are newly created since the last clone, i.e. don't have a record
    in the sys_remote_update_set table

    Parameters:
    instance_name: str - the name of the instance to retrieve the sets from
    set_ids: List[str] - the list of update set names to retrieve

    returns:
    list: list of update sets in the order they should be installed
    """
    if is_invalid_instance(instance_name):
        raise ValueError("Please enter a valid instance name.")

    if not isinstance(set_ids, List):
        raise ValueError("set_ids must be a list")

    for name in set_ids:
        if not name or not isinstance(name, str):
            raise ValueError("IDs cannot be null or empty")

    fields = [
        "name",
        "state",
        # "update_source",
        "description",
        "sys_created_on",
        # "commit_date",
        "sys_updated_by",
        "sys_updated_on",
        # "collisions",
    ]

    id_list = ",".join(set_ids)
    uri = f"https://{instance_name}.service-now.com/api/now/table/sys_update_set"
    params = {
        "sysparm_query": (
            f"nameIN{id_list}^installed_fromISEMPTY"
            "^install_date=NULL^ORDERBYsys_updated_on"
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
