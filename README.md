# python-sn-set

[![Python package](https://github.com/ab7289/python-sn-set/actions/workflows/python-package.yml/badge.svg)](https://github.com/ab7289/python-sn-set/actions/workflows/python-package.yml)

snset is a python cli tool for retrieving the list of installed
update sets in two ServiceNow instances, comparing them, and
outputting the list of update sets that are installed in the source
instance and not installed in the target instance, in the order
that they must be installed in.

# To Install:

Checkout out the repository: `git clone  https://github.com/ab7289/python-sn-set`
Navigate into the project directory: `cd python-sn-set`
Install with pip: `pip install . -e`

# Usage:

snset --target {target instance} --source {sourceinstance}
snset -t {target instance} -s {source instance}
