# Surpress extraneous TF messages
print("Configuration Starting.")
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' 

import threading
import json
import time

from Camera import CameraInterface
from Firebase import FirebaseInterface
    
from LiveFeed import LiveFeed
from FaceDetection import FaceDetection

def start_thread(function):
    thr = threading.Thread(target=function)
    thr.daemon = True
    thr.start()
    return thr

def read_config_file():
    with open('config.json') as jsonFile:
        configFile = json.load(jsonFile)

    return configFile

def setup():
    configFile = read_config_file()

    modelName = configFile["modelName"]
    serviceAccountFile = configFile["serviceAccountFile"]
    liveFeedSize = (configFile["LiveFeedImageWidth"], configFile["LiveFeedImageHeight"])
    QRCode = configFile["QRCode"]
    MLImageSize = (configFile["MLImageWidth"], configFile["MLImageHeight"])
    PartitionSize = (configFile["PartitionWidth"], configFile["PartitionHeight"])
    PartitionImageWidthDelta = configFile["PartitionImageWidthDelta"]
    PartitionImageHieghtDelta = configFile["PartitionImageHieghtDelta"]


    return modelName, serviceAccountFile, liveFeedSize, QRCode, MLImageSize, \
        PartitionImageWidthDelta, PartitionImageHieghtDelta, PartitionSize

def print_done():
    print("")
    print("")
    print("========================")
    print("************************")
    print("")
    print("All Threads Started!!!")
    print("")
    print("************************")
    print("========================")
    print("")
    print("")

def run():
    modelName, serviceAccountFile, liveFeedSize, QRCode, MLImageSize, \
        PartitionImageWidthDelta, PartitionImageHieghtDelta, PartitionSize = setup()

    firebaseConnection = FirebaseInterface(serviceAccountFile)
    securityCameraReference = firebaseConnection.get_security_camera_ref(QRCode)

    if not firebaseConnection.is_registered(securityCameraReference):
        print("Camera is not yet registered. To register camera please scan the camera's QR code from your mobile app.")
        exit()
    
    faceDetection = FaceDetection(modelName, MLImageSize, \
        PartitionImageWidthDelta, PartitionImageHieghtDelta, PartitionSize, securityCameraReference)
    liveFeed = LiveFeed(liveFeedSize, securityCameraReference)

    print("Configuration Successfully Completed.")
    
    # Start Face Detection
    start_thread(faceDetection.run)

    # Start Live Feed
    start_thread(liveFeed.run)

    print_done()
    while(True):
        time.sleep(1)



if __name__ == "__main__":
    run()
