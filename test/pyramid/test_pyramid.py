# -*- coding: utf-8 -*-

import os, sys
import numpy as np
from os.path import dirname as opd
from os.path import abspath as opa
from os.path import join as opj

TEST_PATH = opa(opd(opd(__file__)))
PRJ_PATH = opd(TEST_PATH)
sys.path.insert(0, PRJ_PATH)

from pyslide import pyramid

def test_create_pyramidal_img():
    img_path = os.path.join(PRJ_PATH, "test/data/Images/CropBreastSlide.tif")
    save_dir = os.path.join(PRJ_PATH, "test/data/Slides")
    pyramid.create_pyramidal_img(img_path, save_dir)
    assert os.path.exists(os.path.join(save_dir, "CropBreastSlide.tiff"))

def test_load_wsi_head():
    wsi_img_path = os.path.join(PRJ_PATH, "test/data/Slides/CropBreastSlide.tiff")
    wsi_header = pyramid.load_wsi_head(wsi_img_path)

    print("WSI level dimension info:")
    level_num = wsi_header.level_count
    for ind in np.arange(level_num):
        print("level {:2d} size: {}".format(ind, wsi_header.level_dimensions[ind]))
