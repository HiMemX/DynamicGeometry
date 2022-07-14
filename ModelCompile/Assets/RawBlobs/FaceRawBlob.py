def torawblob(faces, animamount, referenceamount):
    data = b""

    mode = b"\x90"
    chunk = 0
    chunksize = 0x1000
    for fi, face in enumerate(faces):
        if chunk == 0:

            amount = (len(faces)-fi)*3
            if len(face)-fi > chunksize:
                amount = chunksize*3

            data += mode + amount.to_bytes(2, byteorder="big")
    

        if chunk >= chunksize:
            chunk = 0
        
        chunk += 1

        for index in face[:3]:
            data += bytes(animamount)
            data += index[0].to_bytes(2, byteorder="big")
            data += index[2].to_bytes(2, byteorder="big")
            
            for reference in range(referenceamount-3):
                data += bytes(2)

            data += index[1].to_bytes(2, byteorder="big")

    return data
            
