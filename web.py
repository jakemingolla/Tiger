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
from PIL import ImageEnhance
from PIL import ImageOps
import io
import math

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
        if (f == None):
            return None
        f_name = f['filename']
        extension = os.path.splitext(f_name)[1].lower()

        if extension in valid_extensions: 
            f_body = f['body']
            return Image.open(StringIO.StringIO(f_body))
        else:
            return None

    def writeImage(self, img, quality):
        o = io.BytesIO()
        img.save(o, format="JPEG", quality=quality)
        s = o.getvalue()
        self.set_header('Content-type', 'image/jpg')
        self.set_header('Content-lengh', len(s))
        self.write(s)

class CompressHandler(ImageHandler):
    def post(self):
        try:
            img = self.getImageFromRequest()

            contrast   = float(self.get_argument("contrast", ""))
            sharpness  = float(self.get_argument("sharpness", ""))
            channels   = int(self.get_argument("channels", ""))
            probability = float(self.get_argument("probability", ""))
            threshold = int(self.get_argument("threshold", ""))

            img = self.compress(img, contrast, sharpness, channels, probability, threshold)

            self.writeImage(img, 0)

        except Exception as e:
            print e
            self.render("views/invalid.html")

    def get(self):
        self.render("views/compress.html")

    def compress(self, img, contrast, sharpness, channels, probability, threshold):
        converter = ImageEnhance.Contrast(img)
        img = converter.enhance(contrast)

        converter = ImageEnhance.Sharpness(img)
        img = converter.enhance(sharpness)

        img = ImageOps.posterize(img, channels)

        width, height = img.size


        for row in range(0, width):
            for col in range(0, height):
                if (random.random() < probability):
                    pixel = img.getpixel((row, col))

                    r = pixel[0]
                    g = pixel[1]
                    b = pixel[2]

                    if (r > threshold or g > threshold or b > threshold):
                        img.putpixel((row, col), (255 - r, 255 - g, 255 - b))

        return img

class PixelateHandler(ImageHandler):
    def post(self):
        try:
            img = self.getImageFromRequest()
            block_size = int(self.get_argument('blocksize', ''))
            self.pixelate(img, block_size)
            self.writeImage(img, 100)

        except Exception as e:
            self.render("views/invalid.html")

    def get(self):
        self.render("views/pixelate.html")

    def pixelate(self, img, block_size):
        width, height = img.size
        
        for row in range(0, width, block_size):
            for col in range(0, height, block_size):
                self.handle_block(img, row, col, block_size)

    def handle_block(self, img, row, col, block_size):
        r = 0
        g = 0
        b = 0

        for i in range(0, block_size):
            for j in range(0, block_size):
                try:
                    pixel = img.getpixel((row + i, col + j))
                    r += pixel[0]
                    g += pixel[1]
                    b += pixel[2]

                except IndexError:
                    pass

        count = block_size * block_size
        r /= count
        g /= count
        b /= count

        for i in range(0, block_size):
            for j in range(0, block_size):
                try:
                    img.putpixel((row + i, col + j), (r, g, b))
                except IndexError:
                    pass
           

def initializeApplication():
    return tornado.web.Application([
        (r"/", IndexHandler),
        (r"/pixelate", PixelateHandler),
        (r"/compress", CompressHandler)
    ])

if __name__ == "__main__":
    app = initializeApplication()
    port = int(os.environ.get("PORT", 5000))
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
