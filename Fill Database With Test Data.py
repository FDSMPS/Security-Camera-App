import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from os.path import join
from PIL import Image
import base64
from io import BytesIO
from datetime import datetime

sure = input("are you sure? all data will be deleted\n")

if sure != "y":
    print("Aborting")
    exit()
    print('Done aborting')

serviceAccountFile = join( "..", "firebase", "fdsmps-android-firebase-adminsdk-2wplu-a5b2d0a50e.json")
try:
    cred = credentials.Certificate(serviceAccountFile)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://fdsmps-android.firebaseio.com/'
    })
except Exception as e:
    print(e)

root = db.reference()

root.set({})

root.set({
        'Users': 
            {
                'testUsername': {
                    'username': 'testUsername',
                    'email': 'test@test.com',
                    'userSetting': {
                        'location': {
                            'latitude': 55.537788,
                            'longitude': -117.011337
                        },
                        'enable': True,
                        'contacts': {
                            'billy': {
                                'name': 'billy',
                                'phoneNumber': '780-123-4567'
                            },
                            'bobby': {
                                'name': 'bobby',
                                'phoneNumber': '780-223-4567'
                            },
                        },
                        'QRCode': "123456"
                    },
                    'notifications':{
                        'qwerty': {
                            'datetime': '2020-01-15 15:42:00',
                            'notificationID': 'qwerty'
                        }
                    }
                }
            },
    'SecurityCameras':{
        "123456": {
                'currentImage': "basi21739sadvuias",
                'timestamp': '2020-01-16 15:42:00',
                'QRCode': "123456",
                'registered': True,
                "registeredUserName": "testUsername"
        }
    },
    'NotificationImages':{
        'qwerty':{
            'notificationID': "qwerty",
            'Image': "21ebo123b12ui3b12"
        }
    }
})