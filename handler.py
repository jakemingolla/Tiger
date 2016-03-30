from PIL import Image

STEP_SIZE = 4

def main():
    img = Image.open('starry.jpg')

    width, height = img.size
    print (width, height)

    for row in range(0, width, STEP_SIZE):
        for col in range(0, height, STEP_SIZE):
            pixelate(img, row, col)

    img.save('out.jpg')

def pixelate(img, row, col):
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

if __name__ == "__main__":
    main()
