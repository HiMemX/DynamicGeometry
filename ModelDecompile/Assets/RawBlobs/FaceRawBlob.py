
def tofaces(data, animamount, referenceamount):
    offset = 0
    faces = []

    while offset < len(data):
        mode = data[offset:offset+1]
        offset += 0x01

        if mode == b"\x90": # Normal Definition Mode (Check out the modern ToS Wiki for more info)
            indexamount = int.from_bytes(data[offset:offset+2], "big")
            offset += 0x02
            for tri in range(int(indexamount/3)):
                face = []
                for indx in range(3):
                    index = []
                    offset += animamount

                    for reference in range(referenceamount):
                        index.append(int.from_bytes(data[offset:offset+0x02], "big"))
                        offset += 0x02

                    face.append([index[0], index[-1]]) # UVS TEMPORARILY DISABLED
                        
                faces.append(face)

        elif mode == b"\x98":
            indexamount = int.from_bytes(data[offset:offset+2], "big")
            offset += 0x02
            face = []
            for tri in range(0, indexamount):
                index = []
                offset += animamount

                for reference in range(referenceamount):
                    index.append(int.from_bytes(data[offset:offset+0x02], "big"))
                    offset += 0x02

                face.append([index[0], index[-1]]) # UVS TEMPORARILY DISABLED
            
            faces.append(face)
            #for i in range(len(face)-2):
            #    faces.append([face[i], face[i+1], face[i+2]])
    
    
    indices = []
    for i in faces:
        for x in range(len(i)-2):
            if (x+1) % 2 == 0:
                indices.append([(i[x][0], i[x][-1]), (i[x+2][0], i[x+2][-1]), (i[x+1][0], i[x+1][-1])])
                continue
            
            indices.append([(i[x][0], i[x][-1]), (i[x+1][0], i[x+1][-1]), (i[x+2][0], i[x+2][-1])])

    return indices
                        

