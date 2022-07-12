import math

def rgb565(color):
    return (color >> 11 << 3 & 0xff, color >> 5 << 2 & 0xff, color >> 0 << 3 & 0xff)

def rgb888_to_rgb565(color):
    if interpolate == 1:
        return ((int((color[0]**2)/256) >> 3 << 11) + (int((color[1]**2)/256) >> 2 << 5) + (int((color[2]**2)/256) >> 3)).to_bytes(2, byteorder="big")
    return ((color[0] >> 3 << 11) + (color[1] >> 2 << 5) + (color[2] >> 3)).to_bytes(2, byteorder="big")


def vdiff(vector1, vector2):
    return (abs(vector1[0] - vector2[0]) + abs(vector1[1] - vector2[1]) + abs(vector1[2] - vector2[2]))/(765)

def vmul(vector1, factor):
    return (int(vector1[0] * factor), int(vector1[1] * factor), int(vector1[2] * factor))

def vadd(vector1, vector2):
    return (vector1[0] + vector2[0], vector1[1] + vector2[1], vector1[2] + vector2[2])

def tpl_compress(images):
    
    for image_o in images:
        bytecode = b""
        image = [image_o[-1-row] for row in range(len(image_o))]
        while len(image) > 4:
            sizey = len(image)
            sizex = len(image[0])
            for ycblock in range(int(sizey/8)):
                for xcblock in range(int(sizex/8)):
                    for yblock in range(2):
                        for xblock in range(2):        
                            
                            high_diff = 1
                            high = (0, 0, 0)
                            
                            low_diff = 1
                            low = (255, 255, 255)
                            for y in range(4):
                                for x in range(4):
                                    curr_pixel = image[(ycblock*8 + yblock*4 + y)][xcblock*8 + xblock*4 + x]
                                    diff = vdiff(curr_pixel, (255, 255, 255))
                                    
                                    if diff < high_diff:
                                        high_diff = diff
                                        high = curr_pixel
                                    
                                    diff = vdiff(curr_pixel, (0, 0, 0))
                                    
                                    if diff < low_diff:
                                        low_diff = diff
                                        low = curr_pixel
                            
                            
                            if rgb888_to_rgb565(low) < rgb888_to_rgb565(high):
                                palette = [high, low, vadd(vmul(high, 2/3), vmul(low, 1/3)), vadd(vmul(high, 1/3), vmul(low, 2/3))]
                            
                            else:
                                palette = [low, high, vadd(vmul(high, 0.5), vmul(low, 0.5)), (0, 0, 0)]
                            
                            
                            for i in range(2):
                                bytecode += rgb888_to_rgb565(palette[i])
                            
                            indices = ""
                            
                            for y in range(4):
                                for x in range(4):
                                    curr_pixel = image[(ycblock*8 + yblock*4 + y)][xcblock*8 + xblock*4 + x]
                                    
                                    low = 0
                                    diff = 1
                                    for i in range(len(palette)):
                                        curr_diff = vdiff(curr_pixel, palette[i])
                                        if curr_diff < diff:
                                            diff = curr_diff
                                            low = i
                                            
                                    indices += str(bin(low))[2:].zfill(2)
                                    
                            bytecode += int(indices, 2).to_bytes(4, byteorder="big")

            
            image = downscale(image)#[[image[row][rgb] for rgb in range(0, len(image[row]), 2)] for row in range(0, len(image), 2)] 
    return bytecode
#image = [png_to_rgb(r"C:\Users\felix\Desktop\test.png"), b"\x0E"]

def downscale(image):
    newimage = [[[0, 0, 0] for pixel in range(int(len(image[0])/2))] for row in range(int(len(image)/2))]
    for y, row in enumerate(image):
        for x, pixel in enumerate(row):
            newimage[math.floor(y/2)][math.floor(x/2)] = vadd(newimage[math.floor(y/2)][math.floor(x/2)], vmul(pixel, 0.25))
    return newimage
interpolate = 1
def torawblob(texture, inter):
    global interpolate
    interpolate = inter
    bytecode = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00x\xc8t\x06\xee\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \xaf0\x00\x00\x00\x01\x00\x00\x00\x0c\x00\x00\x00\x14\x00\x00\x00\x00'
    bytecode += len(texture[0][0]).to_bytes(2, byteorder="big")
    bytecode += len(texture[0]).to_bytes(2, byteorder="big")
    bytecode += b'\x00\x00\x00\x0e\x00\x00\x00@\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x05\x00\x00\x00\x01\x80\x00\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    bytecode += tpl_compress(texture)
    return bytecode