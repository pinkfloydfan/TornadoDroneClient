
import roslibpy
import cv2
import numpy as np
import base64

import datetime

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

        self.velocityPublisher = roslibpy.Topic(self.client, '/minion/velocity', 'std_msgs/Float32MultiArray')
        self.velocityPublisher.advertise()

        self.imuPublisher = roslibpy.Topic(self.client, '/imu', 'sensor_msgs/Imu')
        self.imuPublisher.advertise()

        self.imagePublisher = roslibpy.Topic(self.client, '/camera/image_compressed/compressed', 'sensor_msgs/CompressedImage')
        self.imagePublisher.advertise()

        self.joyListener = roslibpy.Topic(self.client, '/joy', 'sensor_msgs/Joy')
        self.joyListener.subscribe(lambda message: self.handleJoystickMessage(message))
    
        self.poseListener = roslibpy.Topic(self.client, '/Mono_Inertial/orb_pose', 'geometry_msgs/PoseStamped')
        self.poseListener.subscribe(lambda message: self.handlePoseMessage(message))

        
        self.showRawCapture = True

        self.armed = False

    def handlePoseMessage(self, message):

        self.controller.processPoseMessage(message, self.publishVelocityCallback)

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

        try: 
            #rosImg = dict(format='jpeg', data = b64encoded)

            rosImg = {
                #"header" : {
                    #"stamp" : roslibpy.Time.now()
                #},
                "format" : "jpeg",
                "data" : b64encoded 
            }
            #print("publishing image")
            self.imagePublisher.publish(rosImg)
        except:
            print("Failed to parse image")
            return


        #imageMessage = self.bridge.cv2_to_rosImg(img, encoding = "passthrough")


    def handleAttitudeMessage(self, msg):

        #betaflight is north - west - up

        attitudeList = msg.split(',')

        self.controller.processIMUMessage(attitudeList, self.publishIMUCallback)


    def publishVelocityCallback(self, velocity):
        return

        #self.velocityPublisher.publish(roslibpy.Message({"data":velocity}))

    
    def publishIMUCallback(self, orientation, acceleration, angularVelocity):

        imuMessage = {
            #"header" : {
                #"stamp" : roslibpy.Time.now()
            #},

            "orientation": {
                "x": orientation[0],
                "y": orientation[1],
                "z": orientation[2],
                "w": orientation[3]
            },
            "orientation_covariance": [-1, 0, 0, 0, 0, 0, 0, 0, 0],
            "linear_acceleration": {
                "x": acceleration[0],
                "y": acceleration[1],
                "z": acceleration[2]
            },
            "linear_acceleration_covariance": [-1, 0, 0, 0, 0, 0, 0, 0, 0],
            "angular_velocity" : {
                "x": angularVelocity[0]/10,
                "y": angularVelocity[1]/10,
                "z": angularVelocity[2]/10
            },
            "angular_velocity_covariance": [-1, 0, 0, 0, 0, 0, 0, 0, 0]
        }

        #print(imuMessage)

        self.imuPublisher.publish(imuMessage)