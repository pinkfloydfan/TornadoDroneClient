import roslibpy
import cv2
from cv_bridge import CvBridge
import numpy as np
import base64

class RosHandler:


    def __init__(self): 
        self.client = roslibpy.Ros(host="localhost", port = 9090)
        self.client.on_ready(lambda: print('Is ROS connected?', self.client.is_connected))
        self.client.run()
        self.bridge = CvBridge()
        
        self.publisher = roslibpy.Topic(self.client, '/camera/image_compressed', 'sensor_msgs/CompressedImage')
        self.publisher.advertise()

        self.showRawCapture = True

    def handleImageBlob(self, blob):
        #imageMessage = self.convertFromBlob(blob)

        nparr = np.frombuffer(blob, np.uint8)

        b64encoded = base64.b64encode(nparr).decode('ascii')


        if self.showRawCapture == True:
            img = cv2.imdecode(nparr, flags=cv2.IMREAD_GRAYSCALE)
            cv2.imshow("yes", img)
            cv2.waitKey(1)

        imgmsg = dict(format='jpeg', data = b64encoded)
        print(imgmsg)

        #imageMessage = self.bridge.cv2_to_imgmsg(img, encoding = "passthrough")

        self.publisher.publish(imgmsg)

'''
    def convertFromBlob(self, blob):
        nparr = np.frombuffer(blob, np.uint8)

    
        img = cv2.imdecode(nparr, flags=cv2.IMREAD_GRAYSCALE)

        if self.showRawCapture == True:
            cv2.imshow("yes", img)
            cv2.waitKey(1)

        imageMessage = self.bridge.cv2_to_imgmsg(img, encoding = "passthrough")
        return imageMessage

'''