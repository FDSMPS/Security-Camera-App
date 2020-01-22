import threading
from random import random

class MotionSensorInterface():
    lock = threading.Lock()
    
    def __init__(self):
        pass

    def mimic_is_motion_detected(self):
        result = random() > 0.8
        return result

    def is_motion_detected(self):
        # MotionSensorInterface.lock.acquire()

        img = self.mimic_is_motion_detected()

        # MotionSensorInterface.lock.release()

        return img