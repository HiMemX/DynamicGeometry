import struct

def torawblob(verts):
    data = b""
    for vert in verts:
        data += struct.pack("f", -vert[0])[::-1]
        data += struct.pack("f", vert[1])[::-1]
        data += struct.pack("f", vert[2])[::-1]

    return data