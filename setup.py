#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'salesforce_timecard', '__init__.py'), 'r') as f:
    exec(f.read(), about)

with open("requirements.txt") as requirements_file:
    requirements = [
        requirement for requirement in requirements_file.read().split("\n")
        if requirement != ""
    ]


setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description="Check on https://github.com/giuliocalzolari/salesforce-timecard",
    author=about['__author__'],
    author_email=about['__author_email__'],
    maintainer=about['__maintainer__'],
    maintainer_email=about['__maintainer_email__'],    
    license=about['__license__'],
    url=about['__url__'],
    entry_points="""
        [console_scripts]
        timecard=salesforce_timecard.cli:cli
    """,
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords=about['__keywords__'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Environment :: Console",
        "Programming Language :: Python :: 3.6",
    ]
)
