import click


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

    # TODO set up github actions CI integration
