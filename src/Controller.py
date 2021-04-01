from 

class Controller:
    def __init__(self):

        self.previousTime = datetime.datetime.now()

        self.previousPosition = [0,0,0]
        self.previousOrientation = [0,0,0,1] #x, y, z, w quaternion

        self.velocityX = 0
        self.velocityY = 0
        self.velocityZ = 0



    def processSlamMessage(msg):

        currentPosition = message["pose"]["position"]
        currentOrientation = message["pose"]["orientation"]



    
    def processIMUMessage(msg):

