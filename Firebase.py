import threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class FirebaseInterface():
    lock = threading.Lock()
    instancesMade = 0

    def sendNotification(self):
        pass

    def __init__(self, serviceAccountFile = None):
        
        if (serviceAccountFile is None) and (FirebaseInterface.instancesMade == 0):
            raise Exception("Service Account File not provided to first firebase instance. Connection unable to be made.")
        
        FirebaseInterface.instancesMade += 1

        if FirebaseInterface.instancesMade == 1:
            self.connect_to_firebase(serviceAccountFile)

        self.root = db.reference()
    
    
    def connect_to_firebase(self, serviceAccountFile):
        # FirebaseInterface.lock.acquire()

        cred = credentials.Certificate(serviceAccountFile)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://fdsmps-android.firebaseio.com/'
        })

        # FirebaseInterface.lock.release()
    
    def get_data(self, ref = None):

        if ref == None:
            ref = self.root

        # FirebaseInterface.lock.acquire()
        result = ref.get()
        # FirebaseInterface.lock.release()

        return ref.get()

    def get_security_camera_ref(self, QRCode):
        return self.root.child("SecurityCameras").child(QRCode)

    def is_registered(self, securityCameraReference):
        registeredRef = securityCameraReference.child('registered')
        registered = self.get_data(registeredRef)
        return registered

    def get_live_feed_image_ref(self, securityCameraReference):
        liveFeedImageRef = securityCameraReference.child("currentImage")
        return liveFeedImageRef

    def update_live_feed(self, liveFeedImageRef, imageString):
        return self.set_data(liveFeedImageRef, imageString)

    def set_data(self, ref, data):
        # FirebaseInterface.lock.acquire()
        result = ref.set(data)
        # FirebaseInterface.lock.release()

        return result
