'''
    Creation Date: Feb 3, 2020
    Author: Tymoore Jamal
    Content: This is the firebase class. It handles the interactions that this application has with firebase.
'''

import threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from os.path import join
import uuid
from datetime import datetime
from pyfcm import FCMNotification

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


    def get_users(self):
        '''
            Gets a list of all users connected to this camera. 
        '''
        return self.get_data(self.get_security_camera_ref().child("users"))

    def generateNotificationImage(self, imageString):
        notificationImageID = uuid.uuid4().hex
        notificationImage = {"imageData": imageString, "imageId": notificationImageID}
        self.root.child("NotificationImages").child(notificationImageID).set(notificationImage)
        return notificationImageID

    def generateNotification(self, user, notificationImageID):
        notificationID = uuid.uuid4().hex
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        notification = {"cameraCode": self.settings["QRCode"], "datetime": dt, "imageId": notificationImageID, "notificationId": notificationID}
        self.root.child("Notifications").child(notificationID).set(notification)
        return notificationID

    def sendPushNotification(self, user):
        # Read in API key
        with open(join("..", self.settings["CloudMessagingAPIFile"]), 'r') as apiKeyFile:
            APIKey = apiKeyFile.read()

        pushNotification = FCMNotification(api_key=APIKey)

        # return pushNotification.notify_single_device(\
        #     registration_id = self.root.child("Users").child(user).child("registrationId").get(), \
        #     message_title = self.settings["PushNotificationTitle"], \
        #     message_body = self.settings["PushNotificationMessage"])

        # return pushNotification.notify_single_device(\
        #     registration_id = user, \
        #     message_title = self.settings["PushNotificationTitle"], \
        #     message_body = self.settings["PushNotificationMessage"])

        # return pushNotification.notify_multiple_devices(\
        #     registration_ids = [user], \
        #     message_title = self.settings["PushNotificationTitle"], \
        #     message_body = self.settings["PushNotificationMessage"])

        return pushNotification.notify_topic_subscribers(\
            topic_name = self.settings["QRCode"], \
            message_body = self.settings["PushNotificationMessage"])

    def addNotificationToUser(self, user, notificationID):
        userNotification = {"notificationId": notificationID, "read": False}
        self.root.child("Users").child(user).child("UserNotifications").child(notificationID).set(userNotification)
        

    def sendNotificationToUser(self, user, notificationImageID):
        notificationID = self.generateNotification(user, notificationImageID)
        self.addNotificationToUser(user, notificationID)
        print(self.sendPushNotification(user))

    def sendNotifications(self, imageString):
        '''
            Sends a notification to users who are subscribed to this camera. 
        '''
        users = self.get_users()
        if len(users) > 0:
            notificationImageID = self.generateNotificationImage(imageString)
            for user in users:
                self.sendNotificationToUser(user, notificationImageID)
        
    def connect_to_firebase(self):
        '''
            Establishes a connection to firebase. Only can be run once per session.
        '''
        cred = credentials.Certificate(join("..", self.settings["ServiceAccountFile"]))
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
        registered = self.get_data(self.get_security_camera_ref().child("registered"))

        # convert from string to bool if needed, otherwise return the bool
        if type(registered) == bool:
            return registered

        return registered.lower() == "true"
    
    def get_servo_x_position(self):
        '''
            Get the servo X position.
            @return: the servo x position.
        '''
        return self.get_data(self.get_security_camera_ref().child("servoXPosition"))

    def get_servo_y_position(self):
        '''
            Get the servo y position.
            @return: the servo y position.
        '''
        return self.get_data(self.get_security_camera_ref().child("servoYPosition"))

    def is_enabled(self):
        '''
            Determine if the current camera is enabled.
            @return: if the camera is enabled or not.
        '''
        enabled = self.get_data(self.get_security_camera_ref().child("cameraEnabled"))
        
        # convert from string to bool if not a bool
        if type(enabled) == bool:
            return enabled

        return enabled.lower() == "true"

    def get_live_feed_image_ref(self):
        '''
            Return the live feed image reference. This is to setup writing to this reference.
            @return liveFeedImageRef: the live feed image reference
        '''
        securityCameraReference = self.get_security_camera_ref()
        liveFeedImageRef = securityCameraReference.child("liveFeedImage")
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
