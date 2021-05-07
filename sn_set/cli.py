from typing import List

import click

# from .requests_lib import get_update_sets


@click.command()
@click.option(
    "--target", "-t", required=True, help="The instance you want to compare to"
)
@click.option(
    "--source", "-s", required=True, help="The instance you want update sets from"
)
def main(source, target):
    """
    snset is a python cli tool for retrieving the list of installed
    update sets in two ServiceNow instances, comparing them, and
    outputting the list of update sets that are installed in the source
    instance and not installed in the target instance, in the order
    that they must be installed in.

    Usage:
    snset --target {target instance} --source {sourceinstance}
    snset -t {target instance} -s {source instance}

    Will output to an excel file in the current directory, unless another
    is specified.
    """
    print(f"Begin retrieving update sets from source: {source} and target: {target}")

    print("Begin get source sets")
    # source_sets = get_update_sets(source)
    print("Retrieved Source sets: {len(source_sets)}")
    print("Begin get Target sets")
    # target_sets = get_update_sets(target)
    print("Retrieved Target sets: {len(target_sets)}")

    # set_dif = get_set_diff(source_sets, target_sets)

    print("Get install order")
    # ordered_sets = get_install_order(source, set_dif)

    # TODO output

    exit(0)


def get_set_diff(left: List[str], right: List[str]) -> List[str]:
    """
    Finds all of the elements in the left input that are not present in the right
    returns the difference list. i.e. given two sets A and B, it returns the set A - B

    Parameters:
    left: List[str] - source list of elements
    right: List[str] - list of elements to compare source against

    returns: List[str] - left - right
    """
    if not left or not isinstance(left, list):
        raise ValueError("Left must be a list")
    if not right or not isinstance(right, list):
        raise ValueError("Right must be a list")
    for item in left:
        if not item or not isinstance(item, str):
            raise ValueError("The lists must be composed of strings")
    for item in right:
        if not item or not isinstance(item, str):
            raise ValueError("The lists must be composed of strings")

    return [item for item in left if item not in right]
