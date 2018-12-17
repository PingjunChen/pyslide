# -*- coding: utf-8 -*-

import os, sys


__all__ = ["create_pyramidal_img",
            ]

def create_pyramidal_img(img_path, save_dir):
    """Convert normal image to pyramidal image.
    """

    convert_cmd = "convert " + img_path
    convert_option = " -compress jpeg -quality 90 -define tiff:tile-geometry=256x256 ptif:"
    img_name = os.path.basename(img_path)
    convert_dst = os.path.join(save_dir, os.path.splitext(img_name)[0] + ".tiff")
    os.system(convert_cmd + convert_option + convert_dst)


def read_pyramidal_img(wsi_img_path):
    pass
