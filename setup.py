from setuptools import find_packages, setup

dependecies = [
    "environs==15.0.1",
    "requests==2.33.1",
    "click==8.3.3",
    "xlsxwriter==3.2.9",
]
test_dependencies = [
    "pytest==9.0.3",
    "pytest-cov==7.1.0",
    "coverage==7.13.5",
    "flake8==7.3.0",
    "black==26.3.1",
    "isort==8.0.1",
    "requests-mock==1.12.1",
    "coverage==7.13.5",
]

setup(
    name="snset",
    packages=find_packages(exclude=["tests"]),
    version="0.2.0",
    description="CLI tool to retrieve and compare update sets from ServiceNow",
    author="Alex Biehl",
    license="BSD",
    install_requires=dependecies,
    include_package_data=True,
    entry_points={"console_scripts": ["snset = sn_set.cli:main"]},
    tests_require=test_dependencies,
    test_suite="tests",
)
