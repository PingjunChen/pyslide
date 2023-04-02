# -*- coding: utf-8 -*-

import sys
import numpy as np
from os.path import dirname as opd
from os.path import abspath as opa

TEST_PATH = opa(opd(opd(__file__)))
PRJ_PATH = opd(TEST_PATH)
sys.path.insert(0, PRJ_PATH)

from pyslide import contour

def test_cnt_inside_wsi():
    wsi_h, wsi_w = 4, 5
    cnt1 = np.array([[1, 0, 0, 1, 3.9, 3],
                     [0, 0, 1, 3, 4.9, 1]])
    in_flag = contour.cnt_inside_wsi(cnt1, wsi_h, wsi_w)

    assert in_flag == True, "The contour should be inside the WSI"


def test_intersect_cnt_wsi():
    wsi_h, wsi_w = 4, 5
    cnt1 = np.array([[1, 0, 0, 1, 3.9, 3],
                     [0, 0, 1, 3, 5.1, 1]])

    inter_cnt = contour.intersect_cnt_wsi(cnt1, wsi_h, wsi_w)
    assert np.max(inter_cnt[0, :]) < wsi_h, "The contour should not exceed the height of the WSI"
    assert np.max(inter_cnt[1, :]) < wsi_w, "The contour should not exceed the width of the WSI"


def test_cnt_inside_ratio():
    cnt1 = np.array([[1, 1, 3, 3],
                     [1, 3, 3, 1]])
    cnt2 = np.array([[2, 2, 9, 9],
                     [2, 9, 9, 2]])

    inside_ratio = contour.cnt_inside_ratio(cnt1, cnt2)
    assert 0.0 <= inside_ratio <= 1.0, "The inside ratio should be between 0 and 1"

