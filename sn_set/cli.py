import click


@click.command()
def main():
    """
    snset is a python cli tool for retrieving the list of installed
    update sets in two ServiceNow instances, comparing them, and
    outputting the list of update sets that are installed in the target
    instance and not installed in the source instance, in the order
    that they must be installed in.

    Usage:
    snset --target {target instance} --source {sourceinstance}
    snset -t {target instance} -s {source instance}

    Will output to an excel file in the current directory, unless another
    is specified.
    """
    print("Entrypoint for the program")

    # TODO set up github actions CI integration
