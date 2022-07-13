
from sys import byteorder


def torawblob(faces, animamount, referenceamount):
    mode = b"\x90"
    amount = len(faces)*3

    data = mode + amount.to_bytes(2, byteorder="big")

    for face in faces:
        for index in face[:3]:
            data += bytes(animamount)
            data += index[0].to_bytes(2, byteorder="big")
            data += index[2].to_bytes(2, byteorder="big")
            
            for reference in range(referenceamount-3):
                data += bytes(2)

            data += index[1].to_bytes(2, byteorder="big")

    return data
            
