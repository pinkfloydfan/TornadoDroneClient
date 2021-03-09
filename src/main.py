#ws://192.168.4.22:80
import tornado
from tornado import httpserver, httpclient, ioloop, web, websocket, gen
from tornado.ioloop import PeriodicCallback
from tornado.websocket import websocket_connect
from tornado.ioloop import IOLoop, PeriodicCallback



import websockets
import asyncio



class MainHandler(tornado.websocket.WebSocketHandler):
    def get(self):
        self.write("Hello, world")

    

class Cheese():

    def __init__(self):
        self.hello()


    async def hello(self):
        print("trying to connect")
        url = "ws://localhost:3001"
        conn = await websocket_connect(url)
        while True:
            msg = yield conn.read_message()
            if msg is None: break
    # Do something with msg
    # Do something with msg

# Note to self - don't subclass websockethandler
class Client(object):
    def __init__(self, url, timeout):
        self.url = url
        self.timeout = timeout
        self.ioloop = IOLoop.instance()
        self.ws = None
        self.connect()
        PeriodicCallback(self.keep_alive, 20000).start()
        self.ioloop.start()

    @gen.coroutine
    def connect(self):
        print ("trying to connect")
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
            msg = yield self.ws.read_message()
            if msg is None:
                print ("connection closed")
                self.ws = None
                break
            print(msg)

    def keep_alive(self):
        if self.ws is None:
            self.connect()
        else:
            self.ws.write_message("keep alive")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(3000)
    client = Client("ws://192.168.4.22:80", 5)

  