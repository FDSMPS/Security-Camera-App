import threading
from os import listdir
from os.path import join
from PIL import Image
from random import randint

class CameraInterface():
    lock = threading.Lock()
    
    def __init__(self):
        pass

    
    def mimic_get_image_from_camera(self):
        fpBase = "mockImages"
        images = listdir(fpBase)
        img = Image.open(join(fpBase, images[randint(0, len(images) - 1)]))

        return img

    def get_image_from_camera(self):
        # CameraInterface.lock.acquire()

        img = self.mimic_get_image_from_camera()

        # CameraInterface.lock.release()

        return img
