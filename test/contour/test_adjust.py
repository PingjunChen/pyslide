# -*- coding: utf-8 -*-

import sys
import numpy as np
from os.path import dirname as opd
from os.path import abspath as opa

TEST_PATH = opa(opd(opd(__file__)))
PRJ_PATH = opd(TEST_PATH)
sys.path.insert(0, PRJ_PATH)

from pyslide import contour

def test_contour_to_poly_valid():
    cnt_arr1 = np.array([(0, 2, 2, 0), (0, 0, 2, 2)])
    valid_arr1 = contour.contour_to_poly_valid(cnt_arr1)
    if np.array_equal(cnt_arr1, valid_arr1) != True:
        raise AssertionError

    cnt_arr2 = np.array([(1, 3, 1, 3), (1, 3, 2, 2)])
    valid_arr2 = contour.contour_to_poly_valid(cnt_arr2)
    if np.array_equal(cnt_arr2, valid_arr2) != False:
        raise AssertionError
