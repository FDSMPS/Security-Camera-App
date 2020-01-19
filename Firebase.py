import threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class FirebaseInterface():
    lock = threading.Lock()
    instancesMade = 0
    connection = None

    def __init__(self, serviceAccountFile):
        FirebaseInterface.instancesMade += 1

        if FirebaseInterface.instancesMade == 1:
            FirebaseInterface.connection = self.connect_to_firebase(serviceAccountFile)

        self.root = db.reference()
    
    
    def connect_to_firebase(self, serviceAccountFile):
        FirebaseInterface.lock.acquire()

        cred = credentials.Certificate(serviceAccountFile)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://fdsmps-android.firebaseio.com/'
        })

        FirebaseInterface.lock.release()
    
    def get_data(self, ref = None):

        if ref == None:
            ref = self.root

        FirebaseInterface.lock.acquire()
        result = ref.get()
        FirebaseInterface.lock.release()

        return ref.get()

    def set_data(self, ref, data):
        FirebaseInterface.lock.acquire()
        result = ref.set(data)
        FirebaseInterface.lock.release()

        return result