
import roslibpy
import cv2
import numpy as np
import base64

from cv_bridge import CvBridge
from Controller import Controller

# class in charge of RosLibPy and parsing/sending ROS messages
class RosHandler():


    def __init__(self, parentRef): 

        self.joystickMessage = [0,0,0,0,0,0,0,0]

        self.parentRef = parentRef

        self.ioloop = parentRef.ioloop

        self.controller = Controller()
        
        self.client = roslibpy.Ros(host="localhost", port = 9090)
        self.client.on_ready(lambda: print('Is ROS connected?', self.client.is_connected))
        self.client.run()
        self.bridge = CvBridge()


        
        self.imagePublisher = roslibpy.Topic(self.client, '/camera/image_compressed/compressed', 'sensor_msgs/CompressedImage')
        self.imagePublisher.advertise()

        self.joyListener = roslibpy.Topic(self.client, '/joy', 'sensor_msgs/Joy')
        self.joyListener.subscribe(lambda message: self.handleJoystickMessage(message))
    
        self.poseListener = roslibpy.Topic(self.client, '/orb_slam2_mono/pose', 'geometry_msgs/PoseStamped')
        self.poseListener.subscribe(lambda message: self.handlePoseMessage(message))

        
        self.showRawCapture = True

        self.armed = False

    def handlePoseMessage(self, message):

        self.controller.processPoseMessage(message)

    def handleJoystickMessage(self, message):
        self.joystickMessage = message["axes"]

    

    def handleImageMessage(self, img):
        #imageMessage = self.convertFromimgaxis_camera(img)

        nparr = np.frombuffer(img, np.uint8)

        b64encoded = base64.b64encode(nparr).decode('ascii')


        if self.showRawCapture == True:
            img = cv2.imdecode(nparr, flags=cv2.IMREAD_GRAYSCALE)
            cv2.imshow("yes", img)
            cv2.waitKey(1)

        rosImg = dict(format='jpeg', data = b64encoded)

        #imageMessage = self.bridge.cv2_to_rosImg(img, encoding = "passthrough")

        self.imagePublisher.publish(rosImg)

    def handleAttitudeMessage(self, msg):

        attitudeList = msg.split(',');

        roll  = attitudeList[0]
        pitch = attitudeList[1]
        yaw   = attitudeList[2]
        
        '''
        print("roll: " + roll)
        print("pitch: " + pitch)
        print("yaw: " + yaw)
        '''