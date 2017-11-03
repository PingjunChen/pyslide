# -*- coding: utf-8 -*-

import os, sys, pdb

__all__ = ['to_pyramidal_tiff', ]

def to_pyramidal_tiff(img_dir, img_name, img_surfix='.png'):
    img_filepath = os.path.join(img_dir, img_name + img_surfix)
    tiff_filepath = os.path.join(img_dir, img_name + '.tiff')
    convert_parameters = "-compress jpeg -quality 90 -define tiff:tile-geometry=256x256"
    convert_cmd = "convert '{}' {}  ptif:'{}'".format(img_filepath, convert_parameters, tiff_filepath)
    print('Start converting {}...'.format(name))
    os.system(convert_cmd)
    print('Finish converting...')
