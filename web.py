import tornado.ioloop
import tornado.web
import os

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("views/index.html")

def initializeApplication():
    return tornado.web.Application([
        (r"/", IndexHandler)
    ])

if __name__ == "__main__":
    app = initializeApplication()
    port = int(os.environ.get("PORT", 5000))
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
