# -*- coding: utf-8 -*-

import os, sys
import numpy as np
import itertools, uuid
from skimage import io, transform
import openslide


__all__ = ['wsi_coor_splitting',
           'wsi_patch_splitting']


def wsi_coor_splitting(wsi_h, wsi_w, length, overlap_flag=True):
    ''' Spltting whole slide image to starting coordinates.

    Parameters
    -------
    wsi_h: int
        height of whole slide image
    wsi_w: int
        width of whole slide image
    length: int
        length of the patch image
    overlap_flag: boolean
        patch with overlap or not

    Returns
    -------
    coors_arr: list
        list of starting coordinates of patches ([0]-h, [1]-w)

    '''

    coors_arr = []
    # splitting in both w and h direction with overlap
    def split_patch_overlap(ttl_len, sub_len):
        p_sets = []
        if ttl_len < sub_len:
            return p_sets
        if ttl_len == sub_len:
            p_sets.append(0)
            return p_sets

        p_num = int(np.ceil(ttl_len * 1.0 / sub_len))
        overlap_len = (p_num * sub_len - ttl_len) * 1.0 / (p_num - 1)
        extend_len = sub_len - overlap_len
        for ind in np.arange(p_num):
            p_sets.append(int(round(extend_len * ind)))
        return p_sets

    # splitting in both w and h direction with overlap
    def split_patch_no_overlap(ttl_len, sub_len):
        p_sets = []
        if ttl_len < sub_len:
            return p_sets
        if ttl_len == sub_len:
            p_sets.append(0)
            return p_sets

        p_num = int(np.floor(ttl_len * 1.0 / sub_len))
        p_sets = [ele*sub_len for ele in np.arange(p_num)]
        return p_sets

    if overlap_flag == True:
        h_sets = split_patch_overlap(wsi_h, length)
        w_sets = split_patch_overlap(wsi_w, length)
    else:
        h_sets = split_patch_no_overlap(wsi_h, length)
        w_sets = split_patch_no_overlap(wsi_w, length)

    # combine points in both w and h direction
    if len(w_sets) > 0 and len(h_sets) > 0:
        coors_arr = list(itertools.product(h_sets, w_sets))

    return coors_arr


def wsi_patch_splitting(wsi_path, patch_dir, patch_size=299, save_size=299,
                        wsi_ext="tiff", save_ext="png",
                        pyramid_flag=True, overlap_flag=True, level=0):
    """ Spltting whole slide image to image patches.

    Parameters
    -------
    wsi_path: str
        path of the whole slide image
    patch_dir: str
        location to save the patch
    patch_size: int
        patch size to crop in whole slide image
    save_size: int
        the size of saved image patch
    wsi_ext: str
        file extension of whole slide image
    save_ext: str
        extension of saved image patch name
    pyramid_flag: boolean
        whole slide image is pyramid structure or not
    overlap_flag: boolean
        overlap between patches or not
    level: int
        whole slide image level to crop patch

    Returns
    -------
    None

    """

    if pyramid_flag == False:
        try:
            img = io.imread(wsi_path)
            if img.dtype == "uint16":
                img = (img / 256.0).astype(np.uint8)
            elif img.dtype == "uint8":
                pass
            else:
                raise Exception("Unknow imge data type")
        except:
            print("Cannot handle {}".format(wsi_path))
    else:
        wsi_header = openslide.OpenSlide(wsi_path)
        img = wsi_header.read_region(location=(0, 0), level=level,
                                     size=wsi_header.level_dimensions[level])
        img = np.asarray(img)[:,:,:-1]

    coors_arr = wsi_coor_splitting(wsi_h=img.shape[0], wsi_w=img.shape[1],
                                   length=patch_size, overlap_flag=overlap_flag)
    filename = os.path.splitext(os.path.basename(wsi_path))[0]
    for coor in coors_arr:
        h_start, w_start = coor[0], coor[1]
        cur_patch = img[h_start:h_start+patch_size, w_start:w_start+patch_size, :]
        if patch_size != save_size:
            save_patch = transform.resize(cur_patch, (save_size, save_size))
            save_patch = (save_patch * 255.0).astype(np.uint8)
        else:
            save_patch = cur_patch

        patch_name = "{}_{}.{}".format(filename, str(uuid.uuid4())[:8], save_ext)
        patch_filepath = os.path.join(patch_dir, patch_name)
        io.imsave(patch_filepath, save_patch)
