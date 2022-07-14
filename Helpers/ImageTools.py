
def generateimage(x, y):
    return [[[0, 0, 0] for pixel in range(x)] for row in range(y)]

def pastetexture(texture1, texture2, xcor, ycor):
    sizex = len(texture2[0])
    sizey = len(texture2)
    for y in range(sizey):
        for x in range(sizex):
            texture1[y+ycor][x+xcor] = texture2[y][x]
    return texture1

def resizeindex(len1, len2, index):
    return round((len1/len2) * (index+1) - 1)

def resize(texture, sizex, sizey):
    newtexture = generateimage(sizex, sizey)

    for y, row in enumerate(newtexture):
        for x, pixel in enumerate(row):
            oldy = resizeindex(len(texture), sizey, y)
            oldx = resizeindex(len(texture[0]), sizex, x)
            newtexture[y][x] = texture[oldy][oldx]

    return newtexture

def getbiggestsize(textures):
    biggestsizex = 0
    biggestsizey = 0
    for texture in textures:
        if len(texture) > biggestsizey:
            biggestsizey = len(texture)
            
        if len(texture[0]) > biggestsizex:
            biggestsizex = len(texture[0])

    return biggestsizex, biggestsizey