# -*- coding: utf-8 -*-

import os, sys
import openslide


__all__ = ["create_pyramidal_img",
            "load_wsi_head",
            ]


def create_pyramidal_img(img_path, save_dir):
    """ Convert normal image to pyramidal image.

    Parameters
    -------
    img_path: str
        Whole slide image path (absolute path is needed)
    save_dir: str
        Location of the saved the generated pyramidal image with extension tiff,
        (absolute path is needed)

    Returns
    -------
    status: int
        The status of the pyramidal image generation (0 stands for success)

    Notes
    -------
    ImageMagick need to be preinstalled to use this function.
    >>> sudo apt-get install imagemagick

    Examples
    --------
    >>> img_path = os.path.join(PRJ_PATH, "test/data/Images/CropBreastSlide.tif")
    >>> save_dir = os.path.join(PRJ_PATH, "test/data/Slides")
    >>> status = pyramid.create_pyramidal_img(img_path, save_dir)
    >>> assert status == 0

    """

    convert_cmd = "convert " + img_path
    convert_option = " -compress jpeg -quality 90 -define tiff:tile-geometry=256x256 ptif:"
    img_name = os.path.basename(img_path)
    convert_dst = os.path.join(save_dir, os.path.splitext(img_name)[0] + ".tiff")
    status = os.system(convert_cmd + convert_option + convert_dst)

    return status


def load_wsi_head(wsi_img_path):
    """ Load the header meta data of whole slide pyramidal image.

    Parameters
    -------
    wsi_img_path: str
        The path to whole slide image

    Returns
    -------
    wsi_header: slide class
        Meta information of whole slide image

    """

    wsi_header = openslide.OpenSlide(wsi_img_path)

    return wsi_header
