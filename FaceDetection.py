from Camera import CameraInterface
from Firebase import FirebaseInterface
from tensorflow.keras.models import load_model
import time
from MotionSensor import MotionSensorInterface
from ImageProcessor import ImageProcessor
import numpy as np

class FaceDetection():


    def run(self):

        motionSensor = MotionSensorInterface()

        while True:
            if motionSensor.is_motion_detected():
                print("Motion Detected")
                img = self.camera.get_image_from_camera()
                partitionedImages = ImageProcessor.partitionImage(img, self.MLImageSize, \
                    self.PartitionImageWidthDelta, self.PartitionImageHieghtDelta, self.PartitionSize)
                
                # sometimes false results return x.xx E-16 therefore we set the threashold at 0.5 instead of 0
                faceDetected = np.sum(self.model.predict(np.array(partitionedImages))) > 0.5
                
                if faceDetected:
                    pass

    def load_FD_Model(self, modelName):
        return load_model(modelName)

    def __init__(self, modelName, MLImageSize, PartitionImageWidthDelta, \
        PartitionImageHieghtDelta, PartitionSize, securityCameraReference):
        self.camera = CameraInterface()
        self.model = self.load_FD_Model(modelName)
        self.MLImageSize = MLImageSize
        self.PartitionImageWidthDelta = PartitionImageWidthDelta
        self.PartitionImageHieghtDelta = PartitionImageHieghtDelta
        self.PartitionSize = PartitionSize
        self.securityCameraReference = securityCameraReference
        self.firebase = FirebaseInterface()
