from PIL import Image
from PIL import ImageTk

import math

import numpy as np

def emptyimage(x, y):
    return ImageTk.PhotoImage(Image.new("RGB", (x, y), (255, 255, 255)))

def readpng(path):
    im = Image.open(path)
    pixels = list(im.getdata())
    pixels = [[int(value/1.05) for value in element[:3]] for element in pixels]
    width, height = im.size
    return [[pixels[i * width:(i + 1) * width] for i in range(height)]]

def savepng(path, rgb, name):
    rgbarray = []
    rgbarray = np.array([np.array([[x[0], x[1], x[2]] for x in i], np.uint8) for i in rgb[0]], np.uint8)
    rgbimage = Image.fromarray(rgbarray, "RGB")
    
    if len(rgb) == 2:
        rgbaarray = np.array([np.array([x for x in i], np.uint8) for i in rgb[1]], np.uint8)
        rgbaimage = Image.fromarray(rgbaarray, "L")
        rgbimage.putalpha(rgbaimage)
        
    rgbimage.save(path+f"/{name}.png")

def get2power(num):
    return 2**math.floor(math.log(num)/math.log(2))

def clamp(texture): # Clamps to a 2**x
    x = len(texture[0][0])
    y = len(texture[0])
    xnew = get2power(x)
    ynew = get2power(y)
    return [[[[texture[0][row][pixel][color] for color in range(3)] for pixel in range(xnew)] for row in range(ynew)]]
