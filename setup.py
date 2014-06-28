#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from setuptools import setup, find_packages

import re
import os
import codecs


def read(*parts):
    path = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(path, encoding='utf-8') as fobj:
        return fobj.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

with open('requirements-dev.txt') as f:
    tests_require = f.read().splitlines()

setup(
    name='anthrobot',
    version=find_version("anthrobot", "__init__.py"),
    packages=find_packages(),
    test_suite='nose.collector',
    install_requires=install_requires,
    tests_require=tests_require,
)
