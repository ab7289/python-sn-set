import time
from collections.abc import Iterable
from typing import Dict, List, Set

import click
import pandas as pd
import xlsxwriter

from .requests_lib import get_install_order, get_install_order_new, get_update_sets


@click.command()
@click.option("--timing", default=None, help="Turn on timing testing")
@click.option("--file-name", "-f", help="Specify the output file name if desired")
@click.option(
    "--target", "-t", required=True, help="The instance you want to compare to"
)
@click.option(
    "--source", "-s", required=True, help="The instance you want update sets from"
)
def main(source, target, file_name, timing):
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
    source_sets = list(map(lambda x: x.get("name"), get_update_sets(source)))
    print(f"Retrieved Source sets: {len(source_sets)}")

    print("\nBegin get Target sets")
    target_sets = list(map(lambda x: x.get("name"), get_update_sets(target)))
    print(f"Retrieved Target sets: {len(target_sets)}")

    print("\nCompute set difference")
    set_diff = get_set_diff(source_sets, target_sets, timing=timing)

    if timing:
        print("Success")
        exit(0)

    print(f"\nGet install order for {len(set_diff)} update sets")
    ordered_sets = get_install_order(source, set_diff)
    # print(f"ordered sets: {ordered_sets}")
    # get the elements that weren't in the list of retrieved update sets
    new_sets = get_set_diff(set_diff, list(map(lambda x: x.get("name"), ordered_sets)))

    if new_sets and len(new_sets) > 0:
        print("Getting newly created update sets")
        ordered_sets += get_install_order_new(source, new_sets)

    print("Output to excel")
    if to_excel(ordered_sets, file_name):
        print("Success!")
        exit(0)
    else:
        print("There was an error writing the spreadsheet")
        exit(-1)


def get_set_diff(left: List[str], right: List[str], timing=None) -> List[str]:
    """
    Finds all of the elements in the left input that are not present in the right
    returns the difference list. i.e. given two sets A and B, it returns the set A - B

    Parameters:
    left: List[str] - source list of elements
    right: List[str] - list of elements to compare source against

    returns: List[str] - left - right
    """
    if not left or not isinstance(left, Iterable):
        raise ValueError("Left must be Iterable")
    if not right or not isinstance(right, Iterable):
        raise ValueError("Right must be iterable")
    for item in left:
        if not item or not isinstance(item, str):
            raise ValueError("The lists must be composed of strings")
    for item in right:
        if not item or not isinstance(item, str):
            raise ValueError("The lists must be composed of strings")

    # TODO make this faster, maybe with pandas or with sets
    ctr = 0
    if timing:
        for i in range(10):
            print(f"iteration {i}")
            if timing == "pandas":
                ctr += set_diff_pandas(left, right, is_timing=True)
            elif timing == "set":
                ctr += set_diff_set(left, right, is_timing=True)
            else:
                ctr += set_diff_list(left, right, is_timing=True)
        print(
            f"Average set difference computation time for {timing} was {(ctr / 10):0.4f}"  # noqa E501
        )

    else:
        return set_diff_list(left, right)


def set_diff_list(left: List[str], right: List[str], is_timing=False) -> List[str]:
    tic = time.perf_counter()
    set_dif = [
        item
        for item in left
        if item.lower().strip() not in list(map(lambda x: x.lower().strip(), right))
    ]
    toc = time.perf_counter()
    print(f"Computed set difference with list in {toc - tic:0.4f} seconds")
    if is_timing:
        return toc - tic
    else:
        return set_dif


def set_diff_set(left: List[str], right: List[str], is_timing=False) -> Set[str]:
    tic = time.perf_counter()
    set_dif = {
        item
        for item in left
        if item.lower().strip() not in set(map(lambda x: x.lower().strip(), right))
    }
    toc = time.perf_counter()
    print(f"Computed set difference with set in {toc - tic:0.4f} seconds")
    if is_timing:
        return toc - tic
    else:
        return set_dif


def set_diff_pandas(left: List[str], right: List[str], is_timing=False) -> List[str]:
    tic = time.perf_counter()
    l_df = pd.DataFrame(list(map(lambda x: x.lower().strip(), left)))
    r_df = pd.DataFrame(list(map(lambda x: x.lower().strip(), right)))

    merged = l_df.merge(r_df, how="left", indicator=True).query("_merge == 'left_only'")

    diff_list = merged.values.tolist()
    toc = time.perf_counter()
    print(f"Computed set difference with pandas in {toc - tic:0.4f} seconds")
    if is_timing:
        return toc - tic
    else:
        return diff_list


def to_excel(update_sets: List[Dict[str, str]], file: str) -> bool:
    """
    Takes a list of dictionary items and outputs them to a excel.
    Takes and optional filename and path to output too

    Parameters:
    update_sets: List[Dict[str,str]] - The data to write to excel
    file: str - Optional the name of the file to output to. default is 'output'

    Returns: True if successful, false otherwise
    """
    if (
        not update_sets
        or not isinstance(update_sets, Iterable)
        or len(update_sets) == 0
    ):
        print("update set list was empty, exiting")
        return False
    headers = [key for key in update_sets[0].keys()]
    print(f"headers: {headers}")
    if not file:
        file = "output"
    with xlsxwriter.Workbook(f"{file}.xlsx") as workbook:
        # add worksheet
        worksheet = workbook.add_worksheet()

        # write headers
        for idx, header in enumerate(headers):
            worksheet.write(0, idx, header)

        # write data
        for idx, update_set in enumerate(update_sets, start=1):
            for kdix, (k, v) in enumerate(update_set.items()):
                if isinstance(v, dict):
                    v = v.get("display_value")
                worksheet.write(idx, headers.index(k), v)

        return True
