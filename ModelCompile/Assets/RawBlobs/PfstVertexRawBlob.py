
def torawblob(data, verts, normals):
    offset = 0x00
    offsetskip = 0x14

    output = b""

    for v in range(0, len(verts), 2):
        # Type Check
        if len(data[offset+0x14:]) >= 30:
            bufferlarge = data[offset:offset+0x44]
            first = int.from_bytes(bufferlarge[0x1C:0x20], "big")
            second = int.from_bytes(bufferlarge[0x20:0x24], "big")
            third = int.from_bytes(bufferlarge[0x40:0x44], "big")
            zerocheck = int.from_bytes(bufferlarge[0x12:0x14], "big")
            
            if (first == second or second == third or third == first) and zerocheck == 0:
                offsetskip = 0x24
            
        buffer = data[offset:offset+offsetskip]
        newbuffer = b""

        newbuffer += int(verts[v][0]*2**12).to_bytes(2, byteorder="big", signed=True)
        newbuffer += int(verts[v+1][0]*2**12).to_bytes(2, byteorder="big", signed=True)
        newbuffer += int(verts[v][1]*2**12).to_bytes(2, byteorder="big", signed=True)
        newbuffer += int(verts[v+1][1]*2**12).to_bytes(2, byteorder="big", signed=True)
        newbuffer += int(verts[v][2]*2**12).to_bytes(2, byteorder="big", signed=True)
        newbuffer += int(verts[v+1][2]*2**12).to_bytes(2, byteorder="big", signed=True)

        newbuffer += int(normals[v][0]*-127).to_bytes(1, byteorder="big", signed=True)
        newbuffer += int(normals[v+1][0]*-127).to_bytes(1, byteorder="big", signed=True)
        newbuffer += int(normals[v][1]*127).to_bytes(1, byteorder="big", signed=True)
        newbuffer += int(normals[v+1][1]*127).to_bytes(1, byteorder="big", signed=True)
        newbuffer += int(normals[v][2]*127).to_bytes(1, byteorder="big", signed=True)
        newbuffer += int(normals[v+1][2]*127).to_bytes(1, byteorder="big", signed=True)

        newbuffer += buffer[0x12:]

        output += newbuffer

        offset += offsetskip

    return output