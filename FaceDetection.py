from Camera import CameraInterface
from Firebase import FirebaseInterface
from tensorflow.keras.models import load_model
import time

class FaceDetection():

    def run(self):
        while True:
            print("Face Detection Running")
            time.sleep(5)

    def load_FD_Model(self, modelName):
        return load_model(modelName)

    def __init__(self, modelName, serviceAccountFile):
        self.camera = CameraInterface()
        self.firebase = FirebaseInterface(serviceAccountFile)
        self.model = self.load_FD_Model(modelName)