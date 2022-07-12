import struct

def toverts(data):
    verts = []
    for vert in range(0, len(data), 0x0C):
        verts.append([])

        verts[-1].append(-struct.unpack(">f", data[vert:vert+0x04])[0])
        verts[-1].append(struct.unpack(">f", data[vert+0x04:vert+0x08])[0])
        verts[-1].append(struct.unpack(">f", data[vert+0x08:vert+0x0C])[0])
        
    return verts