# -*- coding: utf-8 -*-


from pycontour.poly_transform import np_arr_to_poly, poly_to_np_arr

__all__ = ["contour_to_poly_valid",
           ]


def contour_to_poly_valid(cnt_arr):
    """ Convert contour to poly valid if not poly valid

    Parameters
    -------
    cnt_arr: np.array
        contour with standard numpy 2d array format

    Returns
    -------
    cnt_valid_arr: np.array
        contour with standard numpy 2d array format

    """

    poly = np_arr_to_poly(cnt_arr)
    if poly.is_valid == True:
        cnt_valid_arr = cnt_arr
    else:
        cnt_valid_arr = poly_to_np_arr(poly.convex_hull)

    return cnt_valid_arr
