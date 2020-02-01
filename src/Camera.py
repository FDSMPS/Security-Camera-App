'''
    Creation Date: Feb 3, 2020
    Author: Tymoore Jamal
    Content: This file contains the Camera class which handles reading in images.
'''

import threading
from os import listdir
from os.path import join
from PIL import Image
from random import randint

import io
from picamera import PiCamera, mmal
import ctypes as ct

MMAL_PARAM_AWBMODE_T = 10 # found in picamera datasheet

class PiCameraWithoutIR(PiCamera):
    '''
        This class modifies the PiCamera class to perform IR filtering.
    '''

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
            'greyworld':     ct.c_uint32(MMAL_PARAM_AWBMODE_T)
            }

class CameraInterface():
    '''
        This class allows us to capture images from the camera. It does this in a safe manner uses a mutex.
    '''
    lock = threading.Lock()
    
    def __init__(self, settings):
        '''
            Creates an instance of this class and initialzes its class variables.
            @param settings: the settings found in the config file.
        '''
        self.settings = settings

    def get_image_from_camera(self):
        '''
            Gets an image from the camera.
            @return img: the recieved image.
        '''
        CameraInterface.lock.acquire()

        imageStream = io.BytesIO()
        with PiCameraWithoutIR() as camera:
            camera.awb_mode = 'greyworld'
            camera.resolution = (self.settings["CameraResolutionWidth"], self.settings["CameraResolutionHeight"])
            camera.capture(imageStream, format='jpeg')

        imageStream.seek(0) # start image stream at the beginning
        img = Image.open(imageStream)

        CameraInterface.lock.release()

        return img