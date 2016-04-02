# Jake Mingolla
# March - April, 2016
#
# Pixl
#
# Created for Luke Hanley, this service is designed to easily manipulate
# images at the pixel level to create distorted images.

import tornado.ioloop
import tornado.web
import os
import random
import string
from mako.template import Template
import StringIO
from PIL import Image
import io

valid_extensions = [
    '.jpg',
    '.jpeg',
    '.png'
]

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("views/index.html")

class ImageHandler(tornado.web.RequestHandler):
    def getImageFromRequest(self):
        f = self.request.files['file'][0]
        f_name = f['filename']
        extension = os.path.splitext(f_name)[1].lower()

        if extension in valid_extensions: 
            f_body = f['body']
            return Image.open(StringIO.StringIO(f_body))
        else:
            return None

    def writeImage(self, img):
        o = io.BytesIO()
        img.save(o, format="JPEG")
        s = o.getvalue()
        self.set_header('Content-type', 'image/jpg')
        self.set_header('Content-lengh', len(s))
        self.write(s)


class PixelateHandler(ImageHandler):
    def post(self):
        try:
            img = self.getImageFromRequest()
            if img == None:
                self.render("views/invalid.html")
                return 
            self.pixelate(img)
            self.writeImage(img)

        except Exception as e:
            self.write(str(e))

    def pixelate(self, img):
        width, height = img.size
        STEP_SIZE = 10
        
        for row in range(0, width, STEP_SIZE):
            for col in range(0, height, STEP_SIZE):
                self.handle_block(img, row, col, STEP_SIZE)

    def handle_block(self, img, row, col, STEP_SIZE):
        r = 0
        g = 0
        b = 0

        for i in range(0, STEP_SIZE):
            for j in range(0, STEP_SIZE):
                try:
                    pixel = img.getpixel((row + i, col + j))
                    r += pixel[0]
                    g += pixel[1]
                    b += pixel[2]

                except IndexError:
                    pass

        count = STEP_SIZE * STEP_SIZE
        r /= count
        g /= count
        b /= count

        for i in range(0, STEP_SIZE):
            for j in range(0, STEP_SIZE):
                try:
                    img.putpixel((row + i, col + j), (r, g, b))
                except IndexError:
                    pass
           

def initializeApplication():
    return tornado.web.Application([
        (r"/", IndexHandler),
        (r"/pixelate", PixelateHandler)
    ])

if __name__ == "__main__":
    app = initializeApplication()
    port = int(os.environ.get("PORT", 5000))
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
