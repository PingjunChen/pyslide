# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
from skimage import color

__all__ = ["mean_patch_val",
           "std_patch_val",
           "patch_bk_ratio"]


def mean_patch_val(img):
    """Calculate the mean pixel value of the patch.

    Parameters
    ----------
    img : np.ndarray
        Patch image.

    Returns
    -------
    float
        Mean pixel value of the patch.
    """
    return img.mean()


def std_patch_val(img):
    """Calculate the standard deviation of pixel values in the patch.

    Parameters
    ----------
    img : np.ndarray
        Patch image.

    Returns
    -------
    float
        Standard deviation of pixel values in the patch.
    """
    return img.std()


def patch_bk_ratio(img, bk_thresh=0.80):
    """Calculate the ratio of background in the image.

    Parameters
    ----------
    img : np.ndarray
        Patch image.
    bk_thresh : float, optional
        Background threshold value, by default 0.80.

    Returns
    -------
    float
        Ratio of background in the patch.
    """
    g_img = color.rgb2gray(img)
    bk_pixel_num = np.sum(g_img > bk_thresh)
    pixel_num = g_img.size
    background_ratio = bk_pixel_num / pixel_num
    return background_ratio
