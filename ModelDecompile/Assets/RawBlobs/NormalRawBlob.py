
def tonormals(data):
    normals = []
    for vert in range(0, len(data), 0x03):
        normals.append([])

        normals[-1].append(int.from_bytes(data[vert:vert+0x01], "big", signed=True)/127.5)
        normals[-1].append(int.from_bytes(data[vert+0x01:vert+0x02], "big", signed=True)/127.5)
        normals[-1].append(int.from_bytes(data[vert+0x02:vert+0x03], "big", signed=True)/127.5)
        
    return normals
