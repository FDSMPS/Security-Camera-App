from PIL import Image
import base64
import io
import numpy as np

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
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        return img_str

    @staticmethod
    def convertStringToImage(imgString):
        msg = base64.b64decode(bytes(imgString, encoding='utf-8'))
        buf = io.BytesIO(msg)
        img = Image.open(buf)

    @staticmethod
    def partitionImage(img, destinationSize, widthDelta, heightDelta, PartitionSize):
        width, height = img.size
        
        partitionWidth, partitionHeight = PartitionSize
        destinationWidth, destinationHeight = destinationSize

        if (partitionWidth > width) or (destinationWidth > width):
            raise Exception("width of image is smaller than partition or destination width")

        if (partitionHeight > height) or (destinationHeight > height):
            raise Exception("height of image is smaller than partition or destination height")


        images = []
        for y in range(0, height - partitionHeight + 1, heightDelta):
            for x in range(0, width - partitionWidth + 1, widthDelta):
                box = (x, y, x + partitionWidth, y + partitionHeight)
                cropped = img.crop(box)
                resized = cropped.resize((destinationWidth,destinationHeight))
                images.append(np.array(resized))
        return images

    def __init__(self):
        pass

# img = Image.open("mockImages/82446133_186948319118808_5283585445173657600_n.jpg")
# images = ImageProcessor.partitionImage(img, (250,250), 300, 300, (500,500))

# print(np.array(images).shape)
# for i in images:
#     img = Image.fromarray(i)
#     img.show()