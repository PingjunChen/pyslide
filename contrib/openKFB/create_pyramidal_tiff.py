# -*- coding: utf-8 -*-

import os, sys
from shutil import copyfile


if __name__ == "__main__":
    tif_dir       = str(sys.argv[1])  # tif folder
    pyramidal_dir = str(sys.argv[2])  # tiff folder
    bk_tif_dir    = str(sys.argv[3])  # tif back folder

    if not os.path.exists(pyramidal_dir):
        os.makedirs(pyramidal_dir)

    tif_list = [ele for ele in os.listdir(tif_dir) if ele.endswith(".tif")]
    for ind, ele in enumerate(tif_list):
        print("Converting {}/{}  {}".format(ind+1, len(tif_list), ele))
        tif_path = os.path.join(tif_dir, ele)

        convert_cmd = "convert " + tif_path
        convert_option = " -compress jpeg -quality 90 -define tiff:tile-geometry=256x256 ptif:"
        convert_dst = os.path.join(pyramidal_dir, os.path.splitext(ele)[0] + ".tiff")

        status = os.system(convert_cmd + convert_option + convert_dst)
        if status != 0:
            copyfile(tif_path, os.path.join(bk_tif_dir, ele))
            print("cannot handle {}".format(ele))
