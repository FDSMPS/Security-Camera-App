from PIL import Image
import base64
from io import BytesIO

class ImageProcessor():

    @staticmethod
    def resizeImage(img, size):

        sizeRatio = size[0]/size[1]
        width = img.size[0]
        height = img.size[1]

        if (width / height) != (size[0]/size[1]):
            possibleNewHeight = round(width / sizeRatio)
            possibleNewWidth = round(height * sizeRatio)

            if possibleNewHeight > height:
                offset = (width - possibleNewWidth)/2
                img = img.crop((offset, 0, possibleNewWidth + offset, height))
            else:
                offset = (height - possibleNewHeight)/2
                img = img.crop((0, offset, width, possibleNewHeight + offset))

        return img.resize(size)

    @staticmethod
    def convertImageToString(img):
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        return img_str

    def __init__(self):
        pass