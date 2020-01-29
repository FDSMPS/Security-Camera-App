import threading
from random import random
import RPi.GPIO as GPIO

class MotionSensorInterface():
    lock = threading.Lock()
    
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.IN)
        GPIO.setup(13, GPIO.IN)
        GPIO.setup(15, GPIO.IN)

    def mimic_is_motion_detected(self):
        result = random() > 0.8
        return result

    def is_motion_detected(self):
        # MotionSensorInterface.lock.acquire()

        detected = GPIO.input(11) or GPIO.input(13) or GPIO.input(15)
        # MotionSensorInterface.lock.release()

        return detected