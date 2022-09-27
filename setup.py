#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ttcal - calendar operations
===========================
"""

classifiers = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
Programming Language :: Python
Programming Language :: Python :: 3
Topic :: Software Development :: Libraries
"""

import sys, os
import setuptools

version = '2.0.1'

DIRNAME = os.path.dirname(__file__)
description = open(os.path.join(DIRNAME, 'README.rst'), 'r').read()


setuptools.setup(
    name='ttcal',
    version=version,
    url='https://github.com/datakortet/ttcal',
    author='Bjorn Pettersen',
    author_email='bp@datakortet.no',
    requires=[],
    install_requires=[],
    # description=__doc__.strip(),
    long_description=description,
    classifiers=[line for line in classifiers.split('\n') if line],
    packages=setuptools.find_packages(exclude=['tests']),
    zip_safe=False,
)
