#from scipy import rot
import datetime

#visualization
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Controller:
    def __init__(self):

        self.previousTime = datetime.datetime.now()

        self.previousPosition = [0,0,0]
        self.previousOrientation = [0,0,0,1] #x, y, z, w quaternion

        self.velocityX = 0
        self.velocityY = 0
        self.velocityZ = 0

        self.vxhist = [0]
        self.vyhist = [0]
        self.vzhist = [0]

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



    
    def processIMUMessage(self, msg):

        print("Placeholder")

