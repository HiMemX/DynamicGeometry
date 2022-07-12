def rgb565(color):
    return (color >> 11 << 3 & 0xff, color >> 5 << 2 & 0xff, color >> 0 << 3 & 0xff)

def vadd(vector1, vector2):
    return (vector1[0] + vector2[0], vector1[1] + vector2[1], vector1[2] + vector2[2])

def vmul(vector1, factor):
    return (int(vector1[0] * factor), int(vector1[1] * factor), int(vector1[2] * factor))

def totexture(data):
    rel_offset = 0x20
    offset = 0x24
    
    image_headers = [] # [offset, ...]
    images = [] # [[sizex, sizey, mode, offset], [...], ...]
        
    image_count = int.from_bytes(data[offset:offset+0x04], "big")
    offset+=0x04
    image_table_offset = int.from_bytes(data[offset:offset+0x04], "big") + rel_offset
    offset+=0x04

    offset = image_table_offset
    for i in range(image_count):
        image_headers.append(int.from_bytes(data[offset:offset+0x04], "big") + rel_offset)
        offset+=0x08
    
    for i in image_headers:
        offset=i
        
        sizey = int.from_bytes(data[offset:offset+0x02], "big"); offset+=0x02
        sizex = int.from_bytes(data[offset:offset+0x02], "big"); offset+=0x05
        mode = data[offset:offset+0x01]; offset+=0x01
        image_offset = int.from_bytes(data[offset:offset+0x04], "big") + rel_offset; offset+=0x04
        
        images.append([sizex, sizey, mode, image_offset])
    
    decompressed_images = []
    
    for i in images:
        offset = i[3]
    
        image = [[0 for i in range(i[0])] for y in range(i[1])]
        
        if i[2] == b"\x00":
            for ycblock in range(int(i[1]/8)):
                for xcblock in range(int(i[0]/8)):
                    for y in range(8):
                        for ymod in range(4):
                            indices = int.from_bytes(data[offset:offset+0x01], "big"); offset+=0x01
                            for x in range(2):
                                value = (indices >> ((1-x) * 4) & 15) << 4 
                                image[-1-(ycblock*8 + y)][xcblock*8 + (x+ymod*2)] = value
          
        elif i[2] == b"\x0E":
            for ycblock in range(int(i[1]/8)):
                for xcblock in range(int(i[0]/8)):
                    for yblock in range(2):
                        for xblock in range(2):
                            color1int = int.from_bytes(data[offset:offset+0x02], "big"); offset+=0x02
                            color2int = int.from_bytes(data[offset:offset+0x02], "big"); offset+=0x02
                            
                            color1 = rgb565(color1int)
                            color2 = rgb565(color2int)
                            
                            if color1int > color2int:
                                palette = [color1, color2, vadd(vmul(color1, 2/3), vmul(color2, 1/3)), vadd(vmul(color1, 1/3), vmul(color2, 2/3))]
                                
                            else:
                                palette = [color1, color2, vadd(vmul(color2, 0.5), vmul(color1, 0.5)), (0, 0, 0)]

                            for y in range(4):
                                indices = int.from_bytes(data[offset:offset+0x01], "big"); offset+=0x01
                                for x in range(4):
                                    image[-1-(ycblock*8 + yblock*4 + y)][xcblock*8 + xblock*4 + (3-x)] = palette[indices >> (x * 2) & 3]
        
        else:
            image = "INVALID_TYPE"
        
        decompressed_images.append(image)
    
    return decompressed_images