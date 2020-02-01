'''
    Creation Date: Feb 3, 2020
    Author: Tymoore Jamal
    Content: This file contains the live feed class which interfaces with the camera to send a live feed to the database.
'''

from Camera import CameraInterface
from Firebase import FirebaseInterface
from ImageProcessor import ImageProcessor
import time

class LiveFeed():
    '''
        The live feed class. Communicates with the camera and the database, to continusly send images to the database.
    '''

    def __init__(self, settings):
        '''
            Creates an instance of this class and initialzes its class variables.
            @param settings: the settings found in the config file.
        '''
        self.settings = settings
        self.camera = CameraInterface(settings)
        self.firebase = FirebaseInterface(settings)

    def run(self):
        '''
            This is the method that is ran when the thread is initially created, it continually reads images
            from the camera and writes it to the database.
        '''
        liveFeedImageRef = self.firebase.get_live_feed_image_ref()

        while True:
            print("Transmitting Live Feed")
            img = self.camera.get_image_from_camera()
            img = ImageProcessor.resizeImage(img, self.settings)
            imgString = str(ImageProcessor.convertImageToString(img), encoding='utf-8')
            self.firebase.update_live_feed(liveFeedImageRef, imgString)