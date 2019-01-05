import os
import cv2
import numpy as np
from threading import Lock
from collections import namedtuple

import math
import openslide
from openslide import open_slide
from openslide.deepzoom import DeepZoomGenerator

# Library for kfb slide
from . import kfbslide
from .kfb_deepzoom import KfbDeepZoomGenerator

def imread(imgfile):
    assert os.path.exists(imgfile), '{} does not exist!'.format(imgfile)
    srcBGR = cv2.imread(imgfile)
    destRGB = cv2.cvtColor(srcBGR, cv2.COLOR_BGR2RGB)
    return destRGB

def imresize_shape(img, outshape):
    
    outshape = ( int(outshape[0]) , int(outshape[1])  )
    if (img.shape[0], img.shape[1]) == outshape:
        return img
    temp = cv2.resize(img, (outshape[1], outshape[0]))
    if len(img.shape) == 3 and img.shape[2] == 1:
        temp = np.reshape(temp, temp.shape + (1,))
    return temp

def get_region(slide_img, location=None, level=None, size=None, img_type = 'openslide'):
    # here, location is at level 0, but size is at level level.
    #import pdb; pdb.set_trace()
    # img_type: openslide / image
    if img_type is 'openslide':
        cur_patch = slide_img.read_region(location=location, level=level, size=size)
    if img_type is 'image':
        ratio = 2**level
        true_size = [size[0]*ratio, size[1]*ratio  ]
        row_st, col_st = location[1], location[0]
        cur_patch = slide_img[row_st:row_st+true_size[1], col_st:col_st+true_size[0],:]
        cur_patch = imresize_shape(cur_patch, [size[1], size[0]])
        
    return cur_patch


def patch_read_slide(slide_path, location=[0,0], level=0, size=None, 
                     region_window=10000, use_grey = False):
    # location are set in highest resolution case. it will adjust using level
    # size is also at level 0, but size will be transformed to level when call get_region
    # both location, size are in [x, y] format
    # it supports both image type and slide type.
    
    file_ext = os.path.splitext( os.path.basename(slide_path) )[1]
    
    img_type = 'openslide'

    if file_ext in ['.svs', '.tif', '.png', '.jpg']:
        if file_ext in ['.tif', '.png', '.jpg']:
            try:
                slide_img  = openslide.open_slide(slide_path)
                SlideWidth,  SlideHeight = slide_img.level_dimensions[level]
                highest_SlideWidth,  highest_SlideHeight = slide_img.level_dimensions[0]
                ratio = slide_img.level_downsamples[level]

            except:
                slide_img  = imread(slide_path)
                ratio = 2**level
                highest_SlideHeight, highest_SlideWidth = slide_img.shape[0:2]
                SlideWidth,  SlideHeight = highest_SlideWidth//ratio,  highest_SlideHeight//ratio
                img_type = 'image' 
                    
        else:
            slide_img  = openslide.open_slide(slide_path)
            SlideWidth,  SlideHeight = slide_img.level_dimensions[level]
            highest_SlideWidth,  highest_SlideHeight = slide_img.level_dimensions[0]
            ratio = slide_img.level_downsamples[level]

    elif file_ext in ['.kfb']:
        slide_img  = kfbslide.open_kfbslide(slide_path)
        SlideWidth,  SlideHeight = slide_img.level_dimensions[level]
        highest_SlideWidth,  highest_SlideHeight = slide_img.level_dimensions[0]

        ratio = slide_img.level_downsamples[level]
        SlideWidth,  SlideHeight = SlideWidth-256,\
                                   SlideHeight-256

    if size is None:
        size = [SlideWidth, SlideHeight]
    else:
        size = [ math.floor(size[0]/ratio), math.floor(size[1]/ratio) ]
    location = [ math.floor(float(location[0])/ratio), math.floor(float(location[1])/ratio)  ]  
    print('start loading image: ', size)

    col_size_, row_size_ = size
    cs, rs = location
    ce, re = min(cs + col_size_, SlideWidth), min(rs + row_size_, SlideHeight)

    col_size, row_size = ce-cs, re-rs

    num_row, num_col = math.ceil(row_size/region_window),  \
                       math.ceil(col_size/region_window) # lower int
    
    if not use_grey:
        patch_ret = np.zeros((row_size, col_size, 3), dtype=np.uint8)+1
    else:
        patch_ret = np.zeros((row_size, col_size, 1), dtype=np.uint8)+1

    for row_idx in range(num_row):
        row_start = row_idx * region_window + rs
        row_end   = min(row_start + region_window, re)

        for col_idx in range(num_col):
            col_start = col_idx * region_window + cs
            col_end   = min(col_start + region_window, ce)

            this_location = (col_start, row_start)
            this_size = (col_end-col_start, row_end-row_start)
            
            location_l0 = ( int(col_start*ratio), int(row_start*ratio))
            
            cur_patch = get_region(slide_img, location=location_l0, 
                                    level=level, size=this_size, img_type = img_type)
            
            cur_patch = np.asarray(cur_patch)[:,:,0:3]

            if use_grey:
                cur_patch =  0.2989*cur_patch[:,:,0] + 0.5870*cur_patch[:,:,1] + 0.1140*cur_patch[:,:,2]
                cur_patch = cur_patch[:,:,None]
                
            patch_ret[row_start-rs:row_end-rs, col_start-cs:col_end-cs,:] = cur_patch.astype(np.uint8)

            print('Finish loading slide at: ', (row_start, row_end, col_start,col_end) )
    return patch_ret


def read_slide_region(slide_img, location=[0,0], level=0, size=None, 
                      region_window=10000, use_grey = False, img_type = 'openslide'):
    # location are set in highest resolution case. it will adjust using level
    # size is also at level 0, but size will be transformed to level when call get_region
    # both location, size are in [x, y] format
    # it supports both image type and slide type.
    
    SlideWidth,  SlideHeight = slide_img.level_dimensions[level]
    highest_SlideWidth,  highest_SlideHeight = slide_img.level_dimensions[0]
    
    ratio = slide_img.level_downsamples[level]
    SlideWidth,  SlideHeight = SlideWidth-256,\
                                SlideHeight-256

    if size is None:
        size = [SlideWidth, SlideHeight]
    else:
        size = [ math.floor(size[0]/ratio), math.floor(size[1]/ratio) ]
    location = [ math.floor(float(location[0])/ratio), math.floor(float(location[1])/ratio)  ]  
    print('start loading image: ', size)

    col_size_, row_size_ = size
    cs, rs = location
    ce, re = min(cs + col_size_, SlideWidth), min(rs + row_size_, SlideHeight)

    col_size, row_size = ce-cs, re-rs

    num_row, num_col = math.ceil(row_size/region_window),  \
                       math.ceil(col_size/region_window) # lower int
    
    if not use_grey:
        patch_ret = np.zeros((row_size, col_size, 3), dtype=np.uint8)+1
    else:
        patch_ret = np.zeros((row_size, col_size, 1), dtype=np.uint8)+1

    for row_idx in range(num_row):
        row_start = row_idx * region_window + rs
        row_end   = min(row_start + region_window, re)

        for col_idx in range(num_col):
            col_start = col_idx * region_window + cs
            col_end   = min(col_start + region_window, ce)

            this_location = (col_start, row_start)
            this_size = (col_end-col_start, row_end-row_start)
            
            location_l0 = ( int(col_start*ratio), int(row_start*ratio))
            
            cur_patch = get_region(slide_img, location=location_l0, 
                                   level=level, size=this_size, img_type = img_type)
            #print('cur_patch shape is: ', cur_patch.shape, 'patch_ret shape is: ', patch_ret.shape)
            #print('local parameters: ', location_l0, this_size)
            #print('rs, re, cs, ce: ', row_start-rs, row_end-rs, col_start-cs, col_end-cs)

            cur_patch = np.asarray(cur_patch)[:,:,0:3]

            if use_grey:
                cur_patch =  0.2989*cur_patch[:,:,0] + 0.5870*cur_patch[:,:,1] + 0.1140*cur_patch[:,:,2]
                cur_patch = cur_patch[:,:,None]

            patch_ret[row_start-rs:row_end-rs, col_start-cs:col_end-cs,:] = cur_patch.astype(np.uint8)

            print('Finish loading slide at: ', (row_start, row_end, col_start,col_end) )
    return patch_ret
