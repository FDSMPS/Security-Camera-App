from Camera import CameraInterface
from Firebase import FirebaseInterface
from ImageProcessor import ImageProcessor
import time
# import base64
# import io
# from PIL import Image

class LiveFeed():
    def run(self):
        if self.firebase.is_registered(self.QRCode):

            liveFeedImageRef = self.firebase.get_live_feed_image_ref(self.QRCode)

            while True:
                print("Transmitting Live Feed")
                img = self.camera.get_image_from_camera()
                img = ImageProcessor.resizeImage(img, self.size)
                imgString = str(ImageProcessor.convertImageToString(img), encoding='utf-8')
                self.firebase.update_live_feed(liveFeedImageRef, imgString)
                # Commented code demonstrates how to convert a string back into an image
                # msg = base64.b64decode(bytes(imgString, encoding='utf-8'))
                # buf = io.BytesIO(msg)
                # img = Image.open(buf)
                # img.show()


    def __init__(self, liveFeedSize, serviceAccountFile, QRCode):
        self.camera = CameraInterface()
        self.firebase = FirebaseInterface(serviceAccountFile)
        self.size = liveFeedSize
        self.QRCode = QRCode