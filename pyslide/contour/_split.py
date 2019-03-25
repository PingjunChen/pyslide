# -*- coding: utf-8 -*-

import numpy as np
from ._rela import cnt_inside_ratio

__all__ = ["contour_patch_splitting_no_overlap",
           "contour_patch_splitting_self_overlap",
           "contour_patch_splitting_half_overlap",]


def contour_patch_splitting_no_overlap(cnt_arr, wsi_h, wsi_w,
                                       patch_size=299, inside_ratio=0.75):
    """ Splitting contour into patches with no overlapping between patches.

    Parameters
    -------
    cnt_arr: np.array
        contour with standard numpy 2d array format
    wsi_h: int
        the height of whole slide image
    wsi_w: int
        the width of whole slide image
    patch_size: int
        size of patch
    inside_ratio: float
        the ratio of patch to be inside the contour

    Returns
    -------
    coors_arr: list
        list of starting coordinates of patches ([0]-h, [1]-w)

    """

    cnt_min_h, cnt_min_w = np.min(cnt_arr[0, :]), np.min(cnt_arr[1, :])
    cnt_max_h, cnt_max_w = np.max(cnt_arr[0, :]), np.max(cnt_arr[1, :])
    if cnt_min_h < 0 or cnt_min_w < 0 or cnt_max_h > wsi_h or cnt_max_w > wsi_w:
        return []

    # add border to top left
    start_h, start_w = None, None
    half_patch_size = int(np.floor(patch_size / 2.0))
    quarter_patch_size = int(np.floor(patch_size / 4.0))
    if cnt_min_h >= half_patch_size:
        start_h = cnt_min_h - half_patch_size
    elif cnt_min_h >= quarter_patch_size:
        start_h = cnt_min_h - quarter_patch_size
    else:
        start_h = cnt_min_h
    if cnt_min_w >= half_patch_size:
        start_w = cnt_min_w - half_patch_size
    elif cnt_min_w >= quarter_patch_size:
        start_w = cnt_min_w - quarter_patch_size
    else:
        start_w = cnt_min_w

    # make up the border to satisfy patch grids
    end_h = (1 + int(np.floor((cnt_max_h - start_h - 1.0) / patch_size))) * patch_size + start_h
    if end_h > wsi_h:
        end_h -= patch_size
    end_w = (1 + int(np.floor((cnt_max_w - start_w  - 1.0) / patch_size))) * patch_size + start_w
    if end_w > wsi_w:
        end_w -= patch_size

    coors_arr = []
    for cur_h in np.arange(start_h, end_h, patch_size):
        for cur_w in np.arange(start_w, end_w, patch_size):
            cur_patch_cnt = np.array([[cur_h, cur_h, cur_h+patch_size, cur_h+patch_size],
                                      [cur_w, cur_w+patch_size, cur_w+patch_size, cur_w]])
            # inside ratio should sastify conditions to be used
            if cnt_inside_ratio(cur_patch_cnt, cnt_arr) >= inside_ratio:
                coors_arr.append([cur_h, cur_w, patch_size, patch_size])

    return coors_arr


def contour_patch_splitting_self_overlap(cnt_arr, patch_size=299, inside_ratio=0.75):
    """ Splitting contour into patches with both start and end meeting,
    with overlapping among patches.

    Parameters
    -------
    cnt_arr: np.array
        contour with standard numpy 2d array format
    patch_size: int
        size of patch
    inside_ratio: float
        the ratio of patch to be inside the contour

    Returns
    -------
    coors_arr: list
        list of starting coordinates of patches ([0]-h, [1]-w)

    """

    cnt_min_h, cnt_min_w = np.min(cnt_arr[0, :]), np.min(cnt_arr[1, :])
    cnt_max_h, cnt_max_w = np.max(cnt_arr[0, :]), np.max(cnt_arr[1, :])

    cnt_h, cnt_w = cnt_max_h - cnt_min_h, cnt_max_w - cnt_min_w
    h_points = int(np.ceil(cnt_h * 1.0 / patch_size))
    w_points = int(np.ceil(cnt_w * 1.0 / patch_size))

    overlap_h_len = (h_points * patch_size - cnt_h) * 1.0 / (h_points - 1)
    extend_h_len = patch_size - overlap_h_len
    overlap_w_len = (w_points * patch_size - cnt_w) * 1.0 / (w_points - 1)
    extend_w_len = patch_size - overlap_w_len

    coors_arr = []
    for h_ind in np.arange(h_points):
        for w_ind in np.arange(w_points):
            cur_h = int(round(cnt_min_h + extend_h_len * h_ind))
            cur_w = int(round(cnt_min_w + extend_w_len * w_ind))
            cur_patch_cnt = np.array([[cur_h, cur_h, cur_h+patch_size, cur_h+patch_size],
                                      [cur_w, cur_w+patch_size, cur_w+patch_size, cur_w]])
            if cnt_inside_ratio(cur_patch_cnt, cnt_arr) >= inside_ratio:
                coors_arr.append([cur_h, cur_w, patch_size, patch_size])
    return coors_arr


def contour_patch_splitting_half_overlap(cnt_arr, wsi_h, wsi_w,
                                       patch_size=448, inside_ratio=0.75):
    """ Splitting patches with half overlap between patches.

    Parameters
    -------
    cnt_arr: np.array
        contour with standard numpy 2d array format
    wsi_h: int
        the height of whole slide image
    wsi_w: int
        the width of whole slide image
    patch_size: int
        size of patch
    inside_ratio: float
        the ratio of patch to be inside the contour

    Returns
    -------
    coors_arr: list
        list of starting coordinates of patches ([0]-h, [1]-w)

    """

    cnt_min_h, cnt_min_w = np.min(cnt_arr[0, :]), np.min(cnt_arr[1, :])
    cnt_max_h, cnt_max_w = np.max(cnt_arr[0, :]), np.max(cnt_arr[1, :])
    if cnt_min_h < 0 or cnt_min_w < 0 or cnt_max_h > wsi_h or cnt_max_w > wsi_w:
        return []

    # add border to top left
    start_h, start_w = None, None
    half_patch_size = int(np.floor(patch_size / 2.0))
    quarter_patch_size = int(np.floor(patch_size / 4.0))
    if cnt_min_h >= half_patch_size:
        start_h = cnt_min_h - half_patch_size
    elif cnt_min_h >= quarter_patch_size:
        start_h = cnt_min_h - quarter_patch_size
    else:
        start_h = cnt_min_h
    if cnt_min_w >= half_patch_size:
        start_w = cnt_min_w - half_patch_size
    elif cnt_min_w >= quarter_patch_size:
        start_w = cnt_min_w - quarter_patch_size
    else:
        start_w = cnt_min_w

    # make up the border to satisfy patch grids
    end_h = (1 + int(np.floor((cnt_max_h - start_h - 1.0) / half_patch_size))) * half_patch_size + start_h
    if end_h > wsi_h - patch_size:
        end_h -= patch_size
    end_w = (1 + int(np.floor((cnt_max_w - start_w  - 1.0) / half_patch_size))) * half_patch_size + start_w
    if end_w > wsi_w - patch_size:
        end_w -= patch_size

    coors_arr = []
    for cur_h in np.arange(start_h, end_h+half_patch_size, half_patch_size):
        for cur_w in np.arange(start_w, end_w+half_patch_size, half_patch_size):
            cur_patch_cnt = np.array([[cur_h, cur_h, cur_h+patch_size, cur_h+patch_size],
                                      [cur_w, cur_w+patch_size, cur_w+patch_size, cur_w]])
            # inside ratio should sastify conditions to be used
            if cnt_inside_ratio(cur_patch_cnt, cnt_arr) >= inside_ratio:
                coors_arr.append([cur_h, cur_w, patch_size, patch_size])

    return coors_arr
