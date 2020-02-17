'''
    Creation Date: Feb 3, 2020
    Author: Tymoore Jamal
    Content: This file contains the Image Processor class which handles processing images.
'''

from PIL import Image
import base64
import io
import numpy as np

class ImageProcessor():
    '''
        This is a static class which deals with processing images.
    '''

    @staticmethod
    def resizeImage(img, size):
        '''
            Resize an image without stretching it.
            @param img: the image to resize
            @param size: the size to resize the image to
            @return: the resized image
        '''
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
        '''
            This method converts an image to a string.
            @param img: the image to convert
            @return img_str: the converted image as a base 64 string
        '''
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_str = str(base64.b64encode(buffered.getvalue()), encoding='utf-8')
        return img_str

    @staticmethod
    def convertStringToImage(imgString):
        '''
            This method converts a string into an image.
            @param imgString: an image stored as a string
            @return img: the image
        '''
        msg = base64.b64decode(bytes(imgString, encoding='utf-8'))
        buf = io.BytesIO(msg)
        img = Image.open(buf)
        return img

    @staticmethod
    def partitionImage(img, destinationSize, widthDelta, heightDelta, PartitionSize):
        '''
            Partitions an image into multiple smaller images.
            @param img: the image to partition
            @distimationSize: the destination size of each image
            @widthDelta: the width delta between each partition
            @heightDelta: the height delta between each partition
            @partitionSize: the partition size
            @return images: a list of images
        '''
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
