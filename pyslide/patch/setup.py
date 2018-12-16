# -*- coding: utf-8 -*-

import os, sys

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration, get_numpy_include_dirs

    config = Configuration('patch', parent_package, top_path)

    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(maintainer='Pingjun Chen',
          maintainer_email='chenpingjun@gmx.com',
          description='Patch utility in whole slide image',
          url='https://github.com/PingjunChen/pyslide',
          license='Apache',
          **(configuration(top_path='').todict())
          )
