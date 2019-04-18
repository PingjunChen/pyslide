# -*- coding: utf-8 -*-

import numpy as np
from shapely import geometry

__all__ = ["cnt_inside_wsi",
           "intersect_cnt_wsi",
           "cnt_inside_ratio",
           ]


def cnt_inside_wsi(cnt_arr, wsi_h, wsi_w):
    """ Determine contour is fully inside whole slide image or not.

    Parameters
    -------
    cnt_arr: np.array
        contour with standard numpy 2d array format
    wsi_h: int
        height of whole slide image
    wsi_w: int
        width of whole slide image

    Returns
    -------
    in_flag: bool
        in_flag to be true if contour is fully inside whole slide image,
        else false

    """

    # construct whole slide image polygon, in whole slide image, we need to avoid
    # contour on the maximum width and height line, thus substract a small value
    wsi_poly = geometry.box(0, 0, wsi_w - 0.001, wsi_h - 0.001)
    # construct contour polygon
    point_list = []
    num_point = cnt_arr.shape[1]
    for ind in np.arange(num_point):
        # need to change h-w to w-h
        point_list.append((cnt_arr[1][ind], cnt_arr[0][ind]))
    cnt_poly = geometry.Polygon(point_list)

    in_flag = wsi_poly.contains(cnt_poly)

    return in_flag


def intersect_cnt_wsi(cnt_arr, wsi_h, wsi_w):
    """ Cutting out the contour part inside the whole slide image.

    Parameters
    -------
    cnt_arr: np.array
        contour with standard numpy 2d array format
    wsi_h: int
        height of whole slide image
    wsi_w: int
        width of whole slide image

    Returns
    -------
    inter_cnt: np.array
        contour intersected with whole slide image

    """

    if cnt_inside_wsi(cnt_arr, wsi_h, wsi_w) == True:
        inter_cnt = cnt_arr.astype(np.uint32)
    else:
        # we remove the last line in both width and height of contour
        wsi_poly = geometry.box(0, 0, wsi_w - 1, wsi_h - 1)

        # construct contour polygon
        point_list = []
        num_point = cnt_arr.shape[1]
        for ind in np.arange(num_point):
            # need to change h-w to w-h
            point_list.append((cnt_arr[1][ind], cnt_arr[0][ind]))
        cnt_poly = geometry.Polygon(point_list)

        # get the intersection part of two polygon
        inter_poly = wsi_poly.intersection(cnt_poly)

        x_coors, y_coors = inter_poly.exterior.coords.xy
        x_coors = x_coors[:-1].tolist()
        y_coors = y_coors[:-1].tolist()
        inter_cnt = np.zeros((2, len(x_coors)), dtype=np.uint32)
        for ind in np.arange(len(x_coors)):
            inter_cnt[0, ind] = y_coors[ind]
            inter_cnt[1, ind] = x_coors[ind]

    return inter_cnt


def cnt_inside_ratio(cnt_arr1, cnt_arr2):
    """ Calculate the ratio between intersection part of cnt_arr1 and cnt_arr2
    to cnt_arr1.

    Parameters
    -------
    cnt_arr1: np.array
        contour with standard numpy 2d array format
    cnt_arr2: np.array
        contour with standard numpy 2d array format

    Returns
    -------
    ratio: float
        intersection ratio of cnt_arr1

    """

    # construct contour polygon
    point_list1, point_list2 = [], []
    num_point1 = cnt_arr1.shape[1]
    num_point2 = cnt_arr2.shape[1]
    # need to change h-w to w-h
    for ind in np.arange(num_point1):
        point_list1.append((cnt_arr1[1][ind], cnt_arr1[0][ind]))
    for ind in np.arange(num_point2):
        point_list2.append((cnt_arr2[1][ind], cnt_arr2[0][ind]))
    cnt_poly1 = geometry.Polygon(point_list1)
    cnt_poly1 = cnt_poly1.convex_hull
    cnt_poly2 = geometry.Polygon(point_list2)
    cnt_poly2 = cnt_poly2.convex_hull

    inter_flag = cnt_poly1.intersects(cnt_poly2)
    if inter_flag == False:
        ratio = 0.0
    else:
        inter_poly = cnt_poly1.intersection(cnt_poly2)
        inter_area = inter_poly.area
        cnt1_area = cnt_poly1.area
        ratio = inter_area * 1.0 / cnt1_area

    return ratio
