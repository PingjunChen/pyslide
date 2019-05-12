# -*- coding: utf-8 -*-

import os, sys
import numpy as np


__all__ = ["create_pyramidal_img",
            "load_wsi_head",
            "load_wsi_level_img",
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
    wsi_head: slide metadata
        Meta information of whole slide image

    """

    import openslide
    wsi_head = openslide.OpenSlide(wsi_img_path)

    return wsi_head


def load_wsi_level_img(wsi_img_path, level=0):
    """ Load the image from specified level of the whole slide image.

    Parameters
    -------
    wsi_img_path: str
        The path to whole slide image
    level: int
        Loading slide image level

    Returns
    -------
    level_img: np.array
        Whole slide numpy image in given specified level

    """


    wsi_head = load_wsi_head(wsi_img_path)
    if level < 0 or level >= wsi_head.level_count:
        raise AssertionError("level {} not availabel in {}".format(
            level, os.path.basename(wsi_img_path)))
    wsi_img = wsi_head.read_region((0, 0), level, wsi_head.level_dimensions[level])
    wsi_img = np.asarray(wsi_img)[:,:,:3]

    return wsi_img
