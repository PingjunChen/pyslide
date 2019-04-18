# -*- coding: utf-8 -*-

import os, sys
from os.path import dirname as opd
from os.path import abspath as opa

from skimage import io

TEST_PATH = opa(opd(opd(__file__)))
PRJ_PATH = opd(TEST_PATH)
sys.path.insert(0, PRJ_PATH)

from pyslide import patch

def test_patch_bk_ratio():
    img_path = os.path.join(PRJ_PATH, "test/data/Images/3c32efd9.png")
    img = io.imread(img_path)

    bk_ratio = patch.patch_bk_ratio(img, bk_thresh=0.80)
    if bk_ratio > 1 or bk_ratio < 0:
        raise AssertionError("Ratio not in the range.")
