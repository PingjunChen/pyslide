# -*- coding: utf-8 -*-

import os, sys
import numpy as np
import matplotlib.pyplot as plt

from os.path import dirname as opd
from os.path import abspath as opa

TEST_PATH = opa(opd(opd(__file__)))
PRJ_PATH = opd(TEST_PATH)
sys.path.insert(0, PRJ_PATH)

from pyslide import pyramid


# def test_create_pyramidal_img():
#     save_dir = os.path.join(PRJ_PATH, "test/data/Slides")
#     status = pyramid.create_pyramidal_img(img_path, save_dir)
#     if not os.path.exists(os.path.join(save_dir, "CropBreastSlide.tiff")):
#         raise AssertionError("Pyramidal creation error")
#     if status != 0:
#         raise AssertionError("Pyramidal creation error")


def test_load_wsi_head():
    wsi_img_path = os.path.join(PRJ_PATH, "test/data/Slides/CropBreastSlide.tiff")
    with open(wsi_img_path, 'r') as f:
        wsi_header = pyramid.load_wsi_head(f)


    print("WSI level dimension info:")
    level_num = wsi_header.level_count
    for ind in np.arange(level_num):
        print("level {:2d} size: {}".format(ind, wsi_header.level_dimensions[ind]))


def test_load_wsi_level_img():
    wsi_img_path = os.path.join(PRJ_PATH, "test/data/Slides/CropBreastSlide.tiff")
    wsi_level_img = pyramid.load_wsi_level_img(wsi_img_path, level=3)
    plt.imshow(wsi_level_img)
    # plt.show()
