# -*- coding: utf-8 -*-

import os, sys


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration, get_numpy_include_dirs

    config = Configuration('pyramid', parent_package, top_path)

    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(maintainer='Pingjun Chen',
          maintainer_email='chenpingjun@gmx.com',
          description='File format utilities of whole slide image',
          url='https://github.com/PingjunChen/pyslide',
          license='MIT',
          **(configuration(top_path='').todict())
          )
