'''
    Creation Date: Feb 3, 2020
    Author: Tymoore Jamal
    Content: This is the main file. It getting the cofiguation settings and starts both the 
        face detection and live feed threads.
'''

print("Configuration Starting.")
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' # Surpress uneeded TF info messages 

import threading
import json
import time

from Camera import CameraInterface
from Firebase import FirebaseInterface
    
from LiveFeed import LiveFeed
from FaceDetection import FaceDetection

def start_thread(function):
    '''
       Create a new thread and run the specified function. 
       @param function: the function to run in a new thread.
       @return: thr: the thread reference.
    '''
    thr = threading.Thread(target=function)
    thr.daemon = True
    thr.start()
    return thr

def read_config_file():
    '''
        Reads the JSON configuration file
        @return configFile: The JSON configuration file as an object.
    '''
    with open(os.join('..','config.json')) as jsonFile:
        configFile = json.load(jsonFile)

    return configFile

def print_threads_started():
    '''
        Prints a message that all threads have started.
    '''
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
    '''
        Runs the main function. Gets settings, determines if the camera is registered 
        and then starts all threads. Then begins an infinite loop so that the other threads keep running.
    '''
    settings = read_config_file()

    firebaseConnection = FirebaseInterface(settings)
    
    # If not registered exit
    if not firebaseConnection.is_registered():
        print("Camera is not yet registered. To register camera please scan the camera's QR code from your mobile app.")
        exit()
    
    faceDetection = FaceDetection(settings)

    liveFeed = LiveFeed(settings)

    print("Configuration Successfully Completed.")
    
    # Start Face Detection
    start_thread(faceDetection.run)

    # Start Live Feed
    start_thread(liveFeed.run)

    print_threads_started()
    while(True):
        time.sleep(settings["OneSecondDelay"])



if __name__ == "__main__":
    run()
