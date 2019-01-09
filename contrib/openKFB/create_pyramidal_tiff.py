# -*- coding: utf-8 -*-

import os, sys

if __name__ == "__main__":
    tif_dir = str(sys.argv[1])      # tif folder
    tiff_dir = str(sys.argv[2])     # tiff folder

    if not os.path.exists(pyramidal_dir):
        os.makedirs(pyramidal_dir)
    tif_list = [ele for ele in os.listdir(tif_dir) if ele.endswith(".tif")]
    for ind, ele in enumerate(tif_list):
        print("Converting {}/{}  {}".format(ind+1, len(tif_list), ele))
        tif_path = os.path.join(tif_dir, ele)
        convert_cmd = "convert " + tif_path
        convert_option = " -compress jpeg -quality 90 -define tiff:tile-geometry=256x256 ptif:"
        convert_dst = os.path.join(pyramidal_dir, os.path.splitext(ele)[0] + ".tiff")
        conversion_str = convert_cmd + convert_option + convert_dst
        os.system(conversion_str)
