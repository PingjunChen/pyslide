# -*- coding: utf-8 -*-

import os, sys


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration

    config = Configuration('pyslide', parent_package, top_path)
    config.add_subpackage('contour')
    config.add_subpackage('patch')
    config.add_subpackage('pyramid')

    return config


if __name__ == "__main__":
    from numpy.distutils.core import setup

    config = configuration(top_path='').todict()
    setup(**config)
