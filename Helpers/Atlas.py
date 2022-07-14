import math
import Helpers.ImageTools as ImageTools

def getatlassize(textureamount):
    return math.ceil(math.sqrt(textureamount))

def fixuvs(uvs, atlassize):
    x = 0
    y = 0
    newuvs = []
    for texture in uvs:
        if x >= atlassize:
            x = 0
            y += 1

        for uv in texture:
            newuvs.append([(uv[0]+x)/atlassize, (uv[1]+y)/atlassize])

        x += 1
        
    return newuvs


def stitch(textures, atlassize):
    sizex = len(textures[0][0])
    sizey = len(textures[0])
    atlas = ImageTools.generateimage(sizex*atlassize, sizey*atlassize)

    x = 0
    y = atlassize-1
    for texture in textures:
        if x >= atlassize:
            x = 0
            y -= 1 # This -= is to make the textures get pasted bottom up, not top down.

        xcor = x*sizex
        ycor = y*sizey
        atlas = ImageTools.pastetexture(atlas, texture, xcor, ycor)
        
        x += 1

    return atlas