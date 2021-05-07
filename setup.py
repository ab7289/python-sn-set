from setuptools import find_packages, setup

dependecies = ["environs==9.3.2", "requests==2.25.1", "click==7.1.2"]
test_dependencies = [
    "pytest==6.2.4",
    "pytest-cov==2.11.1",
    "coverage==5.5",
    "flake8==3.9.1",
    "black==21.5b0",
    "isort==5.8.0",
    "requests-mock==1.9.2",
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
