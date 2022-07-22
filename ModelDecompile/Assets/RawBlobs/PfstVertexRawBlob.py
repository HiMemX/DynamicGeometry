
def toverts(data):
    offset = 0x00
    verts = []

    offsetskip = 0x14

    while offset < len(data):
        buffer = data[offset:offset+0x14]

        X1 = int.from_bytes(buffer[0x00:0x02], "big", signed=True)/2**12
        X2 = int.from_bytes(buffer[0x02:0x04], "big", signed=True)/2**12
        
        Y1 = int.from_bytes(buffer[0x04:0x06], "big", signed=True)/2**12
        Y2 = int.from_bytes(buffer[0x06:0x08], "big", signed=True)/2**12
        
        Z1 = int.from_bytes(buffer[0x08:0x0A], "big", signed=True)/2**12
        Z2 = int.from_bytes(buffer[0x0A:0x0C], "big", signed=True)/2**12
        
        #print(int.from_bytes(buffer[0x00:0x02], "big"), X1, buffer.hex())
        verts.append([X1, Y1, Z1])
        verts.append([X2, Y2, Z2])


        # Type Check
        if len(data[offset+0x14:]) < 30:
            offset += offsetskip
            continue
        
        bufferlarge = data[offset:offset+0x44]
        first = int.from_bytes(bufferlarge[0x1C:0x20], "big")
        second = int.from_bytes(bufferlarge[0x20:0x24], "big")
        third = int.from_bytes(bufferlarge[0x40:0x44], "big")
        zerocheck = int.from_bytes(bufferlarge[0x12:0x14], "big")
        
        if (first == second or second == third or third == first) and zerocheck == 0:
            offsetskip = 0x24
        
        offset += offsetskip

    return verts


def tonormals(data):
    offset = 0x00
    normals = []

    offsetskip = 0x14

    while offset < len(data):
        buffer = data[offset:offset+0x14]

        X1 = int.from_bytes(buffer[0x0C:0x0D], "big", signed=True)/128
        X2 = int.from_bytes(buffer[0x0D:0x0E], "big", signed=True)/128
        Y1 = int.from_bytes(buffer[0x0E:0x0F], "big", signed=True)/128
        Y2 = int.from_bytes(buffer[0x0F:0x10], "big", signed=True)/128
        Z1 = int.from_bytes(buffer[0x10:0x11], "big", signed=True)/128
        Z2 = int.from_bytes(buffer[0x11:0x12], "big", signed=True)/128

        normals.append([-X1, Y1, Z1])
        normals.append([-X2, Y2, Z2])

        # Type Check
        if len(data[offset+0x14:]) < 30:
            offset += offsetskip
            continue
        
        bufferlarge = data[offset:offset+0x44]
        first = int.from_bytes(bufferlarge[0x1C:0x20], "big")
        second = int.from_bytes(bufferlarge[0x20:0x24], "big")
        third = int.from_bytes(bufferlarge[0x40:0x44], "big")
        zerocheck = int.from_bytes(bufferlarge[0x12:0x14], "big")
        
        if (first == second or second == third or third == first) and zerocheck == 0:
            offsetskip = 0x24
        
        offset += offsetskip

    return normals
