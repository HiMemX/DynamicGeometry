def torawblob(normals):
    data = b""
    for normal in normals:
        for dimension in normal:
            data += int(dimension*127).to_bytes(1, byteorder="big", signed=True)

    return data