#ws://192.168.4.22:80
import tornado
from tornado import httpserver, httpclient, ioloop, web, websocket, gen
from tornado.ioloop import PeriodicCallback
from tornado.websocket import websocket_connect


import websockets
import asyncio



class MainHandler(tornado.websocket.WebSocketHandler):
    def get(self):
        self.write("Hello, world")

    async def hello(self):
        uri = "ws://192.168.4.22:80"
        async with websockets.connect(uri) as websocket:

            msg = await websocket.recv()
            print(msg)





def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(3000)
    tornado.ioloop.IOLoop.current().start()

  