#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ttcal
"""

classifiers = """\
Development Status :: 3 - Alpha
Intended Audience :: Developers
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Topic :: Software Development :: Libraries
"""

import setuptools
from distutils.core import setup, Command


version = '0.5.0'


class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys,subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


setup(
    name='ttcal',
    version=version,
    requires=[],
    install_requires=[
        'Django',
        'South'
    ],
    description=__doc__.strip(),
    classifiers=[line for line in classifiers.split('\n') if line],
    long_description=open('README.rst').read(),
    cmdclass={'test': PyTest},
    # packages=setuptools.find_packages(exclude=['tests*']),
    packages=['ttcal'],
    zip_safe=False,
)
