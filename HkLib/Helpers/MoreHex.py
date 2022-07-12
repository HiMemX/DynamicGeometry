import struct

def BytesToFloat(bytes, endian):
    if endian == "big":
        return struct.unpack('<f', bytes)[0]
    return struct.unpack('>f', bytes)[0]

def FloatToBytes(bytes, endian):
    if endian == "big":
        return struct.pack('<f', bytes)
    return struct.pack('>f', bytes)

def GenerateBytes(byte, length):
    output = b""
    for i in range(length):
        output += byte

    return output