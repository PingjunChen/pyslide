# -*- coding: utf-8 -*-

import os, sys
import openslide


__all__ = ["create_pyramidal_img",
            "load_wsi_head",
            ]

def create_pyramidal_img(img_path, save_dir):
    """ Convert normal image to pyramidal image.
    """

    convert_cmd = "convert " + img_path
    convert_option = " -compress jpeg -quality 90 -define tiff:tile-geometry=256x256 ptif:"
    img_name = os.path.basename(img_path)
    convert_dst = os.path.join(save_dir, os.path.splitext(img_name)[0] + ".tiff")
    os.system(convert_cmd + convert_option + convert_dst)


def load_wsi_head(wsi_img_path):
    """ Load the header meta data of whole slide pyramidal image
    """
    wsi_header = openslide.OpenSlide(wsi_img_path)

    return wsi_header
