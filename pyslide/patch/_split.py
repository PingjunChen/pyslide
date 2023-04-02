# -*- coding: utf-8 -*-

import os, sys
import numpy as np
import itertools, uuid
from skimage import io, transform
import openslide


__all__ = ["wsi_coor_splitting",
           "wsi_stride_splitting"]


def wsi_coor_splitting(wsi_h, wsi_w, length, overlap_flag=True):
    """ Splitting whole slide image into starting coordinates.

    Parameters
    ----------
    wsi_h : int
        Height of whole slide image.
    wsi_w : int
        Width of whole slide image.
    length : int
        Length of the patch image.
    overlap_flag : bool
        Patch with overlap or not.

    Returns
    -------
    coors_arr : list
        List of starting coordinates of patches ([0]-h, [1]-w).

    """

    coors_arr = []
    
    # Function to split patch with overlap
    def split_patch_overlap(ttl_len, sub_len):
        p_sets = []
        if ttl_len < sub_len:
            return p_sets
        if ttl_len == sub_len:
            p_sets.append(0)
            return p_sets

        p_num = int(np.ceil(ttl_len * 1.0 / sub_len))
        overlap_len = (p_num * sub_len - ttl_len) * 1.0 / (p_num - 1)
        extend_len = sub_len - overlap_len
        for ind in np.arange(p_num):
            p_sets.append(int(round(extend_len * ind)))
        return p_sets

    # Function to split patch without overlap
    def split_patch_no_overlap(ttl_len, sub_len):
        p_sets = []
        if ttl_len < sub_len:
            return p_sets
        if ttl_len == sub_len:
            p_sets.append(0)
            return p_sets

        p_num = int(np.floor(ttl_len * 1.0 / sub_len))
        p_sets = [ele*sub_len for ele in np.arange(p_num)]
        return p_sets

    if overlap_flag == True:
        h_sets = split_patch_overlap(wsi_h, length)
        w_sets = split_patch_overlap(wsi_w, length)
    else:
        h_sets = split_patch_no_overlap(wsi_h, length)
        w_sets = split_patch_no_overlap(wsi_w, length)

    # Combine points in both w and h direction
    if len(w_sets) > 0 and len(h_sets) > 0:
        coors_arr = [(h, w) for h in h_sets for w in w_sets]

    return coors_arr


def wsi_stride_splitting(wsi_h, wsi_w, patch_len, stride_len):
    """ Split whole slide image to patches with a certain stride.

    Parameters
    -------
    wsi_h: int
        height of whole slide image
    wsi_w: int
        width of whole slide image
    patch_len: int
        length of the patch image
    stride_len: int
        length of the stride

    Returns
    -------
    coors_arr: list
        list of starting coordinates of patches ([0]-h, [1]-w)

    Raises
    ------
    AssertionError
        If patch length is greater than total length.

    """

    coors_arr = []
    
    def stride_split(ttl_len, patch_len, stride_len):
        p_sets = []
        if patch_len > ttl_len:
            raise AssertionError("Patch length larger than total length.")
        elif patch_len == ttl_len:
            p_sets.append(0)
        else:
            stride_num = int(np.ceil((ttl_len - patch_len) * 1.0 / stride_len))
            for ind in range(stride_num+1):
                cur_pos = int(((ttl_len - patch_len) * 1.0 / stride_num) * ind)
                p_sets.append(cur_pos)
        return p_sets

    h_sets = stride_split(wsi_h, patch_len, stride_len)
    w_sets = stride_split(wsi_w, patch_len, stride_len)

    # combine points in both w and h direction
    if len(w_sets) > 0 and len(h_sets) > 0:
        coors_arr = list(itertools.product(h_sets, w_sets))

    return coors_arr
