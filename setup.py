from setuptools import find_packages, setup

dependecies = [
    "environs",
    "requests",
    "click",
    "pandas"
]
test_dependencies = [
    "pytest",
    "pytest-cov",
    "coverage",
    "flake8",
    "black",
    "isort"
]

setup(
    name="snset",
    packages=find_packages(exclude=["tests"]),
    version="0.1.0",
    description="CLI tool to retrieve and compare update sets from ServiceNow",
    author="Alex Biehl",
    license="BSD",
    install_requires=dependecies,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "snset = sn_set.cli:main"
        ]
    },
    tests_require=test_dependencies,
    test_suite="tests"
)