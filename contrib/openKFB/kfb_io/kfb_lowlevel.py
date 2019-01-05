from __future__ import division
from ctypes import *
from openslide import lowlevel
from itertools import count
import numpy as np

_lib = cdll.LoadLibrary("libkfbslide.so")

class _KfbSlide(object):
    def __init__(self, ptr):
        self._as_parameter_ = ptr
        self._valid = True
        self._close = kfbslide_close

    def __del__(self):
        if self._valid:
            self._close(self)

    def invalidate(self):
        self._valid = False

    @classmethod
    def from_param(cls, obj):
        if obj.__class__ != cls:
            raise ValueError("Not an KfbSlide reference")
        if not obj._as_parameter_:
            raise ValueError("Passing undefined slide object")
        if not obj._valid:
            raise ValueError("Passing closed kfbSlide object")
        return obj

# check for errors opening an image file and wrap the resulting handle
def _check_open(result, _func, _args):
    if result is None:
        raise lowlevel.OpenSlideUnsupportedFormatError(
            "Unsupported or missing image file")
    slide = _KfbSlide(c_void_p(result))
    '''
    err = get_error(slide)
    if err is not None:
        raise OpenSlideError(err)
    '''
    return slide

# check if the library got into an error state after each library call
def _check_error(result, func, args):
    '''
    err = get_error(args[0])
    if err is not None:
        raise lowlevel.OpenSlideError(err)
    '''
    return lowlevel._check_string(result, func, args)

# resolve and return an OpenSlide function with the specified properties
def _func(name, restype, argtypes, errcheck=_check_error):
    func = getattr(_lib, name)
    func.argtypes = argtypes
    func.restype = restype
    if errcheck is not None:
        func.errcheck = errcheck
    return func

detect_vendor = _func("kfbslide_detect_vendor", c_char_p, [lowlevel._utf8_p],
                                   lowlevel._check_string)
_kfbslide_open = _func("kfbslide_open", c_void_p, [lowlevel._utf8_p], _check_open)


def kfbslide_open(name):
    print("Before open file %s in kfbslide_ope" % name)
    osr = _kfbslide_open(name)
    if osr is None:
        print("Fail to open file : ", name)
    return osr

kfbslide_close = _func("kfbslide_close", None, [_KfbSlide], lowlevel._check_close)
kfbslide_get_level_count = _func("kfbslide_get_level_count", c_int32, [_KfbSlide])

_kfbslide_get_level_dimensions = _func("kfbslide_get_level_dimensions", None,
                                       [_KfbSlide, c_int32, POINTER(c_int64), POINTER(c_int64)])

def kfbslide_get_level_dimensions(osr, level):
    w = c_int64()
    h = c_int64()
    _kfbslide_get_level_dimensions(osr, level, byref(w), byref(h))
    return (w.value, h.value)

kfbslide_get_level_downsample = _func("kfbslide_get_level_downsample", c_double, [_KfbSlide, c_int32])
kfbslide_get_best_level_for_downsample = _func(
    "kfbslide_get_best_level_for_downsample", c_int32, [_KfbSlide, c_double])
_kfbslide_read_region = _func("kfbslide_read_region", c_bool, [_KfbSlide, c_int32, c_int64, c_int64, \
                               POINTER(c_int), POINTER(POINTER(c_ubyte))])
_kfb_delete_imagedata = _func("kfb_delete_imagedata", c_bool, [POINTER(c_ubyte)])

def kfbslide_read_region(osr, level, pos_x, pos_y):
    data_length = c_int()
    pixel = POINTER(c_ubyte)()
    if not _kfbslide_read_region( osr, level, pos_x, pos_y, 
                byref(data_length), byref(pixel)):
                
        raise ValueError("Fail to read region")
    #print("DataLength : ", data_length)
    if data_length.value == 0:
        raise Exception("Fail to read region")
    
    img_array = np.ctypeslib.as_array(pixel, shape=(data_length.value,)).copy()
    
    return_bool = _kfb_delete_imagedata(pixel)
    #print('delete status: ', return_bool)
    
    return img_array

#ptr =   cast(pixel, POINTER(c_ubyte * data_length.value))
    #img_array = np.asarray(ptr.contents)
    #bb = np.zeros_like(img_array, dtype=np.uint8)
# Convert returned NULL-terminated char** into a list of strings
def _check_name_list(result, func, args):
    _check_error(result, func, args)
    names = []
    for i in count():
        name = result[i]
        if not name:
            break
        names.append(name.decode('UTF-8', 'replace'))
    return names

kfbslide_property_names = _func("kfbslide_get_property_names", POINTER(c_char_p),
                                    [_KfbSlide], _check_name_list)

kfbslide_property_value = _func("kfbslide_get_property_value", c_char_p, [_KfbSlide, lowlevel._utf8_p])

_kfbslide_get_associated_image_names = _func("kfbslide_get_associated_image_names", POINTER(c_char_p), [_KfbSlide])
def kfbslide_get_associated_image_names(osr):
    names = _kfbslide_get_associated_image_names(osr)
    rtn = []
    for name in names:
        if name is None:
            break
        rtn.append(name)
    return rtn

_kfbslide_get_associated_image_dimensions = _func("kfbslide_get_associated_image_dimensions", c_void_p, [_KfbSlide, lowlevel._utf8_p, POINTER(c_int64), POINTER(c_int64), POINTER(c_int)])
def kfbslide_get_associated_image_dimensions( osr, name):
    w = c_int64()
    h = c_int64()
    data_length = c_int()
    _kfbslide_get_associated_image_dimensions(osr, name, byref(w), byref(h), byref(data_length))
    return (w.value, h.value), data_length.value

_kfbslide_read_associated_image = _func("kfbslide_read_associated_image", c_void_p, [_KfbSlide, lowlevel._utf8_p, POINTER(POINTER(c_ubyte))])
def kfbslide_read_associated_image(osr, name):
    data_length = kfbslide_get_associated_image_dimensions(osr, name)[1]
    pixel = POINTER(c_ubyte)()
    _kfbslide_read_associated_image(osr, name, byref(pixel))
    import numpy as np
    narray = np.ctypeslib.as_array(pixel, shape=(data_length,))
    from io import BytesIO
    buf = BytesIO(narray)
    from PIL import Image
    return Image.open(buf)

def main():
    osr = kfbslide_open('/media/dyj/work/Projects/PathPlanet/TCGA_diagnostic_data/Skin/1.kfb')
    names = kfbslide_get_associated_image_names(osr)
    print(names)
    level_cnt = kfbslide_get_level_count(osr)
    print("Level count : ", level_cnt)
    width = c_int64()
    height = c_int64()
    for level in range(level_cnt):
        _kfbslide_get_level_dimensions(osr, c_int32(level), byref(width), byref(height))
        print("Level {0} : {1}, {2}".format( level, width, height))

        downsample = kfbslide_get_level_downsample(osr, level)
        print("Level {0} downsample : {1}".format( level, downsample))
        print("Level {0} best downsample : {1}".format( level, kfbslide_get_best_level_for_downsample(osr, downsample - 1)))
    prop_names = kfbslide_property_names( osr )
    print(prop_names)
    for name in prop_names:
        print( name, "  --->  ", kfbslide_property_value( osr, name))

    asso_img_names = kfbslide_get_associated_image_names(osr)
    print("Associate Imagae Names : ", asso_img_names)
    for name in asso_img_names:
        if name is None:
            break
        ksize, datalength = kfbslide_get_associated_image_dimensions(osr, name)
        width, height = ksize
        print( name, " ---> width : ", width, ", height : ", height, ", datalength : ", datalength)
        img = kfbslide_read_associated_image(osr, name)
        file_name = "./output/" + name.decode("utf8") + ".jpg"
        img.save( file_name)
    '''
    dest = POINTER(c_ubyte)()
    x_mid = int(int( width.value / 256 / 2) * 256)
    y_mid = int(int( height.value / 256 / 2) * 256)
    datalength = c_int(0)
    kfbslide_read_region(osr, 0, x_mid, y_mid, byref(datalength), byref(dest))
    import numpy as np
    nparr = np.ctypeslib.as_array(dest, shape=(datalength.value,))
    with open("./output/img_test.jpg", "wb") as file:
        file.write(nparr)

    '''
    kfbslide_close(osr)

if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print("Error happens : ", err)
