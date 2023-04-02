import numpy as np
from shapely import geometry

from typing import Tuple


__all__ = ["cnt_inside_wsi", "intersect_cnt_wsi", "cnt_inside_ratio"]


def construct_polygon_from_points(point_list: np.ndarray) -> geometry.Polygon:
    """Constructs a Shapely polygon object from a numpy array of points."""
    x, y = point_list[0], point_list[1]
    point_tuples = list(zip(y, x))  # Need to reverse order of x, y to match Shapely convention
    return geometry.Polygon(point_tuples)


def cnt_inside_wsi(cnt_arr: np.ndarray, wsi_h: int, wsi_w: int) -> bool:
    """Determine if a contour is fully inside a whole slide image or not.

    Parameters
    ----------
    cnt_arr : np.ndarray
        Contour with standard numpy 2d array format
    wsi_h : int
        Height of whole slide image
    wsi_w : int
        Width of whole slide image

    Returns
    -------
    in_flag : bool
        True if contour is fully inside whole slide image, else False
    """

    # Construct whole slide image polygon. In whole slide image, we need to avoid
    # contour on the maximum width and height line, thus subtract a small value.
    wsi_poly = geometry.box(0, 0, wsi_w - 0.001, wsi_h - 0.001)
    
    # Construct contour polygon
    cnt_poly = construct_polygon_from_points(cnt_arr)

    in_flag = wsi_poly.contains(cnt_poly)

    return in_flag


def intersect_cnt_wsi(cnt_arr: np.ndarray, wsi_h: int, wsi_w: int) -> np.ndarray:
    """Cut out the contour part inside the whole slide image.

    Parameters
    ----------
    cnt_arr : np.ndarray
        Contour with standard numpy 2d array format
    wsi_h : int
        Height of whole slide image
    wsi_w : int
        Width of whole slide image

    Returns
    -------
    inter_cnt : np.ndarray
        Contour intersected with whole slide image
    """

    if cnt_inside_wsi(cnt_arr, wsi_h, wsi_w):
        inter_cnt = cnt_arr.astype(np.uint32)
    else:
        # We remove the last line in both width and height of contour
        wsi_poly = geometry.box(0, 0, wsi_w - 1, wsi_h - 1)
        
        # Construct contour polygon
        cnt_poly = construct_polygon_from_points(cnt_arr)

        # Get the intersection part of two polygons
        inter_poly = wsi_poly.intersection(cnt_poly)

        x_coors, y_coors = inter_poly.exterior.coords.xy
        x_coors = x_coors[:-1].tolist()
        y_coors = y_coors[:-1].tolist()
        inter_cnt = np.zeros((2, len(x_coors)), dtype=np.uint32)
        for ind in np.arange(len(x_coors)):
            inter_cnt[0, ind] = y_coors[ind]
            inter_cnt[1, ind] = x_coors[ind]

    return inter_cnt


def cnt_inside_ratio(cnt_arr1: np.ndarray, cnt_arr2: np.ndarray) -> float:
    """Calculate the ratio between intersection part of cnt_arr1 and cnt_arr2 to cnt_arr1.

    Parameters
    ----------
    cnt_arr1 : np.ndarray
        Contour with standard numpy 2d array format
    cnt_arr2 : np.ndarray
        Contour with standard numpy 2d array format

    Returns
    -------
    ratio : float
        Intersection ratio of cnt_arr1
    """

    # Construct contour polygons
    cnt_poly1 = construct_polygon_from_points(cnt_arr1)
    cnt_poly2 = construct_polygon_from_points(cnt_arr2)

    # Check if the polygons intersect
    inter_flag = cnt_poly1.intersects(cnt_poly2)
    if not inter_flag:
        ratio = 0.0
    else:
        # Calculate the intersection area and ratio
        inter_poly = cnt_poly1.intersection(cnt_poly2)
        inter_area = inter_poly.area
        cnt1_area = cnt_poly1.area
        ratio = inter_area * 1.0 / cnt1_area

    return ratio
