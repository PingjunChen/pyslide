# -*- coding: utf-8 -*-

import os, sys
from os.path import dirname as opd
from os.path import abspath as opa
from os.path import join as opj

TEST_PATH = opa(opd(opd(__file__)))
PRJ_PATH = opd(TEST_PATH)
sys.path.insert(0, PRJ_PATH)

from pyslide import patch

def test_wsi_patch_splitting():
    coors_arr = patch.wsi_patch_splitting(wsi_w=2048, wsi_h=1536, length=224)
