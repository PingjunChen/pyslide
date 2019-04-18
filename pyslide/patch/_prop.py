# -*- coding: utf-8 -*-

import os, sys
import numpy as np
from skimage import color

__all__ = ['mean_patch_val',
           'patch_bk_ratio']


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


def patch_bk_ratio(img, bk_thresh=0.80):
    """ Calculate the ratio of background in the image

    Parameters
    -------
    img: np.array
        patch image
    bk_thresh: float
        background threshold value

    Returns
    -------
    bk_ratio: float
        the ratio of background in a patch

    """

    g_img = color.rgb2gray(img)
    bk_num = (g_img > bk_thresh).sum()
    pixel_num = g_img.shape[0] * g_img.shape[1]
    bk_ratio = bk_num * 1.0 / pixel_num

    return bk_ratio
