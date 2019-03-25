Contour
========

cnt_inside_wsi
--------
::

def cnt_inside_wsi(cnt_arr, wsi_h, wsi_w):
    """ Determine contour is fully inside whole slide image or not.

    """

intersect_cnt_wsi
--------
::

def intersect_cnt_wsi(cnt_arr, wsi_h, wsi_w):
    """ Cutting out the contour part inside the whole slide image.

    """

cnt_inside_ratio
--------
::

def cnt_inside_ratio(cnt_arr1, cnt_arr2):
    """ Calculate the ratio between intersection part of cnt_arr1 and cnt_arr2
    to cnt_arr1.

    """
