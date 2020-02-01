'''
    Creation Date: Feb 3, 2020
    Author: Tymoore Jamal
    Content: This file contains the Motion Sensor class which handles reading in motion.
'''

import threading
from random import random
import RPi.GPIO as GPIO

class MotionSensorInterface():
    '''
        The motion sensor class. Polls three motion sensors to determine if any detects motion.
    '''
    
    def __init__(self, settings):
        '''
            Creates an instance of this class and initialzes its class variables.
            @param settings: the settings found in the config file.
        '''
        self.settings = settings
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(settings["MotionSensorOnePin"], GPIO.IN)
        GPIO.setup(settings["MotionSensorTwoPin"], GPIO.IN)
        GPIO.setup(settings["MotionSensorThreePin"], GPIO.IN)

    def is_motion_detected(self):
        '''
            Polls three motion sensors to determine if any motion is detected.
            @returns detected: if motion is detected.
        '''
        detected = GPIO.input(self.settings["MotionSensorOnePin"]) \
            or GPIO.input(self.settings["MotionSensorTwoPin"]) \
            or GPIO.input(self.settings["MotionSensorThreePin"])
        return detected