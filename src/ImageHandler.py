import cv2
import base64
import numpy as np

# class that builds an image from a blob
class ImageHandler: 
    def convertFromBlob(self, blob):
        nparr = np.frombuffer(blob, np.uint8)

        img = cv2.imdecode(nparr, flags=cv2.IMREAD_COLOR)

        cv2.imshow("yes", img)
        cv2.waitKey(1)

        return img

