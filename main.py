# Surpress extraneous TF messages
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
    liveFeedSize = (configFile["LiveFeedImageHeight"], configFile["LiveFeedImageWidth"])
    QRCode = configFile["QRCode"]

    return modelName, serviceAccountFile, liveFeedSize, QRCode

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
    modelName, serviceAccountFile, liveFeedSize, QRCode = setup()
    
    faceDetection = FaceDetection(modelName, serviceAccountFile)
    liveFeed = LiveFeed(liveFeedSize, serviceAccountFile, QRCode)

    # Start Face Detection
    start_thread(faceDetection.run)

    # Start Live Feed
    start_thread(liveFeed.run)

    print_done()
    while(True):
        time.sleep(1)



if __name__ == "__main__":
    run()
