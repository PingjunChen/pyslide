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

    if in_flag != True:
        raise AssertionError

def test_intersect_cnt_wsi():
    wsi_h, wsi_w = 4, 5
    cnt1 = np.array([[1, 0, 0, 1, 3.9, 3],
                     [0, 0, 1, 3, 5.1, 1]])

    inter_cnt = contour.intersect_cnt_wsi(cnt1, wsi_h, wsi_w)
    if np.max(inter_cnt[0, :]) >= wsi_h or np.max(inter_cnt[1, :]) >= wsi_w:
        raise AssertionError

def test_cnt_inside_ratio():
    cnt1 = np.array([[1, 1, 3, 3],
                     [1, 3, 3, 1]])
    cnt2 = np.array([[2, 2, 9, 9],
                     [2, 9, 9, 2]])

    inside_ratio = contour.cnt_inside_ratio(cnt1, cnt2)
    if inside_ratio < 0.0 or inside_ratio > 1.0:
        raise AssertionError
