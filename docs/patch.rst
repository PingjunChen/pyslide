Patch
========

wsi_coor_splitting
--------
::

def wsi_coor_splitting(wsi_h, wsi_w, length, overlap_flag=True):
    """ Spltting whole slide image to starting coordinates.

    """

wsi_patch_splitting
--------
::

def wsi_patch_splitting(wsi_path, patch_dir, patch_size=299, save_size=299,
                        wsi_ext="tiff", save_ext="png",
                        pyramid_flag=True, overlap_flag=True, level=0):
    """ Spltting whole slide image to image patches.

    """

mean_patch_val
--------
::

def mean_patch_val(img):
    """ Mean pixel value of the patch.

    """

std_patch_val
--------
::

def std_patch_val(img):
    """ Standard deviation of pixel values in the patch.

    """

patch_bk_ratio
--------
::

def patch_bk_ratio(img, bk_thresh=0.80):
    """ Calculate the ratio of background in the image

    """
