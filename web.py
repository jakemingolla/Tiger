import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello world!")

def initializeApplication():
    return tornado.web.Application([
        (r"/", MainHandler)
    ])

if __name__ == "__main__":
    app = initializeApplication()
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()
