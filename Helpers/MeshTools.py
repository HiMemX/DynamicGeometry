def clamp(value): # 0 -> 1
    if value > 1:
        return 1
    elif value < 0:
        return 0
    return value

def clampuvs(uvs):
    newuvs = []
    for uv in uvs:
        newuvs.append([clamp(uv[0]), clamp(uv[1])])
    return newuvs