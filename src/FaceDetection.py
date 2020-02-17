'''
    Creation Date: Feb 3, 2020
    Author: Tymoore Jamal
    Content: This file contains the face detection class which interfaces with the camera and motion sensors
            to perform face detection.
'''

# Imports
from Camera import CameraInterface
from Firebase import FirebaseInterface
from tensorflow.keras.models import load_model
import time
from MotionSensor import MotionSensorInterface
from ImageProcessor import ImageProcessor
import numpy as np
from os.path import join

class FaceDetection():
    '''
        The face detection class. Communicates with the camera and motion sensor and uses a machine learning model to detect faces.
    '''
    
    def __init__(self, settings):
        '''
            Creates an instance of this class and initialzes its class variables.
            @param settings: the settings found in the config file.
        '''
        self.settings = settings
        self.firebase = FirebaseInterface(settings)
        self.camera = CameraInterface(settings)
        self.motionSensor = MotionSensorInterface(settings)


    def run(self):
        '''
            This is the method that is ran when the thread is initially created, it loads the ML model. 
            It then continually, checks for motion and if detected, feeds the processed images through 
            the ML model to determine if a face is detected. If a face is detected then a notification 
            is created.
        '''
        model = load_model(join("..", "model", self.settings["ModelName"]))

        while True:
            if self.firebase.is_enabled():
                if self.motionSensor.is_motion_detected():
                    print("Motion Detected")
                    img = self.camera.get_image_from_camera()
                    
                    MLSize = (self.settings["MLImageWidth"], self.settings["MLImageHeight"])
                    partitionedImages = ImageProcessor.partitionImage(img, MLSize, self.settings["PartitionImageWidthDelta"],\
                        self.settings["PartitionImageHieghtDelta"],(self.settings["PartitionWidth"], self.settings["PartitionHeight"]))

                    # sometimes false results return x.xx E-16 therefore we set a threshold to bypass this
                    faceDetected = np.sum(model.predict(np.array(partitionedImages))) > self.settings["FaceDetectionThreshold"]
                    print("Face Detected?: " + str(faceDetected))

                    # if a face is detected send a notification
                    if (faceDetected):
                        self.firebase.sendNotifications(ImageProcessor.convertImageToString(img))
                        time.sleep(self.settings["FaceDetectionNotificationDownTime"]) 
