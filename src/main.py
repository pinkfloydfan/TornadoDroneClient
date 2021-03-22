

#ws://192.168.4.22:80
import tornado
from tornado import httpserver, httpclient, ioloop, web, websocket, gen
from tornado.ioloop import PeriodicCallback
from tornado.websocket import websocket_connect
from tornado.ioloop import IOLoop, PeriodicCallback

from tornado.platform.asyncio import asyncio

from tornado.platform.asyncio import AnyThreadEventLoopPolicy
asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())

import numpy as np



#from ImageHandler import ImageHandler
from RosHandler import RosHandler



class MainHandler(tornado.websocket.WebSocketHandler):
    def get(self):
        self.write("Hello, world")


class Client(tornado.websocket.WebSocketHandler):
    def __init__(self, url, timeout):

        self.url = url
        self.timeout = timeout
        self.ioloop = IOLoop.instance()
        self.ws = None
        self.rosHandler = RosHandler(self)
        self.connect()
        PeriodicCallback(self.keep_alive, 20000).start()
        PeriodicCallback(self.getJoystickCommands, 200).start()
        self.ioloop.start()
        self.ioloop.make_current()

    @gen.coroutine
    def connect(self):
        print ("trying to connect to aircraft...")
        try:
            self.ws = yield websocket_connect(self.url)
        except Exception:
            print(Exception)
        else:
            print ("connected")
            self.run()

    @gen.coroutine
    def run(self):
        
        while True:
            #MARK: improve 
            msg = yield self.ws.read_message()
            if msg is None:
                print ("connection closed")
                self.ws = None
                break
            self.rosHandler.handleImageBlob(msg)
            

    def keep_alive(self):
        if self.ws is None:
            self.connect()
        else:
            self.ws.write_message("keep alive")

    def getJoystickCommands(self):
        axes = self.rosHandler.joystickMessage
        lst = [int(-x*500) + 1500 for x in axes]
        strs = [str(i) for i in lst]

        msg = ",".join(strs)
        
        print(msg)
        self.ws.write_message(msg)


    
    '''
    @gen.coroutine
    def test(self, message):
        axes = message["axes"]

        lst = [int(x*500) + 1500 for x in axes]
        strs = [str(i) for i in lst]

        msg = ",".join(strs)
        
        self.ws.write_message(msg)
    '''



def make_app():
    return tornado.web.Application([
        (r"/", Client),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(3000)
    
    client = Client("ws://192.168.4.22:80", 5)

  