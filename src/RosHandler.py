
import roslibpy
import cv2
from cv_bridge import CvBridge
import numpy as np
import base64
import datetime

class RosHandler():


    def __init__(self, parentRef): 

        self.joystickMessage = [0,0,0,0,0,0,0,0]
        self.slamPosition = [0,0,0]
        self.slamOrientation = [0,0,0,1]

        self.parentRef = parentRef

        self.ioloop = parentRef.ioloop

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

        self.previousTime = datetime.datetime.now()
        
        self.showRawCapture = True

        self.armed = False

    def handlePoseMessage(self, message):

  

        
        self.slamPosition = message["pose"]["position"]
        self.slamOrientation = message["pose"]["orientation"] 

        newTime = datetime.datetime.now()

        delta_t = (newTime - self.previousTime).microseconds

        print(delta_t)

        self.previousTime = newTime

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

        roll  = msg[0]
        pitch = msg[1]
        yaw   = msg[2]

        print("roll: " + roll)
        print("pitch: " + pitch)
        print("yaw: " + yaw)