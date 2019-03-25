# -*- coding: utf-8 -*-

import sys
import numpy as np
from os.path import dirname as opd
from os.path import abspath as opa

TEST_PATH = opa(opd(opd(__file__)))
PRJ_PATH = opd(TEST_PATH)
sys.path.insert(0, PRJ_PATH)

from pyslide import contour

def test_contour_patch_splitting_no_overlap():
    wsi_h, wsi_w = 5000, 5000
    cnt_arr = np.array([[160, 160, 4800, 4800],
                        [160, 4800, 4800, 160]])
    coors_arr = contour.contour_patch_splitting_no_overlap(cnt_arr, wsi_h, wsi_w,
                                                           patch_size=299, inside_ratio=0.75)
    if len(coors_arr) == 0:
        raise AssertionError


def test_contour_patch_splitting_self_overlap():
    cnt_arr = np.array([[160, 160, 4800, 4800],
                        [160, 4800, 4800, 160]])
    coors_arr = contour.contour_patch_splitting_self_overlap(cnt_arr, patch_size=299,
                                                           inside_ratio=0.75)
    if len(coors_arr) == 0:
        raise AssertionError


def test_contour_patch_splitting_half_overlap():
    wsi_h, wsi_w = 4752, 4752
    cnt_arr = np.array([[160, 160, 4751, 4751],
                        [160, 4751, 4751, 160]])
    coors_arr = contour.contour_patch_splitting_half_overlap(cnt_arr, wsi_h, wsi_w,
                                                             patch_size=448, inside_ratio=0.01)
    if len(coors_arr) == 0:
        raise AssertionError
