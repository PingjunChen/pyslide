# -*- coding: utf-8 -*-

import os, sys, pdb

BASE_PATH = os.path.abspath(os.path.dirname(__file__))


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration, get_numpy_include_dirs

    config = Configuration('io', parent_package, top_path)
    config.add_data_dir('tests')

    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(maintainer='Pingjun Chen',
          maintainer_email='chenpingjun@gmx.com',
          description='Whole slide image IO',
          url='https://github.com/PingjunChen/pyslide',
          license='Apache',
          **(configuration(top_path='').todict())
          )
