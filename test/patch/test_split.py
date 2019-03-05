# -*- coding: utf-8 -*-

import sys
from os.path import dirname as opd
from os.path import abspath as opa

TEST_PATH = opa(opd(opd(__file__)))
PRJ_PATH = opd(TEST_PATH)
sys.path.insert(0, PRJ_PATH)

from pyslide import patch


def test_wsi_coor_splitting():
    coors_arr = patch.wsi_coor_splitting(wsi_h=1536, wsi_w=2048, length=224, overlap_flag=True)
