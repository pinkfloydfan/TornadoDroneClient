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


        r = R.from_euler('xyz', [float(msg[0])/10, float(msg[1])/10, msg[2]], degrees = True)
        orientation = r.as_quat()

        acceleration = [float(msg[3])*0.02, float(msg[4])*0.02, float(msg[5])*0.02]

        angularVelocity = [float(msg[6]), float(msg[7]), float(msg[8])]

        callback(orientation, acceleration, angularVelocity)




        #print("Placeholder")

