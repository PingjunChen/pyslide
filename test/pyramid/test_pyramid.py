# -*- coding: utf-8 -*-

import os, sys
from os.path import dirname as opd
from os.path import abspath as opa
from os.path import join as opj

TEST_PATH = opa(opd(opd(__file__)))
PRJ_PATH = opd(TEST_PATH)
sys.path.insert(0, opj(PRJ_PATH, "pyslide"))

import pyramid

def test_create_pyramidal_img():
    img_path = os.path.join(PRJ_PATH, "data", "Images", "CropBreastSlide.tif")
    save_dir = os.path.join(PRJ_PATH, "data", "Slides")

    pyramid.create_pyramidal_img(img_path, save_dir)
    assert 1 == 1, "IO Testing is passed"