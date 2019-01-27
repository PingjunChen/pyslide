# -*- coding: utf-8 -*-

import os, sys
import numpy as np


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
