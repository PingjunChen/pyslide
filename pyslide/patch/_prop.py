# -*- coding: utf-8 -*-

import os, sys
import numpy as np
from skimage import color

__all__ = ['mean_patch_val', ]


def mean_patch_val(img):
    """ Mean pixel value of the patch.

    Parameters
    -------
    img: np.array
        Patch image

    Returns
    -------
    mean_val: float
        Mean pixel value of the patch

    """

    mean_val = np.mean(img)

    return mean_val


def std_patch_val(img):
    """ Standard deviation of pixel values in the patch.

    Parameters
    -------
    img: np.array
        Patch image

    Returns
    -------
    std_val: float
        Standard deviation of pixel values in the patch

    """

    std_val = np.std(img)

    return std_val


def patch_bg_ratio(img, bg_thresh=0.72):
    """ Calculate the ratio of background in the image

    Parameters
    -------
    img: np.array
        patch image
    bg_thresh: float
        background threshold value

    Returns
    -------
    bg_ratio: float
        the ratio of background in a patch

    """

    g_img = color.rgb2gray(img)
    bg_num = (g_img > bg_thresh).sum()
    pixel_num = g_img.shape[0] * g_img.shape[1]
    bg_ratio = bg_num * 1.0 / pixel_num

    return bg_ratio
