# This file is part of ubuntu-iso-download. See LICENSE for license infomation.
"""Setup.py file."""

import os
from setuptools import find_packages, setup


def read_readme():
    """Read and return text of README.md."""
    pwd = os.path.abspath(os.path.dirname(__name__))
    readme_file = os.path.join(pwd, "README.md")
    with open(readme_file, "r") as readme:
        readme_txt = readme.read()

    return readme_txt


def gather_deps():
    """Read requirements.txt and pre-process for setup.

    Returns:
         list of packages and dependency links.

    """
    default = open("requirements.txt", "r").read().splitlines()
    new_pkgs = []
    links = []
    for resource in default:
        if "git+https" in resource.strip():
            links.append(resource)
        else:
            new_pkgs.append(resource)

    return new_pkgs, links


PKGS, LINKS = gather_deps()

setup(
    name="ubuntu-iso-download",
    version="21.1",
    description="Download the latest Ubuntu ISOs.",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Joshua Powers",
    author_email="josh.powers@canonical.com",
    url="https://github.com/powersj/ubuntu-iso-download",
    download_url=("https://github.com/powersj/ubuntu-iso-download/tarball/master"),
    python_requires=">=3.6",
    install_requires=PKGS,
    dependency_links=LINKS,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
    keywords=["ubuntu", "download", "iso"],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": ["ubuntu-iso-download=ubuntu_iso_download.__main__:launch"]
    },
    zip_safe=True,
)
