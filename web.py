import tornado.ioloop
import tornado.web
import os
import random
import string
from mako.template import Template

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("views/index.html")

class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            file1 = self.request.files['file1'][0]
            orig_filename = file1['filename']
            extension = os.path.splitext(orig_filename)[1]
            tmp_filename = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(12))
            final_filename = tmp_filename + extension

            output_file = open("uploads/" + final_filename, 'w')
            output_file.write(file1['body'])

            template = Template(filename="views/upload.html")
            self.write(template.render(filename=final_filename))


        except Exception as e:
            self.write(str(e))
            

def initializeApplication():
    return tornado.web.Application([
        (r"/", IndexHandler),
        (r"/upload", UploadHandler)
    ])

if __name__ == "__main__":
    app = initializeApplication()
    port = int(os.environ.get("PORT", 5000))
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
