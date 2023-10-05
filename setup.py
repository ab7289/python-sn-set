from setuptools import find_packages, setup

dependecies = [
    "environs==9.3.2",
    "requests==2.31.0",
    "click==8.1.7",
    "xlsxwriter==3.1.6",
]
test_dependencies = [
    "pytest==7.4.2",
    "pytest-cov==4.1.0",
    "coverage==7.3.2",
    "flake8==6.1.0",
    "black==23.9.1",
    "isort==5.12.0",
    "requests-mock==1.11.0",
    "coveralls==7.3.2",
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
    entry_points={"console_scripts": ["snset = sn_set.cli:main"]},
    tests_require=test_dependencies,
    test_suite="tests",
)
