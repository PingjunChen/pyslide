# -*- coding: utf-8 -*-

import os, sys, pdb
import pytest

from pyslide import DATA_DIR
from pyslide.io import to_pyramidal_tiff

def test_to_pyramidal_tiff():
    input_img_dir = os.path.join(DATA_DIR, "thyroid/thumb_slide")
    input_img_name = "1268669.png"

    to_pyramidal_tiff(input_img_dir, input_img_name, img_surfix=".png")

if __name__ == "__main__":
    # run_module_suite()
    test_to_pyramidal_tiff
