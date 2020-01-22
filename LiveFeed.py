from Camera import CameraInterface
from Firebase import FirebaseInterface
from ImageProcessor import ImageProcessor
import time

class LiveFeed():
    def run(self):
        liveFeedImageRef = self.firebase.get_live_feed_image_ref(self.securityCameraReference)

        while True:
            print("Transmitting Live Feed")
            img = self.camera.get_image_from_camera()
            img = ImageProcessor.resizeImage(img, self.size)
            imgString = str(ImageProcessor.convertImageToString(img), encoding='utf-8')
            self.firebase.update_live_feed(liveFeedImageRef, imgString)


    def __init__(self, liveFeedSize, securityCameraReference):
        self.camera = CameraInterface()
        self.size = liveFeedSize
        self.securityCameraReference = securityCameraReference
        self.firebase = FirebaseInterface()