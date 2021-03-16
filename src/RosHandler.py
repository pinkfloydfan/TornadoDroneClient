import roslibpy

class RosHandler:

    def __init__(self): 
        ros = roslibpy.Ros(host="localhost", port = 9090)
        ros.run()