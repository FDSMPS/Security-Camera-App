'''
    Creation Date: Feb 3, 2020
    Author: Tymoore Jamal
    Content: This is the firebase class. It handles the interactions that this application has with firebase.
'''

import threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class FirebaseInterface():
    '''
        The firebase interface class. Handles all interactions with firebase.
    '''

    instancesMade = 0

    def __init__(self, settings):
        '''
            Creates an instance of this class. If it is the first instance made
            initializes the connection to firebase.

            @param settings: the settings found in the config file.

        '''
        self.settings = settings

        FirebaseInterface.instancesMade += 1

        if FirebaseInterface.instancesMade == 1:
            self.connect_to_firebase()

        self.root = db.reference()

    def sendNotification(self):
        '''
            Sends a notification to users who are subscribed to this camera. 
        '''
        # TODO: Send notification to associates users.
        pass
    
    def connect_to_firebase(self):
        '''
            Establishes a connection to firebase. Only can be run once per session.
        '''
        cred = credentials.Certificate(self.settings["ServiceAccountFile"])
        firebase_admin.initialize_app(cred, {
            'databaseURL': self.settings["DatabaseURL"]
        })

    
    def get_data(self, ref = None):
        '''
            Get all data from a given node.

            @param ref: the refrence node. If None, the root will be used.
            @return result: the retrieved data
        '''
        if ref == None:
            ref = self.root

        return ref.get()

    def get_security_camera_ref(self):
        '''
            Get the reference node for this camera
            @return: the reference
        '''
        return self.root.child("SecurityCameras").child(self.settings["QRCode"])

    def is_registered(self):
        '''
            Determine if the current camera is registered.
            @return: if the camera is registered or not.
        '''
        securityCameraReference = self.get_security_camera_ref()
        registeredRef = securityCameraReference.child('registered')
        registered = self.get_data(registeredRef)
        return registered

    def get_live_feed_image_ref(self):
        '''
            Return the live feed image reference. This is to setup writing to this reference.
            @return liveFeedImageRef: the live feed image reference
        '''
        securityCameraReference = self.get_security_camera_ref()
        liveFeedImageRef = securityCameraReference.child("currentImage")
        return liveFeedImageRef

    def update_live_feed(self, liveFeedImageRef, imageString):
        '''
            Update the live feed with the specified image
            @param liveFeedImageRef: the live feed image referance
            @param imageString: the image to store
            @return: the image reference to the new image
        '''
        return self.set_data(liveFeedImageRef, imageString)

    def set_data(self, ref, data):
        '''
            Sets the data for a specific node
            @param ref: the reference to write to
            @param data: the data to write
            @return: The reference to the new data
        '''
        return ref.set(data)
