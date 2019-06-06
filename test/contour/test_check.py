# -*- coding: utf-8 -*-

import sys
import numpy as np
from os.path import dirname as opd
from os.path import abspath as opa

TEST_PATH = opa(opd(opd(__file__)))
PRJ_PATH = opd(TEST_PATH)
sys.path.insert(0, PRJ_PATH)

from pyslide import contour


def test_contour_valid():
    cnt_arr1 = np.array([(0, 2, 2, 0), (0, 0, 2, 2)])
    if contour.contour_valid(cnt_arr1) != True:
        raise AssertionError

    cnt_arr2 = np.array([(1, 3, 1, 3), (1, 3, 2, 2)])
    if contour.contour_valid(cnt_arr2) != False:
        raise AssertionError
