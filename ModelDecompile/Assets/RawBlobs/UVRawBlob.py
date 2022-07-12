
def touvs(data, uvfactor):
    uvs = []
    for uv in range(0, len(data), 0x04):
        uvs.append([])
        for dimension in range(0, 0x04, 0x02):
            uvs[-1].append(int.from_bytes(data[uv+dimension:uv+dimension+0x02], "big", signed=True)/(2**uvfactor))
        
    return uvs