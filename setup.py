#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
from setuptools import setup, find_packages

def locked_requirements(section):
    """Look through the 'Pipfile.lock' to fetch requirements by section."""
    with open('Pipfile.lock') as pip_file:
        pipfile_json = json.load(pip_file)

    if section not in pipfile_json:
        print("{0} section missing from Pipfile.lock".format(section))
        return []

    return [package + detail.get('version', "")
            for package, detail in pipfile_json[section].items()]


here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, "salesforce_timecard", "__init__.py"), "r") as f:
    exec(f.read(), about)


setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description="Check on {}".format(about["__url__"]),
    author=about["__author__"],
    author_email=about["__author_email__"],
    maintainer=about["__maintainer__"],
    maintainer_email=about["__maintainer_email__"],
    license=about["__license__"],
    url=about["__url__"],
    packages=["salesforce_timecard",],
    install_requires=locked_requirements("default"),
    entry_points={
        "console_scripts": [
            "timecard = salesforce_timecard.cli:cli"
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=about["__keywords__"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Environment :: Console",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ]
)
