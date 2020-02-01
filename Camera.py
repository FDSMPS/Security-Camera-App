import threading
from os import listdir
from os.path import join
from PIL import Image
from random import randint

import io
from picamera import PiCamera
from picamera import mmal
import ctypes as ct


class PiCameraWorld(PiCamera):
    AWB_MODES = {
        'off':           mmal.MMAL_PARAM_AWBMODE_OFF,
        'auto':          mmal.MMAL_PARAM_AWBMODE_AUTO,
        'sunlight':      mmal.MMAL_PARAM_AWBMODE_SUNLIGHT,
        'cloudy':        mmal.MMAL_PARAM_AWBMODE_CLOUDY,
        'shade':         mmal.MMAL_PARAM_AWBMODE_SHADE,
        'tungsten':      mmal.MMAL_PARAM_AWBMODE_TUNGSTEN,
        'fluorescent':   mmal.MMAL_PARAM_AWBMODE_FLUORESCENT,
        'incandescent':  mmal.MMAL_PARAM_AWBMODE_INCANDESCENT,
        'flash':         mmal.MMAL_PARAM_AWBMODE_FLASH,
        'horizon':       mmal.MMAL_PARAM_AWBMODE_HORIZON,
        'greyworld':     ct.c_uint32(10)
        }

class CameraInterface():
    lock = threading.Lock()
    
    def __init__(self):
        pass

    def get_image_from_camera(self):
        CameraInterface.lock.acquire()

        imageStream = io.BytesIO()
        with PiCameraWorld() as camera:
            camera.awb_mode = 'greyworld'
            camera.resolution = (1080,720)
            camera.capture(imageStream, format='jpeg')

        imageStream.seek(0)
        img = Image.open(imageStream)

        CameraInterface.lock.release()

        return img