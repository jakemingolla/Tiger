import tornado.ioloop
import tornado.web
import os

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Luke Hanley lives at 65 Bromfield Rd Somerville MA 02144.")

def initializeApplication():
    return tornado.web.Application([
        (r"/", MainHandler)
    ])

if __name__ == "__main__":
    app = initializeApplication()
    port = int(os.environ.get("PORT", 5000))
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
