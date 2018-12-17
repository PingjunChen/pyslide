# -*- coding: utf-8 -*-

import os, sys

__all__ = ["PKG_DIR", "DATA_DIR", "__version__"]

PKG_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(os.path.dirname(PKG_DIR), 'data')

__version__ = '0.2.0'