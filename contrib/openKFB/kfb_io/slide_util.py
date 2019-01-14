'''
This module encapsulate operations about slide
'''
import os
import numpy as np
from threading import Lock
from collections import namedtuple

from openslide import open_slide
from openslide.deepzoom import DeepZoomGenerator

# Library for kfb slide
from . import kfbslide
from ..file_founder import FileFounderFactory
from  .kfb_deepzoom import KfbDeepZoomGenerator
from .io_image import read_slide_region


class KfbSlideClass:
    @classmethod
    def open_slide(cls, slide_file_path):
        return kfbslide.open_kfbslide(slide_file_path)

    @classmethod
    def get_deepzoom(cls, slide):
        return KfbDeepZoomGenerator(slide)


class OpenSlideClass:
    @classmethod
    def open_slide(cls, slide_file_path):
        return open_slide(slide_file_path)

    @classmethod
    def get_deepzoom(cls, slide):
        return DeepZoomGenerator(slide)


class SlideClassFactory:
    __non_openslide_classes = {".kfb": KfbSlideClass}

    @classmethod
    def get_slide_class(cls, file_ext):
        if file_ext in cls.__non_openslide_classes:
            return cls.__non_openslide_classes[file_ext]
        else:
            return OpenSlideClass

SlideDeepzoom = namedtuple('SlideDeepzoom', ['slide', 'deepzoom'])

class SlideManager:
    _slide_deepzoom = {}
    _dict_lock = Lock()

    @staticmethod
    def get_slide_local_path( slide_id):
        return FileFounderFactory.get_file_path(slide_id)

    @staticmethod
    def __load_slide(slide_local_path):
        file_ext = os.path.splitext(slide_local_path)[1]
        slide_class = SlideClassFactory.get_slide_class(file_ext)
        slide = slide_class.open_slide(slide_local_path)
        deepzoom = slide_class.get_deepzoom(slide)
        return slide, deepzoom

    @classmethod
    def __get_slide_deepzoom(cls, slide_id):
        ''' do not use buffer to avoid memory leak
        slide_local_path = cls.get_slide_local_path( request, slide_id)
        slide, deepzoom = cls.__load_slide(slide_local_path)
        return SlideDeepzoom(slide = slide, deepzoom = deepzoom)
        '''
        if slide_id not in cls._slide_deepzoom:
            with cls._dict_lock:
                if slide_id not in cls._slide_deepzoom:
                    slide_local_path = cls.get_slide_local_path( slide_id)
                    slide, deepzoom  = cls.__load_slide(slide_local_path)
                    cls._slide_deepzoom[slide_id] = SlideDeepzoom(
                        slide=slide, deepzoom=deepzoom)
        return cls._slide_deepzoom[slide_id]

    @classmethod
    def get_slide(cls, slide_id):
        return cls.__get_slide_deepzoom( slide_id).slide

    @classmethod
    def get_deepzoom(cls,  slide_id):
        return cls.__get_slide_deepzoom(  slide_id).deepzoom

def get_slide(slide_id):
    return SlideManager.get_slide(slide_id)


def get_deepzoom(slide_id):
    return SlideManager.get_deepzoom(slide_id)

def get_slide_info():
    if file_ext in ['.svs', '.tif', '.png', '.jpg']:
        if file_ext in ['.tif', '.png', '.jpg']:
            try:
                slide_img  = imread(slide_path)
                ratio = 2**level
                highest_SlideHeight, highest_SlideWidth = slide_img.shape[0:2]
                SlideWidth,  SlideHeight = highest_SlideWidth//ratio,  highest_SlideHeight//ratio
                img_type = 'image'

            except:
                slide_img  = openslide.open_slide(slide_path)
                SlideWidth,  SlideHeight = slide_img.level_dimensions[level]
                highest_SlideWidth,  highest_SlideHeight = slide_img.level_dimensions[0]
                ratio = slide_img.level_downsamples[level]

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


class IOCLS__(object):
    def __init__(self, idSlide, x_coords=None, y_coords=None):
        '''
            do some special treatments for jpg, png, etc. later on
        '''
        self.file_path = SlideManager.get_slide_local_path(idSlide)
        file_name      = os.path.basename(self.file_path)
        self.file_ext  = os.path.splitext(file_name)[1]  #'.ext, .jpg'
        self.slide     = get_slide(idSlide)


        rs, cs, re, ce = self.get_info(x_coords, y_coords)
        self.rs = rs
        self.cs = cs
        self.re = re
        self.ce = ce

    #def close(self):
    #    self.slide.close()

    def get_info(self, x_coords=[], y_coords=[]):
        SLIDE_LEVEL = 0
        HEIGHT_SCALE = 1.0
        WIDTH_SCALE = 1.0
        TILE_SIZE = 256

        slide_width, slide_height = self.slide.level_dimensions[0]
        if len(x_coords ) > 0 and len(y_coords)> 0:
            # Get sub image
            minx_coor, maxx_coor = min(x_coords), max(x_coords)
            centerx_coor = int((minx_coor + maxx_coor) / 2.0)
            miny_coor, maxy_coor = min(y_coords), max(y_coords)
            centery_coor = int((miny_coor + maxy_coor) / 2.0)
            # contour width and height
            contour_width = maxx_coor-minx_coor
            contour_height = maxy_coor-miny_coor

            # get region min x and y coordinates: consider can less than 0
            region_minx_coor = int(centerx_coor - contour_width * WIDTH_SCALE / 2.0)
            region_minx_coor = region_minx_coor if region_minx_coor >= 0 else 0
            region_miny_coor = int(centery_coor - contour_height * HEIGHT_SCALE / 2.0)
            region_miny_coor = region_miny_coor if region_miny_coor >= 0 else 0
            # get region max x and y coordinates: consider can less than 0
            region_maxx_coor = int(centerx_coor +   contour_width * WIDTH_SCALE / 2.0)
            region_maxx_coor = region_maxx_coor if  region_maxx_coor < slide_width else slide_width-1
            region_maxy_coor = int(centery_coor +   contour_height * HEIGHT_SCALE / 2.0)
            region_maxy_coor = region_maxy_coor if  region_maxy_coor < slide_height else slide_height-1

            rs, cs, re, ce = region_miny_coor, region_minx_coor, region_maxy_coor, region_maxx_coor
        else:
            rs,cs, re, ce = 0, 0, slide_height-256, slide_width-256

        return rs, cs, re, ce

    def read_region(self, location=[0,0],  size=[256, 256],  level=0, use_grey=False):
        # in [x, y] format
        #return self.slide.read_region(location=location,  size=size,  level=level)
        return read_slide_region(self.slide, location=location,  size=size,  level=level,
                                 region_window=10000, use_grey = use_grey)


class IOCLS(object):
    def __init__(self, idSlide, x_coords=None, y_coords=None, level=0):
        '''
            do some special treatments for jpg, png, etc. later on
        '''
        self.file_path = SlideManager.get_slide_local_path(idSlide)
        file_name      = os.path.basename(self.file_path)

        self.file_ext  = os.path.splitext(file_name)[1]  #'.ext, .jpg'
        self.slide     = get_slide(idSlide)
        self.naked_name = os.path.splitext(file_name)[0]  #'.ext, .jpg'

        rs, cs, re, ce = self.get_info(x_coords, y_coords)
        self.rs = rs
        self.cs = cs
        self.re = re
        self.ce = ce

    #def close(self):
    #    self.slide.close()

    def get_info(self, x_coords=[], y_coords=[]):
        SLIDE_LEVEL = 0
        HEIGHT_SCALE = 1.0
        WIDTH_SCALE = 1.0
        TILE_SIZE = 256

        slide_width, slide_height = self.slide.level_dimensions[0]
        if len(x_coords ) > 0 and len(y_coords)> 0:
            # Get sub image
            minx_coor, maxx_coor = min(x_coords), max(x_coords)
            centerx_coor = int((minx_coor + maxx_coor) / 2.0)
            miny_coor, maxy_coor = min(y_coords), max(y_coords)
            centery_coor = int((miny_coor + maxy_coor) / 2.0)
            # contour width and height
            contour_width = maxx_coor-minx_coor
            contour_height = maxy_coor-miny_coor

            # get region min x and y coordinates: consider can less than 0
            region_minx_coor = int(centerx_coor - contour_width * WIDTH_SCALE / 2.0)
            region_minx_coor = region_minx_coor if region_minx_coor >= 0 else 0
            region_miny_coor = int(centery_coor - contour_height * HEIGHT_SCALE / 2.0)
            region_miny_coor = region_miny_coor if region_miny_coor >= 0 else 0
            # get region max x and y coordinates: consider can less than 0
            region_maxx_coor = int(centerx_coor +   contour_width * WIDTH_SCALE / 2.0)
            region_maxx_coor = region_maxx_coor if  region_maxx_coor < slide_width else slide_width-1
            region_maxy_coor = int(centery_coor +   contour_height * HEIGHT_SCALE / 2.0)
            region_maxy_coor = region_maxy_coor if  region_maxy_coor < slide_height else slide_height-1

            rs, cs, re, ce = region_miny_coor, region_minx_coor, region_maxy_coor, region_maxx_coor
        else:
            rs,cs, re, ce = 0, 0, slide_height-256, slide_width-256

        return rs, cs, re, ce

    def read_region(self, location=[0,0],  size=[256, 256],  level=0, use_grey=False,  **kwargs):
        # in [x, y] format
        downsample_ratio = self.slide.level_downsamples[level]

        true_size = [int(r/downsample_ratio) for r in size]

        cur_patch  = self.slide.read_region(location=location,  size=true_size,  level=level)
        cur_patch  = np.asarray(cur_patch)

        if use_grey:
            cur_patch =  0.2989*cur_patch[:,:,0] + 0.5870*cur_patch[:,:,1] + 0.1140*cur_patch[:,:,2]
            cur_patch = cur_patch[:,:,None]
        return cur_patch
