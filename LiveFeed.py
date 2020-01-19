from Camera import CameraInterface
from Firebase import FirebaseInterface
import time

class LiveFeed():
    def run(self):
        while True:
            print("Live Feed Running")
            time.sleep(2)

    def __init__(self, serviceAccountFile):
        self.camera = CameraInterface()
        self.firebase = FirebaseInterface(serviceAccountFile)