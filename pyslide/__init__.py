# -*- coding: utf-8 -*-

import os, sys
import pkg_resources

__all__ = ["__version__", ]

__version__ = pkg_resources.require("pyslide")[0].version

from . import contour
from . import patch
from . import pyramid
