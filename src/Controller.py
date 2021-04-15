from scipy.spatial.transform import Rotation as R
import datetime


class Controller:
    def __init__(self):

        self.previousTime = datetime.datetime.now()

        self.previousPosition = [0,0,0]
        self.previousOrientation = [0,0,0,1] #x, y, z, w quaternion

        self.velocityX = 0
        self.velocityY = 0
        self.velocityZ = 0

        self.time = [0]


    def processPoseMessage(self, msg, callback):

        currentPosition = msg["pose"]["position"]
        currentOrientation = msg["pose"]["orientation"]

        currentTime = datetime.datetime.now()

        dt = ((currentTime - self.previousTime).microseconds/1e6)

        vx = (currentPosition["x"] - self.previousPosition[0])/dt
        vy = (currentPosition["y"] - self.previousPosition[1])/dt
        vz = (currentPosition["z"] - self.previousPosition[2])/dt


        self.previousPosition = [currentPosition["x"], currentPosition["y"], currentPosition["z"]]
        self.previousTime = currentTime

        #print("vx: " + str(vx) + ", " + "vy: " + str(vy) + ", " + "vz: " + str(vz))

        returnArr = [vx,vy,vz]

        callback(returnArr)

    def processIMUMessage(self, msg, callback):


        r = R.from_euler('xyz', [msg[0], msg[1], msg[2]], degrees = True)
        orientation = r.as_quat()

        acceleration = [msg[3], msg[4], msg[5]]

        angularVelocity = [msg[6], msg[7], msg[8]]

        timestamp = msg[9]

        isImageFrame = msg[10]

        if isImageFrame == 0:
            callback(orientation, acceleration, angularVelocity, timestamp, False, 0)
        else:
            callback(orientation, acceleration, angularVelocity, timestamp, True, isImageFrame)

        




        #print("Placeholder")

