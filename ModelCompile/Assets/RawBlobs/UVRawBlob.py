import struct

def torawblob(uvs, factor):
    data = b""
    for uv in uvs:
        for dimension in uv:
            data += int(dimension/1.01*(2**factor)).to_bytes(2, byteorder="big", signed=True)

    return data