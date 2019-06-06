# -*- coding: utf-8 -*-

from pycontour.poly_transform import np_arr_to_poly


__all__ = ["contour_valid",
           ]


def contour_valid(cnt_arr):
    """ Check contour is valid or not.

    Parameters
    -------
    cnt_arr: np.array
        contour with standard numpy 2d array format

    Returns
    -------
    valid: boolean
        True if valid, else False

    """

    poly = np_arr_to_poly(cnt_arr)
    valid = True if poly.is_valid else False

    return valid
