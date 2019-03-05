# -*- coding: utf-8 -*-
import os, sys, pdb
from setuptools import setup, find_packages

import pyslide

PKG_NAME = "pyslide"
VERSION = pyslide.__version__
DESCRIPTION = "Python whole slide image analysis toolkit"
HOMEPAGE = "https://github.com/PingjunChen/pyslide"
LICENSE = "MIT"
AUTHOR_NAME = "Pingjun Chen"
AUTHOR_EMAIL = "chenpingjun@gmx.com"

REQS = ""
with open('requirements.txt') as f:
    REQS = f.read().splitlines()

CLASSIFIERS = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'Intended Audience :: Healthcare Industry',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Topic :: Scientific/Engineering',
]

args = dict(
    name=PKG_NAME,
    version=VERSION,
    description=DESCRIPTION,
    url=HOMEPAGE,
    license=LICENSE,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(),
    install_requires=REQS,
    classifiers= CLASSIFIERS,
)

setup(**args)
