
def getids(data):
    textureamount = int.from_bytes(data[0x14:0x15], "big")-1
    #if textureamount == 0: return []

    textures = [data[:0x08]]
    offset = int.from_bytes(data[0x1F:0x20], "big")

    for texture in range(textureamount):
        textures.append(data[offset:offset+0x08])
        offset += 0x10

    return textures