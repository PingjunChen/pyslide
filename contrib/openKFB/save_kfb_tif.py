# -*- coding: utf-8 -*-

import os, sys
from pydaily import filesystem
from skimage.external.tifffile import imsave

sys.path.insert(0, '.')
from kfb_io.io_image import patch_read_slide

if __name__ == "__main__":
	input_root = str(sys.argv[1])   # kfb folder
	save_root = str(sys.argv[2])    # tif folder

    if not os.path.exists(save_root):
        os.makedirs(save_root)
    kfb_files = filesystem.find_ext_files(input_root, "kfb")

	for ind, this_kfb_path in enumerate(kfb_files):
        print("Processing {}/{}".format(ind+1, len(kfb_files)))
	    img_name = os.path.basename(this_kfb_path)
	    img_name_noext = os.path.splitext(img_name)[0]

	    this_raw_data = patch_read_slide(this_kfb_path, level=1)
	    save_path = os.path.join(save_root, img_name_noext+'.tif')
	    imsave(save_path, this_raw_data, compress=9, bigtiff=True)
