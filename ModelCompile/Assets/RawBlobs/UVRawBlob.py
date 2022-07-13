def torawblob(uvs, factor):
    data = b""
    for uv in uvs:
        for dimension in uv:
            data += int(dimension*(2**factor-1)).to_bytes(2, byteorder="big", signed=True)

    return data