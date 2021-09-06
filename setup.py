#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Utility to export google authenticator accounts.

    2021-∞ (c) blurryroots innovation qanat OÜ. All rights reserved.
    See license.md for details.

    https://think-biq.com
'''

import setuptools
import setuptools.dist
import os
from src.gabut.cli import get_version


def get_long_description():
    project_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(project_path, 'readme.md'), 'r') as fh:
        long_description = fh.read()
        return long_description


class BinaryDistribution(setuptools.dist.Distribution):
    '''
    Distribution which always forces a binary package with platform name.
    Thanks to https://stackoverflow.com/a/36886459/949561
    '''
    def has_ext_modules(foo):
        return True


setuptools.setup(
    python_requires='>=3.9',
    name="gabut",
    version=get_version(),
    description="Google authenticator backup tool.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    package_dir = {'gabut': 'src/gabut'},
    packages=['gabut'],
    include_package_data=False,
    package_data={},
    entry_points={
        'console_scripts': ['gabut = gabut.cli:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    author="blurryroots innovation qanat OÜ",
    author_email="sf@think-biq.com",
    url="https://gitlab.com/think-biq/gabut",
    distclass=BinaryDistribution
)
