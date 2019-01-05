import os, sys
from tifffile import imsave

sys.path.insert(0, '.')
from kfb_io.io_image import patch_read_slide

def walk_dir(data_dir, file_types):
    path_list = []
    for dirpath, dirnames, files in os.walk(data_dir):
        for f in files:
            for this_type in file_types:
                if f.endswith(this_type):
                    path_list.append( os.path.join(dirpath, f)  )
                    break
    return path_list


if __name__ == "__main__":
	input_root = ""
	save_root = ""

    if not os.path.exists(save_root):
        os.makedirs(save_root)
	kfb_files = walk_dir(input_root, ['.kfb'])


	for this_kfb_path in kfb_files:
	    img_name = os.path.basename(this_kfb_path)
	    img_name_noext = os.path.splitext(img_name)[0]

	    this_raw_data = patch_read_slide(this_kfb_path)
	    save_path = os.path.join(save_root, img_name_noext+'.tif')
	    imsave(save_path, this_raw_data, compress=8, bigtiff=True)
