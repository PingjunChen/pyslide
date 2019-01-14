# -*- coding: utf-8 -*-

import os, sys
from shutil import copyfile
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tif_dir',       type=str, default='./data/tif',
                        help='directory of tif')
    parser.add_argument('--pyramidal_dir', type=str, default='./data/tiff',
                        help='directory for generated tiff')
    parser.add_argument('--bk_tif_dir',    type=str, default='./data/bk_tif',
                        help='directory for unprocessed tif')

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = get_args()

    import pdb; pdb.set_trace()
    tif_list = [ele for ele in os.listdir(args.tif_dir) if ele.endswith(".tif")]
    if len(tif_list) == 0:
        raise Exception("No tif files in designated directory")

    if not os.path.exists(args.pyramidal_dir):
        os.makedirs(args.pyramidal_dir)
    if not os.path.exists(args.bk_tif_dir):
        os.makedirs(args.bk_tif_dir)


    for ind, ele in enumerate(tif_list):
        print("Converting {}/{}  {}\r".format(ind+1, len(tif_list), ele))
        tif_path = os.path.join(args.tif_dir, ele)

        convert_cmd = "convert " + tif_path
        convert_option = " -compress jpeg -quality 90 -define tiff:tile-geometry=256x256 ptif:"
        convert_dst = os.path.join(args.pyramidal_dir, os.path.splitext(ele)[0] + ".tiff")

        status = os.system(convert_cmd + convert_option + convert_dst)
        if status != 0:
            copyfile(tif_path, os.path.join(args.bk_tif_dir, ele))
            print("cannot handle {}".format(ele))
