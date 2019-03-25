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

contour_patch_splitting_no_overlap
--------
::

def contour_patch_splitting_no_overlap(cnt_arr, wsi_h, wsi_w,
                                       patch_size=299, inside_ratio=0.75):
    """ Splitting contour into patches with no overlapping between patches.

    """

contour_patch_splitting_self_overlap
--------
::

def contour_patch_splitting_self_overlap(cnt_arr, patch_size=299, inside_ratio=0.75):
    """ Splitting contour into patches with both start and end meeting,
    with overlapping among patches.

    """
