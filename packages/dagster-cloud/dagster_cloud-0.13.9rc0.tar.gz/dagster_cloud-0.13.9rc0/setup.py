from typing import Dict

from setuptools import find_packages, setup


def get_version() -> str:
    version: Dict[str, str] = {}
    with open("dagster_cloud/version.py") as fp:
        exec(fp.read(), version)  # pylint: disable=W0122

    return version["__version__"]


if __name__ == "__main__":
    ver = get_version()
    # dont pin dev installs to avoid pip dep resolver issues
    pin = "" if ver == "dev" else f"=={ver}"
    setup(
        name="dagster_cloud",
        version=ver,
        author_email="hello@elementl.com",
        packages=find_packages(exclude=["dagster_cloud_tests"]),
        include_package_data=True,
        install_requires=[f"dagster{pin}", "typer", "questionary"],
        extras_require={
            "tests": [
                "black",
                "docker",
                "httpretty",
                "isort",
                "kubernetes",
                "mypy==0.812",
                "pylint",
                "pytest",
                "typer",
                "questionary",
                "types-PyYAML",
                "types-requests",
                f"dagster_k8s{pin}",
                "ursula",
            ],
            "docker": ["docker", f"dagster_docker{pin}"],
            "kubernetes": ["kubernetes", f"dagster_k8s{pin}"],
            "ecs": [f"dagster_aws{pin}", "boto3"],
        },
        author="Elementl",
        license="Apache-2.0",
        classifiers=[
            "Programming Language :: Python :: 3.8",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
        ],
        entry_points={
            "console_scripts": [
                "dagster-cloud = dagster_cloud.cli.entrypoint:app",
            ]
        },
    )
